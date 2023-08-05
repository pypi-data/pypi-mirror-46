# -*- coding: utf-8 -*-
# Licensed under a 3-clause BSD style license - see LICENSE.rst

import fnmatch
import time
import re
import datetime
import warnings
from collections import OrderedDict, defaultdict

import numpy as np

from astropy.utils.decorators import lazyproperty
from astropy.utils.exceptions import AstropyDeprecationWarning
from astropy import units as u
from astropy import _erfa as erfa
from .utils import day_frac, quantity_day_frac, two_sum, two_product


__all__ = ['TimeFormat', 'TimeJD', 'TimeMJD', 'TimeFromEpoch', 'TimeUnix',
           'TimeCxcSec', 'TimeGPS', 'TimeDecimalYear',
           'TimePlotDate', 'TimeUnique', 'TimeDatetime', 'TimeString',
           'TimeISO', 'TimeISOT', 'TimeFITS', 'TimeYearDayTime',
           'TimeEpochDate', 'TimeBesselianEpoch', 'TimeJulianEpoch',
           'TimeDeltaFormat', 'TimeDeltaSec', 'TimeDeltaJD',
           'TimeEpochDateString', 'TimeBesselianEpochString',
           'TimeJulianEpochString', 'TIME_FORMATS', 'TIME_DELTA_FORMATS',
           'TimezoneInfo', 'TimeDeltaDatetime', 'TimeDatetime64']

__doctest_skip__ = ['TimePlotDate']

# These both get filled in at end after TimeFormat subclasses defined.
# Use an OrderedDict to fix the order in which formats are tried.
# This ensures, e.g., that 'isot' gets tried before 'fits'.
TIME_FORMATS = OrderedDict()
TIME_DELTA_FORMATS = OrderedDict()

# Translations between deprecated FITS timescales defined by
# Rots et al. 2015, A&A 574:A36, and timescales used here.
FITS_DEPRECATED_SCALES = {'TDT': 'tt', 'ET': 'tt',
                          'GMT': 'utc', 'UT': 'utc', 'IAT': 'tai'}


def _regexify_subfmts(subfmts):
    """
    Iterate through each of the sub-formats and try substituting simple
    regular expressions for the strptime codes for year, month, day-of-month,
    hour, minute, second.  If no % characters remain then turn the final string
    into a compiled regex.  This assumes time formats do not have a % in them.

    This is done both to speed up parsing of strings and to allow mixed formats
    where strptime does not quite work well enough.
    """
    new_subfmts = []
    for subfmt_tuple in subfmts:
        subfmt_in = subfmt_tuple[1]
        for strptime_code, regex in (('%Y', r'(?P<year>\d\d\d\d)'),
                                     ('%m', r'(?P<mon>\d{1,2})'),
                                     ('%d', r'(?P<mday>\d{1,2})'),
                                     ('%H', r'(?P<hour>\d{1,2})'),
                                     ('%M', r'(?P<min>\d{1,2})'),
                                     ('%S', r'(?P<sec>\d{1,2})')):
            subfmt_in = subfmt_in.replace(strptime_code, regex)

        if '%' not in subfmt_in:
            subfmt_tuple = (subfmt_tuple[0],
                            re.compile(subfmt_in + '$'),
                            subfmt_tuple[2])
        new_subfmts.append(subfmt_tuple)

    return tuple(new_subfmts)


class TimeFormatMeta(type):
    """
    Metaclass that adds `TimeFormat` and `TimeDeltaFormat` to the
    `TIME_FORMATS` and `TIME_DELTA_FORMATS` registries, respectively.
    """

    _registry = TIME_FORMATS

    def __new__(mcls, name, bases, members):
        cls = super().__new__(mcls, name, bases, members)

        # Register time formats that have a name, but leave out astropy_time since
        # it is not a user-accessible format and is only used for initialization into
        # a different format.
        if 'name' in members and cls.name != 'astropy_time':
            mcls._registry[cls.name] = cls

        if 'subfmts' in members:
            cls.subfmts = _regexify_subfmts(members['subfmts'])

        return cls


