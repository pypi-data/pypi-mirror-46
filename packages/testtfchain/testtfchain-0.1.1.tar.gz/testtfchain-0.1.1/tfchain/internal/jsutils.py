import re
import random
from datetime import datetime, timedelta
import time
from functools import reduce
import traceback
import struct
import json
import urllib
from hashlib import blake2b

# Copied and Modified from Jumpscale
# TODO: Remove

def blake2(s, digest_size=32):
    if isinstance(s, str): # check string direct otherwise have to pass in j
        s = s.encode()
    return blake2b(s,digest_size=digest_size).digest()

def blake2_string(s, digest_size=32):
    return blake2(s, digest_size=digest_size).hex()

def generateRandomInt(fromInt, toInt):
    return random.randint(fromInt, toInt)


def generateXCharID(x):
    r = "1234567890abcdefghijklmnopqrstuvwxyz"
    l = len(r)
    out = ""
    for _ in range(0, x):
        p = generateRandomInt(0, l - 1)
        out += r[p]
    return out


def generateXByteID(x):
    out = bytearray()
    for _ in range(0, x):
        out.append(generateRandomInt(0, 255))
    return out


# TIME
""" Timestamp routines """

LASTTIME = 0
DELTATIME_INITIALIZED = False


class TimeInterval:
    """ Enumerator for time interval units """

    NANOSECONDS = -3
    MICROSECONDS = -2
    MILLISECONDS = -1
    SECONDS = 0
    MINUTES = 1
    HOURS = 2
    DAYS = 3
    WEEKS = 4
    MONTHS = 5
    YEARS = 6


def printdelta():
    """
    This is a function for source code or performance debugging.
    Call this function at every point cut in the source code
    where you want to print out a timestamp, together with the source code line
    """

    global LASTTIME, DELTATIME_INITIALIZED
    currenttime = time.time()
    if DELTATIME_INITIALIZED:
        print(("... TIME DELTA: " + str(currenttime - LASTTIME)))
        LASTTIME = currenttime
    else:
        print("... STARTING TIME MEASUREMENTS")
        LASTTIME = currenttime
        DELTATIME_INITIALIZED = True
    print((" @ Source file [" +
           traceback.extract_stack()[-2][0] +
           "] line [" +
           str(traceback.extract_stack()[-2][1]) +
           "]"))


def getabstime():
    """ Get string representation of absolute time in milliseconds """
    x = time.time()
    part1 = time.strftime("%a %d %b %Y, %H:%M:%S", time.localtime(x))
    part2 = ".%03d" % ((x % 1) * 1000)
    return part1 + part2


TIMES = {'s': 1,
         'm': 60,
         'h': 3600,
         'd': 3600 * 24,
         'w': 3600 * 24 * 7,
         'M': int(3600 * 24 * 365 / 12),
         'Y': 3600 * 24 * 365,
         }