class TimeFormat(metaclass=TimeFormatMeta):
    """
    Base class for time representations.

    Parameters
    ----------
    val1 : numpy ndarray, list, number, str, or bytes
        Values to initialize the time or times.  Bytes are decoded as ascii.
    val2 : numpy ndarray, list, or number; optional
        Value(s) to initialize the time or times.  Only used for numerical
        input, to help preserve precision.
    scale : str
        Time scale of input value(s)
    precision : int
        Precision for seconds as floating point
    in_subfmt : str
        Select subformat for inputting string times
    out_subfmt : str
        Select subformat for outputting string times
    from_jd : bool
        If true then val1, val2 are jd1, jd2
    """

    _default_scale = 'utc'  # As of astropy 0.4

    def __init__(self, val1, val2, scale, precision,
                 in_subfmt, out_subfmt, from_jd=False):
        self.scale = scale  # validation of scale done later with _check_scale
        self.precision = precision
        self.in_subfmt = in_subfmt
        self.out_subfmt = out_subfmt

        if from_jd:
            self.jd1 = val1
            self.jd2 = val2
        else:
            val1, val2 = self._check_val_type(val1, val2)
            self.set_jds(val1, val2)

    def __len__(self):
        return len(self.jd1)

    @property
    def scale(self):
        """Time scale"""
        self._scale = self._check_scale(self._scale)
        return self._scale

    @scale.setter
    def scale(self, val):
        self._scale = val

    def mask_if_needed(self, value):
        if self.masked:
            value = np.ma.array(value, mask=self.mask, copy=False)
        return value

    @property
    def mask(self):
        if 'mask' not in self.cache:
            self.cache['mask'] = np.isnan(self.jd2)
            if self.cache['mask'].shape:
                self.cache['mask'].flags.writeable = False
        return self.cache['mask']

    @property
    def masked(self):
        if 'masked' not in self.cache:
            self.cache['masked'] = bool(np.any(self.mask))
        return self.cache['masked']

    @property
    def jd2_filled(self):
        return np.nan_to_num(self.jd2) if self.masked else self.jd2

    @lazyproperty
    def cache(self):
        """
        Return the cache associated with this instance.
        """
        return defaultdict(dict)

    def _check_val_type(self, val1, val2):
        """Input value validation, typically overridden by derived classes"""
        # val1 cannot contain nan, but val2 can contain nan
        ok1 = val1.dtype == np.double and np.all(np.isfinite(val1))
        ok2 = val2 is None or (val2.dtype == np.double and not np.any(np.isinf(val2)))
        if not (ok1 and ok2):
            raise TypeError('Input values for {0} class must be finite doubles'
                            .format(self.name))

        if getattr(val1, 'unit', None) is not None:
            # Convert any quantity-likes to days first, attempting to be
            # careful with the conversion, so that, e.g., large numbers of
            # seconds get converted without loosing precision because
            # 1/86400 is not exactly representable as a float.
            val1 = u.Quantity(val1, copy=False)
            if val2 is not None:
                val2 = u.Quantity(val2, copy=False)

            try:
                val1, val2 = quantity_day_frac(val1, val2)
            except u.UnitsError:
                raise u.UnitConversionError(
                    "only quantities with time units can be "
                    "used to instantiate Time instances.")
            # We now have days, but the format may expect another unit.
            # On purpose, multiply with 1./day_unit because typically it is
            # 1./erfa.DAYSEC, and inverting it recovers the integer.
            # (This conversion will get undone in format's set_jds, hence
            # there may be room for optimizing this.)
            factor = 1. / getattr(self, 'unit', 1.)
            if factor != 1.:
                val1, carry = two_product(val1, factor)
                carry += val2 * factor
                val1, val2 = two_sum(val1, carry)

        elif getattr(val2, 'unit', None) is not None:
            raise TypeError('Cannot mix float and Quantity inputs')

        if val2 is None:
            val2 = np.zeros_like(val1)

        def asarray_or_scalar(val):
            """
            Remove ndarray subclasses since for jd1/jd2 we want a pure ndarray
            or a Python or numpy scalar.
            """
            return np.asarray(val) if isinstance(val, np.ndarray) else val

        return asarray_or_scalar(val1), asarray_or_scalar(val2)

    def _check_scale(self, scale):
        """
        Return a validated scale value.

        If there is a class attribute 'scale' then that defines the default /
        required time scale for this format.  In this case if a scale value was
        provided that needs to match the class default, otherwise return
        the class default.

        Otherwise just make sure that scale is in the allowed list of
        scales.  Provide a different error message if `None` (no value) was
        supplied.
        """
        if scale is None:
            scale = self._default_scale

        if scale not in TIME_SCALES:
            raise ScaleValueError("Scale value '{0}' not in "
                                  "allowed values {1}"
                                  .format(scale, TIME_SCALES))

        return scale

    def set_jds(self, val1, val2):
        """
        Set internal jd1 and jd2 from val1 and val2.  Must be provided
        by derived classes.
        """
        raise NotImplementedError

    def to_value(self, parent=None):
        """
        Return time representation from internal jd1 and jd2.  This is
        the base method that ignores ``parent`` and requires that
        subclasses implement the ``value`` property.  Subclasses that
        require ``parent`` or have other optional args for ``to_value``
        should compute and return the value directly.
        """
        return self.mask_if_needed(self.value)

    @property
    def value(self):
        raise NotImplementedError


class TimeJD(TimeFormat):
    """
    Julian Date time format.
    This represents the number of days since the beginning of
    the Julian Period.
    For example, 2451544.5 in JD is midnight on January 1, 2000.
    """
    name = 'jd'

    def set_jds(self, val1, val2):
        self._check_scale(self._scale)  # Validate scale.
        self.jd1, self.jd2 = day_frac(val1, val2)

    @property
    def value(self):
        return self.jd1 + self.jd2


class TimeMJD(TimeFormat):
    """
    Modified Julian Date time format.
    This represents the number of days since midnight on November 17, 1858.
    For example, 51544.0 in MJD is midnight on January 1, 2000.
    """
    name = 'mjd'

    def set_jds(self, val1, val2):
        # TODO - this routine and vals should be Cythonized to follow the ERFA
        # convention of preserving precision by adding to the larger of the two
        # values in a vectorized operation.  But in most practical cases the
        # first one is probably biggest.
        self._check_scale(self._scale)  # Validate scale.
        jd1, jd2 = day_frac(val1, val2)
        jd1 += erfa.DJM0  # erfa.DJM0=2400000.5 (from erfam.h)
        self.jd1, self.jd2 = day_frac(jd1, jd2)

    @property
    def value(self):
        return (self.jd1 - erfa.DJM0) + self.jd2


class TimeDecimalYear(TimeFormat):
    """
    Time as a decimal year, with integer values corresponding to midnight
    of the first day of each year.  For example 2000.5 corresponds to the
    ISO time '2000-07-02 00:00:00'.
    """
    name = 'decimalyear'

    def set_jds(self, val1, val2):
        self._check_scale(self._scale)  # Validate scale.

        sum12, err12 = two_sum(val1, val2)
        iy_start = np.trunc(sum12).astype(int)
        extra, y_frac = two_sum(sum12, -iy_start)
        y_frac += extra + err12

        val = (val1 + val2).astype(np.double)
        iy_start = np.trunc(val).astype(int)

        imon = np.ones_like(iy_start)
        iday = np.ones_like(iy_start)
        ihr = np.zeros_like(iy_start)
        imin = np.zeros_like(iy_start)
        isec = np.zeros_like(y_frac)

        # Possible enhancement: use np.unique to only compute start, stop
        # for unique values of iy_start.
        scale = self.scale.upper().encode('ascii')
        jd1_start, jd2_start = erfa.dtf2d(scale, iy_start, imon, iday,
                                          ihr, imin, isec)
        jd1_end, jd2_end = erfa.dtf2d(scale, iy_start + 1, imon, iday,
                                      ihr, imin, isec)

        t_start = Time(jd1_start, jd2_start, scale=self.scale, format='jd')
        t_end = Time(jd1_end, jd2_end, scale=self.scale, format='jd')
        t_frac = t_start + (t_end - t_start) * y_frac

        self.jd1, self.jd2 = day_frac(t_frac.jd1, t_frac.jd2)

    @property
    def value(self):
        scale = self.scale.upper().encode('ascii')
        iy_start, ims, ids, ihmsfs = erfa.d2dtf(scale, 0,  # precision=0
                                                self.jd1, self.jd2_filled)
        imon = np.ones_like(iy_start)
        iday = np.ones_like(iy_start)
        ihr = np.zeros_like(iy_start)
        imin = np.zeros_like(iy_start)
        isec = np.zeros_like(self.jd1)

        # Possible enhancement: use np.unique to only compute start, stop
        # for unique values of iy_start.
        scale = self.scale.upper().encode('ascii')
        jd1_start, jd2_start = erfa.dtf2d(scale, iy_start, imon, iday,
                                          ihr, imin, isec)
        jd1_end, jd2_end = erfa.dtf2d(scale, iy_start + 1, imon, iday,
                                      ihr, imin, isec)

        dt = (self.jd1 - jd1_start) + (self.jd2 - jd2_start)
        dt_end = (jd1_end - jd1_start) + (jd2_end - jd2_start)
        decimalyear = iy_start + dt / dt_end

        return decimalyear


class TimeFromEpoch(TimeFormat):
    """
    Base class for times that represent the interval from a particular
    epoch as a floating point multiple of a unit time interval (e.g. seconds
    or days).
    """

    def __init__(self, val1, val2, scale, precision,
                 in_subfmt, out_subfmt, from_jd=False):
        self.scale = scale
        # Initialize the reference epoch (a single time defined in subclasses)
        epoch = Time(self.epoch_val, self.epoch_val2, scale=self.epoch_scale,
                     format=self.epoch_format)
        self.epoch = epoch

        # Now create the TimeFormat object as normal
        super().__init__(val1, val2, scale, precision, in_subfmt, out_subfmt,
                         from_jd)

    def set_jds(self, val1, val2):
        """
        Initialize the internal jd1 and jd2 attributes given val1 and val2.
        For an TimeFromEpoch subclass like TimeUnix these will be floats giving
        the effective seconds since an epoch time (e.g. 1970-01-01 00:00:00).
        """
        # Form new JDs based on epoch time + time from epoch (converted to JD).
        # One subtlety that might not be obvious is that 1.000 Julian days in
        # UTC can be 86400 or 86401 seconds.  For the TimeUnix format the
        # assumption is that every day is exactly 86400 seconds, so this is, in
        # principle, doing the math incorrectly, *except* that it matches the
        # definition of Unix time which does not include leap seconds.

        # note: use divisor=1./self.unit, since this is either 1 or 1/86400,
        # and 1/86400 is not exactly representable as a float64, so multiplying
        # by that will cause rounding errors. (But inverting it as a float64
        # recovers the exact number)
        day, frac = day_frac(val1, val2, divisor=1. / self.unit)

        jd1 = self.epoch.jd1 + day
        jd2 = self.epoch.jd2 + frac

        # Create a temporary Time object corresponding to the new (jd1, jd2) in
        # the epoch scale (e.g. UTC for TimeUnix) then convert that to the
        # desired time scale for this object.
        #
        # A known limitation is that the transform from self.epoch_scale to
        # self.scale cannot involve any metadata like lat or lon.
        try:
            tm = getattr(Time(jd1, jd2, scale=self.epoch_scale,
                              format='jd'), self.scale)
        except Exception as err:
            raise ScaleValueError("Cannot convert from '{0}' epoch scale '{1}'"
                                  "to specified scale '{2}', got error:\n{3}"
                                  .format(self.name, self.epoch_scale,
                                          self.scale, err))

        self.jd1, self.jd2 = day_frac(tm._time.jd1, tm._time.jd2)

    def to_value(self, parent=None):
        # Make sure that scale is the same as epoch scale so we can just
        # subtract the epoch and convert
        if self.scale != self.epoch_scale:
            if parent is None:
                raise ValueError('cannot compute value without parent Time object')
            try:
                tm = getattr(parent, self.epoch_scale)
            except Exception as err:
                raise ScaleValueError("Cannot convert from '{0}' epoch scale '{1}'"
                                      "to specified scale '{2}', got error:\n{3}"
                                      .format(self.name, self.epoch_scale,
                                              self.scale, err))

            jd1, jd2 = tm._time.jd1, tm._time.jd2
        else:
            jd1, jd2 = self.jd1, self.jd2

        time_from_epoch = ((jd1 - self.epoch.jd1) +
                           (jd2 - self.epoch.jd2)) / self.unit

        return self.mask_if_needed(time_from_epoch)

    value = property(to_value)

    @property
    def _default_scale(self):
        return self.epoch_scale


class TimeUnix(TimeFromEpoch):
    """
    Unix time: seconds from 1970-01-01 00:00:00 UTC.
    For example, 946684800.0 in Unix time is midnight on January 1, 2000.

    NOTE: this quantity is not exactly unix time and differs from the strict
    POSIX definition by up to 1 second on days with a leap second.  POSIX
    unix time actually jumps backward by 1 second at midnight on leap second
    days while this class value is monotonically increasing at 86400 seconds
    per UTC day.
    """
    name = 'unix'
    unit = 1.0 / erfa.DAYSEC  # in days (1 day == 86400 seconds)
    epoch_val = '1970-01-01 00:00:00'
    epoch_val2 = None
    epoch_scale = 'utc'
    epoch_format = 'iso'