class Time_(object):
    """
    generic provider of time functions
    """

    def __init__(self):
        self.timeinterval = TimeInterval()

    @property
    def epoch(self):
        """
        jstime.epoch
        """

        return int(time.time())

    def getTimeEpoch(self):
        '''
        Get epoch timestamp (number of seconds passed since January 1, 1970)
        '''
        timestamp = int(time.time())
        return timestamp

    def getSecondsInHR(self, seconds):
        """
        jstime.getSecondsInHR(365)
        """
        minute = 60.
        hour = 3600.
        day = hour * 24
        week = day * 7
        if seconds < minute:
            return "%s seconds" % seconds
        elif seconds < hour:
            return "%s minutes" % round((seconds / minute), 1)
        elif seconds < day:
            return "%s hours" % round((seconds / hour), 1)
        elif seconds < week:
            return "%s days" % round((seconds / day), 1)
        else:
            return "%s weeks" % round((seconds / week), 1)

    def getTimeEpochBin(self):
        '''
        Get epoch timestamp (number of seconds passed since January 1, 1970) in binary format of 4 bytes
        '''
        return struct.pack("<I", self.getTimeEpoch())

    def getLocalTimeHR(self):
        '''
        Get the current local date and time in a human-readable form

        jstime.getLocalTimeHR()
        '''
        #timestamp = time.asctime(time.localtime(time.time()))
        timestr = self.formatTime(self.getTimeEpoch())
        return timestr

    def getLocalTimeHRForFilesystem(self):
        # TODO: check if correct implementation
        return time.strftime("%d_%b_%Y_%H_%M_%S", time.gmtime())

    def formatTime(self, epoch, formatstr='%Y/%m/%d %H:%M:%S', local=True):
        '''
        Returns a formatted time string representing the current time

        See http://docs.python.org/lib/module-time.html#l2h-2826 for an
        overview of available formatting options.

        @param format: Format string
        @type format: string

        @returns: Formatted current time
        @rtype: string
        '''
        epoch = float(epoch)
        if local:
            timetuple = time.localtime(epoch)
        else:
            timetuple = time.gmtime(epoch)
        timestr = time.strftime(formatstr, timetuple)
        return timestr

    def epoch2HRDate(self, epoch, local=True):
        return self.formatTime(epoch, '%Y/%m/%d', local)

    def epoch2HRDateTime(self, epoch, local=True):
        return self.formatTime(epoch, '%Y/%m/%d %H:%M:%S', local)

    def pythonDateTime2HRDateTime(self, pythonDateTime, local=True):
        if not isinstance(pythonDateTime, datetime.datetime):
            raise ValueError(
                "needs to be python date.time obj:%s" % pythonDateTime)
        epoch = pythonDateTime.timestamp()
        return self.epoch2HRDateTime(epoch)

    def pythonDateTime2Epoch(self, pythonDateTime, local=True):
        if not isinstance(pythonDateTime, datetime.datetime):
            raise ValueError(
                "needs to be python date.time obj:%s" % pythonDateTime)

        epoch = pythonDateTime.timestamp()
        return epoch

    def epoch2pythonDateTime(self, epoch):
        return datetime.datetime.fromtimestamp(epoch)

    def epoch2ISODateTime(self, epoch):
        dt = datetime.datetime.fromtimestamp(epoch)
        return dt.isoformat()

    def epoch2pythonDate(self, epoch):
        return datetime.date.fromtimestamp(epoch)

    def epoch2HRTime(self, epoch, local=True):
        return self.formatTime(epoch, '%H:%M:%S', local)

    def getMinuteId(self, epoch=None):
        """
        is # min from jan 1 2010
        """
        if epoch is None:
            epoch = time.time()
        if epoch < 1262318400.0:
            raise RuntimeError(
                "epoch cannot be smaller than 1262318400, given epoch:%s" % epoch)

        return int((epoch - 1262318400.0) / 60.0)

    def getHourId(self, epoch=None):
        """
        is # hour from jan 1 2010
        """
        return int(self.getMinuteId(epoch) / 60)

    def fiveMinuteIdToEpoch(self, fiveMinuteId):
        return fiveMinuteId * 60 * 5 + 1262318400

    def get5MinuteId(self, epoch=None):
        """
        is # 5 min from jan 1 2010
        """
        return int(self.getMinuteId(epoch) / 5)

    def getDayId(self, epoch=None):
        """
        is # day from jan 1 2010
        """
        return int(self.getMinuteId(epoch) / (60 * 24))

    def getDeltaTime(self, txt):
        """
        only supported now is -3m, -3d and -3h (ofcourse 3 can be any int)
        and an int which would be just be returned
        means 3 days ago 3 hours ago
        if 0 or '' then is now
        """
        txt = txt.strip()
        unit = txt[-1]
        if txt[-1] not in list(TIMES.keys()):
            raise RuntimeError(
                "Cannot find time, needs to be in format have time indicator %s " %
                list(
                    TIMES.keys()))
        value = float(txt[:-1])
        return int(value * TIMES[unit])

    def getEpochDeltaTime(self, txt):
        """
        only supported now is + and -3m, -3d and -3h  (ofcourse 3 can be any int)
        and an int which would be just be returned
        means 3 days ago 3 hours ago
        if 0 or '' then is now

        supported:

            s (second) ,m (min) ,h (hour) ,d (day),w (week), M (month), Y (year)

        """
        if txt is None or str(txt).strip() == "0":
            return self.getTimeEpoch()
        return self.getTimeEpoch() + self.getDeltaTime(txt)

    def HRDateToEpoch(self, datestr, local=True):
        """
        convert string date to epoch
        Date needs to be formatted as 1988/06/16  (Y/m/d)
        """
        if datestr.strip() == "":
            return 0
        try:
            datestr = datestr.strip()
            return time.mktime(time.strptime(datestr, "%Y/%m/%d"))
        except BaseException:
            raise ValueError(
                "Date needs to be formatted as \" 1988/06/16\", also check if date is valid, now format = %s" %
                datestr)

    def HRDateTime2epoch(self, hrdatetime):
        """
        convert string date/time to epoch
        Needs to be formatted as 16/06/1988 %H:%M:%S
        """
        if hrdatetime.strip() == "":
            return 0
        try:
            hrdatetime = hrdatetime.strip()
            return int(
                time.mktime(
                    time.strptime(
                        hrdatetime,
                        "%Y/%m/%d %H:%M:%S")))
        except BaseException:
            raise ValueError(
                "Date needs to be formatted as Needs to be formatted as 16/06/1988 %H:%M:%S, also check if date is valid, now format = {}".format(
                hrdatetime))

    def any2epoch(self, val, in_list=False):
        """
        if list will go item by item until not empty,0 or None
        if int is epoch
        if string is human readable format
        if date.time yeh ...
        """
        if isinstance(val, list):
            for item in val:
                res = self.any2epoch(item, in_list=True)
                if res != 0:
                    return res
            return 0
        if val is None:
            return 0
        if isinstance(val, int)(val):
            return val
        if isinstance(val, str)(val):
            try:
                return self.HRDateTime2epoch(val)
            except BaseException:
                pass
            try:
                return self.HRDateToEpoch(val)
            except BaseException:
                pass
        if isinstance(val, datetime.datetime):
            return self.pythonDateTime2Epoch(val)
        if not in_list:
            raise ValueError(
                "Could not define format of time value, needs to be int, human readable time, list or python datetime obj.")
        else:
            return 0

    def any2HRDateTime(self, val):
        """
        if list will go item by item until not empty,0 or None
        if int is epoch
        if string is human readable format
        if date.time yeh ...
        """
        epoch = self.any2epoch(val)
        return self.epoch2HRDateTime(epoch)

    def test(self):
        now = self.getTimeEpoch()
        hr = self.epoch2HRDateTime(now)
        assert self.HRDateTime2epoch(hr) == now
        assert self.any2epoch(hr) == now
        dt = self.epoch2pythonDateTime(now)
        assert self.any2epoch(dt) == now
        hr = self.pythonDateTime2HRDateTime(dt)
        assert self.any2epoch(hr) == now
        hr = self.any2HRDateTime(now)
        assert self.any2epoch(hr) == now
        hr = self.any2HRDateTime(hr)
        assert self.any2epoch(hr) == now
        hr = self.any2HRDateTime(dt)
        assert self.any2epoch(hr) == now
        hr = self.any2HRDateTime(["", 0, dt])
        assert self.any2epoch(hr) == now