class TimeCxcSec(TimeFromEpoch):
    """
    Chandra X-ray Center seconds from 1998-01-01 00:00:00 TT.
    For example, 63072064.184 is midnight on January 1, 2000.
    """
    name = 'cxcsec'
    unit = 1.0 / erfa.DAYSEC  # in days (1 day == 86400 seconds)
    epoch_val = '1998-01-01 00:00:00'
    epoch_val2 = None
    epoch_scale = 'tt'
    epoch_format = 'iso'


class TimeGPS(TimeFromEpoch):
    """GPS time: seconds from 1980-01-06 00:00:00 UTC
    For example, 630720013.0 is midnight on January 1, 2000.

    Notes
    =====
    This implementation is strictly a representation of the number of seconds
    (including leap seconds) since midnight UTC on 1980-01-06.  GPS can also be
    considered as a time scale which is ahead of TAI by a fixed offset
    (to within about 100 nanoseconds).

    For details, see http://tycho.usno.navy.mil/gpstt.html
    """
    name = 'gps'
    unit = 1.0 / erfa.DAYSEC  # in days (1 day == 86400 seconds)
    epoch_val = '1980-01-06 00:00:19'
    # above epoch is the same as Time('1980-01-06 00:00:00', scale='utc').tai
    epoch_val2 = None
    epoch_scale = 'tai'
    epoch_format = 'iso'


class TimePlotDate(TimeFromEpoch):
    """
    Matplotlib `~matplotlib.pyplot.plot_date` input:
    1 + number of days from 0001-01-01 00:00:00 UTC

    This can be used directly in the matplotlib `~matplotlib.pyplot.plot_date`
    function::

      >>> import matplotlib.pyplot as plt
      >>> jyear = np.linspace(2000, 2001, 20)
      >>> t = Time(jyear, format='jyear', scale='utc')
      >>> plt.plot_date(t.plot_date, jyear)
      >>> plt.gcf().autofmt_xdate()  # orient date labels at a slant
      >>> plt.draw()

    For example, 730120.0003703703 is midnight on January 1, 2000.
    """
    # This corresponds to the zero reference time for matplotlib plot_date().
    # Note that TAI and UTC are equivalent at the reference time.
    name = 'plot_date'
    unit = 1.0
    epoch_val = 1721424.5  # Time('0001-01-01 00:00:00', scale='tai').jd - 1
    epoch_val2 = None
    epoch_scale = 'utc'
    epoch_format = 'jd'


class TimeUnique(TimeFormat):
    """
    Base class for time formats that can uniquely create a time object
    without requiring an explicit format specifier.  This class does
    nothing but provide inheritance to identify a class as unique.
    """


class TimeAstropyTime(TimeUnique):
    """
    Instantiate date from an Astropy Time object (or list thereof).

    This is purely for instantiating from a Time object.  The output
    format is the same as the first time instance.
    """
    name = 'astropy_time'

    def __new__(cls, val1, val2, scale, precision,
                in_subfmt, out_subfmt, from_jd=False):
        """
        Use __new__ instead of __init__ to output a class instance that
        is the same as the class of the first Time object in the list.
        """
        val1_0 = val1.flat[0]
        if not (isinstance(val1_0, Time) and all(type(val) is type(val1_0)
                                                 for val in val1.flat)):
            raise TypeError('Input values for {0} class must all be same '
                            'astropy Time type.'.format(cls.name))

        if scale is None:
            scale = val1_0.scale
        if val1.shape:
            vals = [getattr(val, scale)._time for val in val1]
            jd1 = np.concatenate([np.atleast_1d(val.jd1) for val in vals])
            jd2 = np.concatenate([np.atleast_1d(val.jd2) for val in vals])
        else:
            val = getattr(val1_0, scale)._time
            jd1, jd2 = val.jd1, val.jd2

        OutTimeFormat = val1_0._time.__class__
        self = OutTimeFormat(jd1, jd2, scale, precision, in_subfmt, out_subfmt,
                             from_jd=True)

        return self


class TimeDatetime(TimeUnique):
    """
    Represent date as Python standard library `~datetime.datetime` object

    Example::

      >>> from astropy.time import Time
      >>> from datetime import datetime
      >>> t = Time(datetime(2000, 1, 2, 12, 0, 0), scale='utc')
      >>> t.iso
      '2000-01-02 12:00:00.000'
      >>> t.tt.datetime
      datetime.datetime(2000, 1, 2, 12, 1, 4, 184000)
    """
    name = 'datetime'

    def _check_val_type(self, val1, val2):
        # Note: don't care about val2 for this class
        if not all(isinstance(val, datetime.datetime) for val in val1.flat):
            raise TypeError('Input values for {0} class must be '
                            'datetime objects'.format(self.name))
        return val1, None

    def set_jds(self, val1, val2):
        """Convert datetime object contained in val1 to jd1, jd2"""
        # Iterate through the datetime objects, getting year, month, etc.
        iterator = np.nditer([val1, None, None, None, None, None, None],
                             flags=['refs_ok'],
                             op_dtypes=[object] + 5*[np.intc] + [np.double])
        for val, iy, im, id, ihr, imin, dsec in iterator:
            dt = val.item()

            if dt.tzinfo is not None:
                dt = (dt - dt.utcoffset()).replace(tzinfo=None)

            iy[...] = dt.year
            im[...] = dt.month
            id[...] = dt.day
            ihr[...] = dt.hour
            imin[...] = dt.minute
            dsec[...] = dt.second + dt.microsecond / 1e6

        jd1, jd2 = erfa.dtf2d(self.scale.upper().encode('ascii'),
                              *iterator.operands[1:])
        self.jd1, self.jd2 = day_frac(jd1, jd2)

    def to_value(self, timezone=None, parent=None):
        """
        Convert to (potentially timezone-aware) `~datetime.datetime` object.

        If ``timezone`` is not ``None``, return a timezone-aware datetime
        object.

        Parameters
        ----------
        timezone : {`~datetime.tzinfo`, None} (optional)
            If not `None`, return timezone-aware datetime.

        Returns
        -------
        `~datetime.datetime`
            If ``timezone`` is not ``None``, output will be timezone-aware.
        """
        if timezone is not None:
            if self._scale != 'utc':
                raise ScaleValueError("scale is {}, must be 'utc' when timezone "
                                      "is supplied.".format(self._scale))

        # Rather than define a value property directly, we have a function,
        # since we want to be able to pass in timezone information.
        scale = self.scale.upper().encode('ascii')
        iys, ims, ids, ihmsfs = erfa.d2dtf(scale, 6,  # 6 for microsec
                                           self.jd1, self.jd2_filled)
        ihrs = ihmsfs['h']
        imins = ihmsfs['m']
        isecs = ihmsfs['s']
        ifracs = ihmsfs['f']
        iterator = np.nditer([iys, ims, ids, ihrs, imins, isecs, ifracs, None],
                             flags=['refs_ok'],
                             op_dtypes=7*[iys.dtype] + [object])

        for iy, im, id, ihr, imin, isec, ifracsec, out in iterator:
            if isec >= 60:
                raise ValueError('Time {} is within a leap second but datetime '
                                 'does not support leap seconds'
                                 .format((iy, im, id, ihr, imin, isec, ifracsec)))
            if timezone is not None:
                out[...] = datetime.datetime(iy, im, id, ihr, imin, isec, ifracsec,
                                             tzinfo=TimezoneInfo()).astimezone(timezone)
            else:
                out[...] = datetime.datetime(iy, im, id, ihr, imin, isec, ifracsec)

        return self.mask_if_needed(iterator.operands[-1])

    value = property(to_value)


class TimezoneInfo(datetime.tzinfo):
    """
    Subclass of the `~datetime.tzinfo` object, used in the
    to_datetime method to specify timezones.

    It may be safer in most cases to use a timezone database package like
    pytz rather than defining your own timezones - this class is mainly
    a workaround for users without pytz.
    """
    @u.quantity_input(utc_offset=u.day, dst=u.day)
    def __init__(self, utc_offset=0*u.day, dst=0*u.day, tzname=None):
        """
        Parameters
        ----------
        utc_offset : `~astropy.units.Quantity` (optional)
            Offset from UTC in days. Defaults to zero.
        dst : `~astropy.units.Quantity` (optional)
            Daylight Savings Time offset in days. Defaults to zero
            (no daylight savings).
        tzname : string, `None` (optional)
            Name of timezone

        Examples
        --------
        >>> from datetime import datetime
        >>> from astropy.time import TimezoneInfo  # Specifies a timezone
        >>> import astropy.units as u
        >>> utc = TimezoneInfo()    # Defaults to UTC
        >>> utc_plus_one_hour = TimezoneInfo(utc_offset=1*u.hour)  # UTC+1
        >>> dt_aware = datetime(2000, 1, 1, 0, 0, 0, tzinfo=utc_plus_one_hour)
        >>> print(dt_aware)
        2000-01-01 00:00:00+01:00
        >>> print(dt_aware.astimezone(utc))
        1999-12-31 23:00:00+00:00
        """
        if utc_offset == 0 and dst == 0 and tzname is None:
            tzname = 'UTC'
        self._utcoffset = datetime.timedelta(utc_offset.to_value(u.day))
        self._tzname = tzname
        self._dst = datetime.timedelta(dst.to_value(u.day))

    def utcoffset(self, dt):
        return self._utcoffset

    def tzname(self, dt):
        return str(self._tzname)

    def dst(self, dt):
        return self._dst