def epoch2HRDateTime(epoch, local=True):
    return Time_().epoch2HRDateTime(epoch, local=local)

# FIXME: convert to static methods
class Duration:
    '''
    internal representation is an int (seconds)
    '''
    NAME = 'duration'

    def __init__(self, default=None):
        # inspired by https://stackoverflow.com/a/51916936
        self._RE = re.compile(
            r'^((?P<days>[\.\d]+?)d)?((?P<hours>[\.\d]+?)h)?((?P<minutes>[\.\d]+?)m)?((?P<seconds>[\.\d]+?)s)?$')
        self.BASETYPE = "int"
        self.NOCHECK = True
        self._default = default

    def get_default(self):
        return 0

    def python_code_get(self, value):
        """
        produce the python code which represents this value
        """
        return self.clean(value)

    def check(self, value):
        '''
        Check whether provided value is a valid duration representation
        be carefull is SLOW
        '''
        try:
            self.clean(value)
            return True
        except:
            return False

    def fromString(self, txt):
        return self.clean(txt)

    def toString(self, val):
        val = self.clean(val)
        if val == 0:
            return ""
        days = val//86400
        hours = (val - days*86400)//3600
        minutes = (val - days*86400 - hours*3600)//60
        seconds = val - days*86400 - hours*3600 - minutes*60
        return reduce(
            (lambda r, p: r+str(p[0])+p[1] if p[0] > 0 else r),
            [(days, "d"), (hours, "h"), (minutes, "m"), (seconds, "s")], "")

    def toHR(self, v):
        return self.toString(v)

    def clean(self, v):
        """
        support following formats:
        - None, 0: means undefined date
        - seconds = int
        - 1 (seconds)
        - 1s (seconds)
        - 2m (minutes)
        - 3h (hours)
        - 4d (days)
        - 1d4h2m3s (can also combine multiple, has to be from biggest to smallest and each unit has to be unique (e.g. cannot have 2 times hour specified))
        will return seconds
        """
        if v in [0, "0", None, ""]:
            return 0
        if isinstance(v, str):
            v = v.replace("'", "").replace("\"", "").strip()
            if v.isdigit():
                return int(v)  # shortcut for when string is an integer
            parts = self._RE.match(v)
            if parts is None:
                raise ValueError(
                    "Could not parse any time information from '{}'.  Examples of valid strings: '8h', '2d8h5m20s', '2m4s'".format(v))
            time_params = {name: float(
                param) for name, param in parts.groupdict().items() if param}
            return int(timedelta(**time_params).total_seconds())
        elif isinstance(v, int):
            return v
        else:
            raise ValueError(
                "Input needs to be string or int: {} ({})".format(v, type(v)))