class TimeString(TimeUnique):
    """
    Base class for string-like time representations.

    This class assumes that anything following the last decimal point to the
    right is a fraction of a second.

    This is a reference implementation can be made much faster with effort.
    """

    def _check_val_type(self, val1, val2):
        # Note: don't care about val2 for these classes
        if val1.dtype.kind not in ('S', 'U'):
            raise TypeError('Input values for {0} class must be strings'
                            .format(self.name))
        return val1, None

    def parse_string(self, timestr, subfmts):
        """Read time from a single string, using a set of possible formats."""
        # Datetime components required for conversion to JD by ERFA, along
        # with the default values.
        components = ('year', 'mon', 'mday', 'hour', 'min', 'sec')
        defaults = (None, 1, 1, 0, 0, 0)
        # Assume that anything following "." on the right side is a
        # floating fraction of a second.
        try:
            idot = timestr.rindex('.')
        except Exception:
            fracsec = 0.0
        else:
            timestr, fracsec = timestr[:idot], timestr[idot:]
            fracsec = float(fracsec)

        for _, strptime_fmt_or_regex, _ in subfmts:
            if isinstance(strptime_fmt_or_regex, str):
                try:
                    tm = time.strptime(timestr, strptime_fmt_or_regex)
                except ValueError:
                    continue
                else:
                    vals = [getattr(tm, 'tm_' + component)
                            for component in components]

            else:
                tm = re.match(strptime_fmt_or_regex, timestr)
                if tm is None:
                    continue
                tm = tm.groupdict()
                vals = [int(tm.get(component, default)) for component, default
                        in zip(components, defaults)]

            # Add fractional seconds
            vals[-1] = vals[-1] + fracsec
            return vals
        else:
            raise ValueError('Time {0} does not match {1} format'
                             .format(timestr, self.name))

    def set_jds(self, val1, val2):
        """Parse the time strings contained in val1 and set jd1, jd2"""
        # Select subformats based on current self.in_subfmt
        subfmts = self._select_subfmts(self.in_subfmt)
        # Be liberal in what we accept: convert bytes to ascii.
        # Here .item() is needed for arrays with entries of unequal length,
        # to strip trailing 0 bytes.
        to_string = (str if val1.dtype.kind == 'U' else
                     lambda x: str(x.item(), encoding='ascii'))
        iterator = np.nditer([val1, None, None, None, None, None, None],
                             op_dtypes=[val1.dtype] + 5*[np.intc] + [np.double])
        for val, iy, im, id, ihr, imin, dsec in iterator:
            val = to_string(val)
            iy[...], im[...], id[...], ihr[...], imin[...], dsec[...] = (
                self.parse_string(val, subfmts))

        jd1, jd2 = erfa.dtf2d(self.scale.upper().encode('ascii'),
                              *iterator.operands[1:])
        self.jd1, self.jd2 = day_frac(jd1, jd2)

    def str_kwargs(self):
        """
        Generator that yields a dict of values corresponding to the
        calendar date and time for the internal JD values.
        """
        scale = self.scale.upper().encode('ascii'),
        iys, ims, ids, ihmsfs = erfa.d2dtf(scale, self.precision,
                                           self.jd1, self.jd2_filled)

        # Get the str_fmt element of the first allowed output subformat
        _, _, str_fmt = self._select_subfmts(self.out_subfmt)[0]

        if '{yday:' in str_fmt:
            has_yday = True
        else:
            has_yday = False
            yday = None

        ihrs = ihmsfs['h']
        imins = ihmsfs['m']
        isecs = ihmsfs['s']
        ifracs = ihmsfs['f']
        for iy, im, id, ihr, imin, isec, ifracsec in np.nditer(
                [iys, ims, ids, ihrs, imins, isecs, ifracs]):
            if has_yday:
                yday = datetime.datetime(iy, im, id).timetuple().tm_yday

            yield {'year': int(iy), 'mon': int(im), 'day': int(id),
                   'hour': int(ihr), 'min': int(imin), 'sec': int(isec),
                   'fracsec': int(ifracsec), 'yday': yday}

    def format_string(self, str_fmt, **kwargs):
        """Write time to a string using a given format.

        By default, just interprets str_fmt as a format string,
        but subclasses can add to this.
        """
        return str_fmt.format(**kwargs)

    @property
    def value(self):
        # Select the first available subformat based on current
        # self.out_subfmt
        subfmts = self._select_subfmts(self.out_subfmt)
        _, _, str_fmt = subfmts[0]

        # TODO: fix this ugly hack
        if self.precision > 0 and str_fmt.endswith('{sec:02d}'):
            str_fmt += '.{fracsec:0' + str(self.precision) + 'd}'

        # Try to optimize this later.  Can't pre-allocate because length of
        # output could change, e.g. year rolls from 999 to 1000.
        outs = []
        for kwargs in self.str_kwargs():
            outs.append(str(self.format_string(str_fmt, **kwargs)))

        return np.array(outs).reshape(self.jd1.shape)

    def _select_subfmts(self, pattern):
        """
        Return a list of subformats where name matches ``pattern`` using
        fnmatch.
        """

        fnmatchcase = fnmatch.fnmatchcase
        subfmts = [x for x in self.subfmts if fnmatchcase(x[0], pattern)]
        if len(subfmts) == 0:
            raise ValueError('No subformats match {0}'.format(pattern))
        return subfmts


class TimeISO(TimeString):
    """
    ISO 8601 compliant date-time format "YYYY-MM-DD HH:MM:SS.sss...".
    For example, 2000-01-01 00:00:00.000 is midnight on January 1, 2000.

    The allowed subformats are:

    - 'date_hms': date + hours, mins, secs (and optional fractional secs)
    - 'date_hm': date + hours, mins
    - 'date': date
    """

    name = 'iso'
    subfmts = (('date_hms',
                '%Y-%m-%d %H:%M:%S',
                # XXX To Do - use strftime for output ??
                '{year:d}-{mon:02d}-{day:02d} {hour:02d}:{min:02d}:{sec:02d}'),
               ('date_hm',
                '%Y-%m-%d %H:%M',
                '{year:d}-{mon:02d}-{day:02d} {hour:02d}:{min:02d}'),
               ('date',
                '%Y-%m-%d',
                '{year:d}-{mon:02d}-{day:02d}'))

    def parse_string(self, timestr, subfmts):
        # Handle trailing 'Z' for UTC time
        if timestr.endswith('Z'):
            if self.scale != 'utc':
                raise ValueError("Time input terminating in 'Z' must have "
                                 "scale='UTC'")
            timestr = timestr[:-1]
        return super().parse_string(timestr, subfmts)


class TimeISOT(TimeISO):
    """
    ISO 8601 compliant date-time format "YYYY-MM-DDTHH:MM:SS.sss...".
    This is the same as TimeISO except for a "T" instead of space between
    the date and time.
    For example, 2000-01-01T00:00:00.000 is midnight on January 1, 2000.

    The allowed subformats are:

    - 'date_hms': date + hours, mins, secs (and optional fractional secs)
    - 'date_hm': date + hours, mins
    - 'date': date
    """

    name = 'isot'
    subfmts = (('date_hms',
                '%Y-%m-%dT%H:%M:%S',
                '{year:d}-{mon:02d}-{day:02d}T{hour:02d}:{min:02d}:{sec:02d}'),
               ('date_hm',
                '%Y-%m-%dT%H:%M',
                '{year:d}-{mon:02d}-{day:02d}T{hour:02d}:{min:02d}'),
               ('date',
                '%Y-%m-%d',
                '{year:d}-{mon:02d}-{day:02d}'))


class TimeYearDayTime(TimeISO):
    """
    Year, day-of-year and time as "YYYY:DOY:HH:MM:SS.sss...".
    The day-of-year (DOY) goes from 001 to 365 (366 in leap years).
    For example, 2000:001:00:00:00.000 is midnight on January 1, 2000.

    The allowed subformats are:

    - 'date_hms': date + hours, mins, secs (and optional fractional secs)
    - 'date_hm': date + hours, mins
    - 'date': date
    """

    name = 'yday'
    subfmts = (('date_hms',
                '%Y:%j:%H:%M:%S',
                '{year:d}:{yday:03d}:{hour:02d}:{min:02d}:{sec:02d}'),
               ('date_hm',
                '%Y:%j:%H:%M',
                '{year:d}:{yday:03d}:{hour:02d}:{min:02d}'),
               ('date',
                '%Y:%j',
                '{year:d}:{yday:03d}'))


class TimeDatetime64(TimeISOT):
    name = 'datetime64'

    def _check_val_type(self, val1, val2):
        # Note: don't care about val2 for this class`
        if not val1.dtype.kind == 'M':
            raise TypeError('Input values for {0} class must be '
                            'datetime64 objects'.format(self.name))
        return val1, None

    def set_jds(self, val1, val2):
        # If there are any masked values in the ``val1`` datetime64 array
        # ('NaT') then stub them with a valid date so downstream parse_string
        # will work.  The value under the mask is arbitrary but a "modern" date
        # is good.
        mask = np.isnat(val1)
        masked = np.any(mask)
        if masked:
            val1 = val1.copy()
            val1[mask] = '2000'

        # Make sure M(onth) and Y(ear) dates will parse and convert to bytestring
        if val1.dtype.name in ['datetime64[M]', 'datetime64[Y]']:
            val1 = val1.astype('datetime64[D]')
        val1 = val1.astype('S')

        # Standard ISO string parsing now
        super().set_jds(val1, val2)

        # Finally apply mask if necessary
        if masked:
            self.jd2[mask] = np.nan

    @property
    def value(self):
        precision = self.precision
        self.precision = 9
        ret = super().value
        self.precision = precision
        return ret.astype('datetime64')


class TimeFITS(TimeString):
    """
    FITS format: "[±Y]YYYY-MM-DD[THH:MM:SS[.sss]]".

    ISOT but can give signed five-digit year (mostly for negative years);

    The allowed subformats are:

    - 'date_hms': date + hours, mins, secs (and optional fractional secs)
    - 'date': date
    - 'longdate_hms': as 'date_hms', but with signed 5-digit year
    - 'longdate': as 'date', but with signed 5-digit year

    See Rots et al., 2015, A&A 574:A36 (arXiv:1409.7583).
    """
    name = 'fits'
    subfmts = (
        ('date_hms',
         (r'(?P<year>\d{4})-(?P<mon>\d\d)-(?P<mday>\d\d)T'
          r'(?P<hour>\d\d):(?P<min>\d\d):(?P<sec>\d\d(\.\d*)?)'),
         '{year:04d}-{mon:02d}-{day:02d}T{hour:02d}:{min:02d}:{sec:02d}'),
        ('date',
         r'(?P<year>\d{4})-(?P<mon>\d\d)-(?P<mday>\d\d)',
         '{year:04d}-{mon:02d}-{day:02d}'),
        ('longdate_hms',
         (r'(?P<year>[+-]\d{5})-(?P<mon>\d\d)-(?P<mday>\d\d)T'
          r'(?P<hour>\d\d):(?P<min>\d\d):(?P<sec>\d\d(\.\d*)?)'),
         '{year:+06d}-{mon:02d}-{day:02d}T{hour:02d}:{min:02d}:{sec:02d}'),
        ('longdate',
         r'(?P<year>[+-]\d{5})-(?P<mon>\d\d)-(?P<mday>\d\d)',
         '{year:+06d}-{mon:02d}-{day:02d}'))
    # Add the regex that parses the scale and possible realization.
    # Support for this is deprecated.  Read old style but no longer write
    # in this style.
    subfmts = tuple(
        (subfmt[0],
         subfmt[1] + r'(\((?P<scale>\w+)(\((?P<realization>\w+)\))?\))?',
         subfmt[2]) for subfmt in subfmts)

    def parse_string(self, timestr, subfmts):
        """Read time and deprecated scale if present"""
        # Try parsing with any of the allowed sub-formats.
        for _, regex, _ in subfmts:
            tm = re.match(regex, timestr)
            if tm:
                break
        else:
            raise ValueError('Time {0} does not match {1} format'
                             .format(timestr, self.name))
        tm = tm.groupdict()
        # Scale and realization are deprecated and strings in this form
        # are no longer created.  We issue a warning but still use the value.
        if tm['scale'] is not None:
            warnings.warn("FITS time strings should no longer have embedded time scale.",
                          AstropyDeprecationWarning)
            # If a scale was given, translate from a possible deprecated
            # timescale identifier to the scale used by Time.
            fits_scale = tm['scale'].upper()
            scale = FITS_DEPRECATED_SCALES.get(fits_scale, fits_scale.lower())
            if scale not in TIME_SCALES:
                raise ValueError("Scale {0!r} is not in the allowed scales {1}"
                                 .format(scale, sorted(TIME_SCALES)))
            # If no scale was given in the initialiser, set the scale to
            # that given in the string.  Realization is ignored
            # and is only supported to allow old-style strings to be
            # parsed.
            if self._scale is None:
                self._scale = scale
            if scale != self.scale:
                raise ValueError("Input strings for {0} class must all "
                                 "have consistent time scales."
                                 .format(self.name))
        return [int(tm['year']), int(tm['mon']), int(tm['mday']),
                int(tm.get('hour', 0)), int(tm.get('min', 0)),
                float(tm.get('sec', 0.))]

    @property
    def value(self):
        """Convert times to strings, using signed 5 digit if necessary."""
        if 'long' not in self.out_subfmt:
            # If we have times before year 0 or after year 9999, we can
            # output only in a "long" format, using signed 5-digit years.
            jd = self.jd1 + self.jd2
            if jd.min() < 1721425.5 or jd.max() >= 5373484.5:
                self.out_subfmt = 'long' + self.out_subfmt
        return super().value


class TimeEpochDate(TimeFormat):
    """
    Base class for support floating point Besselian and Julian epoch dates
    """
    _default_scale = 'tt'  # As of astropy 3.2, this is no longer 'utc'.

    def set_jds(self, val1, val2):
        self._check_scale(self._scale)  # validate scale.
        epoch_to_jd = getattr(erfa, self.epoch_to_jd)
        jd1, jd2 = epoch_to_jd(val1 + val2)
        self.jd1, self.jd2 = day_frac(jd1, jd2)

    @property
    def value(self):
        jd_to_epoch = getattr(erfa, self.jd_to_epoch)
        return jd_to_epoch(self.jd1, self.jd2)