duration = Duration()
jstime = Time_()

class DateTime:
    NAME =  'datetime,t'

    def __init__(self, default=None):

        self.BASETYPE = "int"
        self.NOCHECK = True
        self._default = default

    def default_get(self):
        if not self._default:
            self._default = 0
        return self._default

    def fromString(self, txt):
        return self.clean(txt)

    def toString(self, val, local=True):
        val = self.clean(val)
        if val == 0:
            return ""
        return jstime.epoch2HRDateTime(val, local=local)

    def toHR(self, v):
        return self.toString(v)

    def clean(self, v):
        """
        support following formats:
        - None, 0: means undefined date
        - epoch = int
        - month/day 22:50
        - month/day  (will be current year if specified this way)
        - year(4char)/month/day
        - year(4char)/month/day 10am:50
        - year(2char)/month/day
        - day/month/4char
        - year(4char)/month/day 22:50
        - +4h
        - -4h
        in stead of h also supported: s (second) ,m (min) ,h (hour) ,d (day),w (week), M (month), Y (year)
        will return epoch
        """
        if v is None:
            return self.default_get()
        def date_process(dd):
            if "/" not in dd:
                raise ValueError("date needs to have:/, now:%s" % v)
            splitted = dd.split("/")
            if len(splitted) == 2:
                dfstr = "%Y/%m/%d"
                dd = "%s/%s" % (jstime.epoch2HRDate(jstime.epoch).split("/")[0], dd.strip())
            elif len(splitted) == 3:
                s0 = splitted[0].strip()
                s1 = splitted[1].strip()
                s2 = splitted[2].strip()
                if len(s0) == 4 and (len(s1) == 2 or len(s1) == 1) and (len(s2) == 2 or len(s2) == 1):
                    # year in front
                    dfstr = "%Y/%m/%d"
                elif len(s2) == 4 and (len(s1) == 2 or len(s1) == 1) and (len(s0) == 2 or len(s0) == 1):
                    # year at end
                    dfstr = "%d/%m/%Y"
                elif (len(s2) == 2 or len(s2) == 1) and (len(s1) == 2 or len(s1) == 1) and (len(s0) == 2 or len(s0) == 1):
                    # year at start but small
                    dfstr = "%y/%m/%d"
                else:
                    raise ValueError("date wrongly formatted, now:%s" % v)
            else:
                raise ValueError("date needs to have 2 or 3 /, now:%s" % v)
            return (dd, dfstr)

        def time_process(v):
            v = v.strip()
            if ":" not in v:
                return ("00:00:00", "%H:%M:%S")
            splitted = v.split(":")
            if len(splitted) == 2:
                if "am" in v.lower() or "pm" in v.lower():
                    fstr = "%I%p:%M"
                else:
                    fstr = "%H:%M"
            elif len(splitted) == 3:
                if "am" in v.lower() or "pm" in v.lower():
                    fstr = "%I%p:%M:%S"
                else:
                    fstr = "%H:%M:%S"
            return (v, fstr)
        
        if v is None:
            v=0

        if isinstance(v, str):
            v=v.replace("'","").replace("\"","").strip()
            if v.strip() in ["0", "",0]:
                return 0

            if "+" in v or "-" in v:
                return jstime.getEpochDeltaTime(v)

            if ":" in v:
                # have time inside the representation
                dd, tt = v.split(" ", 1)
                tt, tfstr = time_process(tt)
            else:
                tt, tfstr = time_process("")
                dd = v

            dd, dfstr = date_process(dd)

            fstr = dfstr + " " + tfstr
            hrdatetime = dd + " " + tt
            epoch = int(time.mktime(time.strptime(hrdatetime, fstr)))
            return epoch
        elif isinstance(v, int):
            return v
        else:
            raise ValueError("Input needs to be string:%s" % v)

    def capnp_schema_get(self, name, nr):
        return "%s @%s :UInt32;" % (name, nr)

    def test(self):
        """
        js_shell 'jsdatetime.test()'
        """