class TimeBesselianEpoch(TimeEpochDate):
    """Besselian Epoch year as floating point value(s) like 1950.0"""
    name = 'byear'
    epoch_to_jd = 'epb2jd'
    jd_to_epoch = 'epb'

    def _check_val_type(self, val1, val2):
        """Input value validation, typically overridden by derived classes"""
        if hasattr(val1, 'to') and hasattr(val1, 'unit'):
            raise ValueError("Cannot use Quantities for 'byear' format, "
                             "as the interpretation would be ambiguous. "
                             "Use float with Besselian year instead. ")

        return super()._check_val_type(val1, val2)


class TimeJulianEpoch(TimeEpochDate):
    """Julian Epoch year as floating point value(s) like 2000.0"""
    name = 'jyear'
    unit = erfa.DJY  # 365.25, the Julian year, for conversion to quantities
    epoch_to_jd = 'epj2jd'
    jd_to_epoch = 'epj'


class TimeEpochDateString(TimeString):
    """
    Base class to support string Besselian and Julian epoch dates
    such as 'B1950.0' or 'J2000.0' respectively.
    """
    _default_scale = 'tt'  # As of astropy 3.2, this is no longer 'utc'.

    def set_jds(self, val1, val2):
        epoch_prefix = self.epoch_prefix
        # Be liberal in what we accept: convert bytes to ascii.
        to_string = (str if val1.dtype.kind == 'U' else
                     lambda x: str(x.item(), encoding='ascii'))
        iterator = np.nditer([val1, None], op_dtypes=[val1.dtype, np.double])
        for val, years in iterator:
            try:
                time_str = to_string(val)
                epoch_type, year_str = time_str[0], time_str[1:]
                year = float(year_str)
                if epoch_type.upper() != epoch_prefix:
                    raise ValueError
            except (IndexError, ValueError, UnicodeEncodeError):
                raise ValueError('Time {0} does not match {1} format'
                                 .format(time_str, self.name))
            else:
                years[...] = year

        self._check_scale(self._scale)  # validate scale.
        epoch_to_jd = getattr(erfa, self.epoch_to_jd)
        jd1, jd2 = epoch_to_jd(iterator.operands[-1])
        self.jd1, self.jd2 = day_frac(jd1, jd2)

    @property
    def value(self):
        jd_to_epoch = getattr(erfa, self.jd_to_epoch)
        years = jd_to_epoch(self.jd1, self.jd2)
        # Use old-style format since it is a factor of 2 faster
        str_fmt = self.epoch_prefix + '%.' + str(self.precision) + 'f'
        outs = [str_fmt % year for year in years.flat]
        return np.array(outs).reshape(self.jd1.shape)


class TimeBesselianEpochString(TimeEpochDateString):
    """Besselian Epoch year as string value(s) like 'B1950.0'"""
    name = 'byear_str'
    epoch_to_jd = 'epb2jd'
    jd_to_epoch = 'epb'
    epoch_prefix = 'B'


class TimeJulianEpochString(TimeEpochDateString):
    """Julian Epoch year as string value(s) like 'J2000.0'"""
    name = 'jyear_str'
    epoch_to_jd = 'epj2jd'
    jd_to_epoch = 'epj'
    epoch_prefix = 'J'


class TimeDeltaFormatMeta(TimeFormatMeta):
    _registry = TIME_DELTA_FORMATS


class TimeDeltaFormat(TimeFormat, metaclass=TimeDeltaFormatMeta):
    """Base class for time delta representations"""

    def _check_scale(self, scale):
        """
        Check that the scale is in the allowed list of scales, or is `None`
        """
        if scale is not None and scale not in TIME_DELTA_SCALES:
            raise ScaleValueError("Scale value '{0}' not in "
                                  "allowed values {1}"
                                  .format(scale, TIME_DELTA_SCALES))

        return scale

    def set_jds(self, val1, val2):
        self._check_scale(self._scale)  # Validate scale.
        self.jd1, self.jd2 = day_frac(val1, val2, divisor=1./self.unit)

    @property
    def value(self):
        return (self.jd1 + self.jd2) / self.unit


class TimeDeltaSec(TimeDeltaFormat):
    """Time delta in SI seconds"""
    name = 'sec'
    unit = 1. / erfa.DAYSEC  # for quantity input


class TimeDeltaJD(TimeDeltaFormat):
    """Time delta in Julian days (86400 SI seconds)"""
    name = 'jd'
    unit = 1.


class TimeDeltaDatetime(TimeDeltaFormat, TimeUnique):
    """Time delta in datetime.timedelta"""
    name = 'datetime'

    def _check_val_type(self, val1, val2):
        # Note: don't care about val2 for this class
        if not all(isinstance(val, datetime.timedelta) for val in val1.flat):
            raise TypeError('Input values for {0} class must be '
                            'datetime.timedelta objects'.format(self.name))
        return val1, None

    def set_jds(self, val1, val2):
        self._check_scale(self._scale)  # Validate scale.
        iterator = np.nditer([val1, None],
                             flags=['refs_ok'],
                             op_dtypes=[object] + [np.double])

        for val, sec in iterator:
            sec[...] = val.item().total_seconds()

        self.jd1, self.jd2 = day_frac(iterator.operands[-1], 0.0,
                                      divisor=erfa.DAYSEC)

    @property
    def value(self):
        iterator = np.nditer([self.jd1 + self.jd2, None],
                             flags=['refs_ok'],
                             op_dtypes=[self.jd1.dtype] + [object])

        for jd, out in iterator:
            out[...] = datetime.timedelta(days=jd.item())

        return self.mask_if_needed(iterator.operands[-1])


from .core import Time, TIME_SCALES, TIME_DELTA_SCALES, ScaleValueError