class Date(DateTime):
    '''
    internal representation is an epoch (int)
    '''
    NAME =  'date,d'

    def __init__(self, default=None):

        self.BASETYPE = "int"
        # self._RE = re.compile('[0-9]{4}/[0-9]{2}/[0-9]{2}')
        self.NOCHECK = True
        self._default = default

    def clean(self, v):
        """
        support following formats:
        - 0: means undefined date
        - epoch = int  (will round to start of the day = 00h)
        - month/day  (will be current year if specified this way)
        - year(4char)/month/day
        - year(2char)/month/day
        - day/month/4char
        - +4M
        - -4Y
        in stead of h also supported: s (second) ,m (min) ,h (hour) ,d (day),w (week), M (month), Y (year)
        will return epoch
        """
        if v is None:
            return self.default_get()
        if isinstance(v,str):
            v=v.replace("'","").replace("\"","").strip()
        if v in [0,"0",None,""]:
            return 0
        # am sure there are better ways how to do this but goes to beginning of day
        v2 = DateTime.clean(self,v)
        dt = datetime.fromtimestamp(v2)
        dt2 = datetime(dt.year,dt.month,dt.day,0,0)
        return int(dt2.strftime('%s'))

    def toString(self, val, local=True):
        val = self.clean(val)
        if val == 0:
            return ""
        return jstime.epoch2HRDate(val, local=local)


jsdate = Date()
jsdatetime = DateTime()

class BytesEncoder(json.JSONEncoder):
    ENCODING = 'ascii'
    def default(self, obj):
        if isinstance(obj, bytes):
            return obj.decode(self.ENCODING)
        return json.JSONEncoder.default(self, obj)


class Encoder(object):
    @staticmethod
    def get(encoding='ascii'):
        kls = BytesEncoder
        kls.ENCODING = encoding
        return kls


def json_dumps(obj, sort_keys=False, indent=False, encoding='ascii'):
    return json.dumps(obj, ensure_ascii=False, sort_keys=sort_keys, indent=indent, cls=Encoder.get(encoding=encoding))


def json_loads(s):
    if isinstance(s, bytes):
        s = s.decode('utf-8')
    return json.loads(s)
