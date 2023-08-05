"""
Python implementation of the TIIP (Thin Industrial Internet Protocol) protocol.
"""

import json

from datetime import datetime as dt
from datetime import timedelta as td

import dateutil.parser as parser

# Python3 compability fixes
import sys

PY3 = sys.version_info > (3,)
if PY3:
    long = int
    unicode = str
else:
    # noinspection PyShadowingBuiltins
    bytes = str

__version__ = 'tiip.3.0'  # TIIP protocol version


class TIIPMessage(object):
    # noinspection PyShadowingBuiltins
    def __init__(
            self, tiipStr=None, tiipDict=None, ts=None, lat=None, mid=None, sid=None, type=None,
            src=None, targ=None, sig=None, ch=None, arg=None, pl=None, ok=None,
            ten=None, verifyVersion=True):
        """
        @param tiipStr: A string representation of a TIIPMessage to load on init
        @param tiipDict: A dictionary representation of a TIIPMessage to load on init
        @raise: TypeError, ValueError
        All other arguments are keys to set in the TIIPMessage, see TIIP specification for more details:
            https://github.com/whitelizard/tiip
        """
        # Protocol keys
        self.__pv = __version__
        self.__ts = self.getTimeStamp()
        self.__lat = None
        self.__mid = None
        self.__sid = None
        self.__type = None
        self.__src = None
        self.__targ = None
        self.__sig = None
        self.__ch = None
        self.__arg = None
        self.__pl = None
        self.__ok = None
        self.__ten = None

        # Parse constructor arguments
        if tiipStr is not None:
            self.loadFromStr(tiipStr, verifyVersion)
        if tiipDict is not None:
            self.loadFromDict(tiipDict, verifyVersion)
        if ts is not None:
            self.ts = ts
        if lat is not None:
            self.lat = lat
        if mid is not None:
            self.mid = mid
        if sid is not None:
            self.sid = sid
        if type is not None:
            self.type = type
        if src is not None:
            self.src = src
        if targ is not None:
            self.targ = targ
        if sig is not None:
            self.sig = sig
        if ch is not None:
            self.ch = ch
        if arg is not None:
            self.arg = arg
        if pl is not None:
            self.pl = pl
        if ok is not None:
            self.ok = ok
        if ten is not None:
            self.ten = ten

    def __str__(self):
        return json.dumps(dict(self))

    def __iter__(self):
        yield 'pv', self.__pv
        yield 'ts', self.__ts
        if self.__lat is not None:
            yield 'lat', self.__lat
        if self.__mid is not None:
            yield 'mid', self.__mid
        if self.__sid is not None:
            yield 'sid', self.__sid
        if self.__type is not None:
            yield 'type', self.__type
        if self.__src is not None:
            yield 'src', self.__src
        if self.__targ is not None:
            yield 'targ', self.__targ
        if self.__sig is not None:
            yield 'sig', self.__sig
        if self.__ch is not None:
            yield 'ch', self.__ch
        if self.__arg is not None:
            yield 'arg', self.__arg
        if self.__pl is not None:
            yield 'pl', self.__pl
        if self.__ok is not None:
            yield 'ok', self.__ok
        if self.__ten is not None:
            yield 'ten', self.__ten

    @staticmethod
    def getTimeStamp():
        """
        Creates a timestamp string representation according to the TIIP-specification for timestamps.
        @return:
        """
        return dt.utcnow().isoformat(timespec='microseconds') + 'Z'

    @property
    def pv(self):
        return self.__pv

    @property
    def ts(self):
        return self.__ts

    @ts.setter
    def ts(self, value):
        if isinstance(value, str) or isinstance(value, unicode) or isinstance(value, bytes):
            try:
                dateObj = parser.parse(value)
            except ValueError:
                raise ValueError('timestamp string must be parseable to datetime')
            if dateObj.utcoffset() not in [None, td(0)]:
                raise ValueError('timestamp string must be in utc timezone')
            if value[-1] != 'Z' or value[19] != '.':
                raise ValueError('seconds must be decimals and end with Z')
            self.__ts = value
        elif isinstance(value, dt):
            if value.utcoffset() not in [None, td(0)]:
                raise ValueError('timestamp string must be in utc timezone')
            iso = value.isoformat(timespec='microseconds')
            if iso.endswith("+00:00"):
                iso = iso[:-6]
            self.__ts = iso + 'Z'
        else:
            raise TypeError('timestamp can only be of types datetime or a valid unicode or string representation of a iso 6801')

    @property
    def lat(self):
        return self.__lat

    @lat.setter
    def lat(self, value):
        if value is None:
            self.__lat = None
        elif isinstance(value, str) or isinstance(value, unicode) or isinstance(value, bytes):
            try:
                float(value)  # Check if string is float representation
            except ValueError:
                raise ValueError('Latency string must be parseable to float')
            else:
                self.__lat = value
        elif isinstance(value, (int, float, long)):
            self.__lat = repr(round(value, 6))
        else:
            raise TypeError('Latency can only be of types None, float, int, long or a valid unicode or string representation of a float')

    @property
    def mid(self):
        return self.__mid

    @mid.setter
    def mid(self, value):
        if value is None:
            self.__mid = None
        elif isinstance(value, str) or isinstance(value, unicode) or isinstance(value, bytes):
            self.__mid = value
        else:
            raise TypeError('mid can only be of types unicode, str or None')

    @property
    def sid(self):
        return self.__sid

    @sid.setter
    def sid(self, value):
        if value is None:
            self.__sid = None
        elif isinstance(value, str) or isinstance(value, unicode) or isinstance(value, bytes):
            self.__sid = value
        else:
            raise TypeError('sid can only be of types unicode, str or None')

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, value):
        if value is None:
            self.__type = None
        elif isinstance(value, str) or isinstance(value, unicode) or isinstance(value, bytes):
            self.__type = value
        else:
            raise TypeError('type can only be of types unicode, str or None')

    @property
    def src(self):
        return self.__src

    @src.setter
    def src(self, value):
        if value is None:
            self.__src = None
        elif isinstance(value, list):
            self.__src = value
        else:
            raise TypeError('source can only be of types list or None')

    @property
    def targ(self):
        return self.__targ

    @targ.setter
    def targ(self, value):
        if value is None:
            self.__targ = None
        elif isinstance(value, list):
            self.__targ = value
        else:
            raise TypeError('target can only be of types list or None')

    @property
    def sig(self):
        return self.__sig

    @sig.setter
    def sig(self, value):
        if value is None:
            self.__sig = None
        elif isinstance(value, str) or isinstance(value, unicode) or isinstance(value, bytes):
            self.__sig = value
        else:
            raise TypeError('signal can only be of types unicode, str or None')

    @property
    def ch(self):
        return self.__ch

    @ch.setter
    def ch(self, value):
        if value is None:
            self.__ch = None
        elif isinstance(value, str) or isinstance(value, unicode) or isinstance(value, bytes):
            self.__ch = value
        else:
            raise TypeError('channel can only be of types unicode, str or None')

    @property
    def arg(self):
        return self.__arg

    @arg.setter
    def arg(self, value):
        if value is None:
            self.__arg = None
        elif isinstance(value, dict):
            self.__arg = value
        else:
            raise TypeError('arguments can only be of types dict or None')

    @property
    def pl(self):
        return self.__pl

    @pl.setter
    def pl(self, value):
        if value is None:
            self.__pl = None
        elif isinstance(value, list):
            self.__pl = value
        else:
            raise TypeError('payload can only be of types list or None')

    @property
    def ok(self):
        return self.__ok

    @ok.setter
    def ok(self, value):
        if value is None:
            self.__ok = None
        elif isinstance(value, bool):
            self.__ok = value
        else:
            raise TypeError('ok can only be of types bool or None')

    @property
    def ten(self):
        return self.__ten

    @ten.setter
    def ten(self, value):
        if value is None:
            self.__ten = None
        elif isinstance(value, str) or isinstance(value, unicode) or isinstance(value, bytes):
            self.__ten = value
        else:
            raise TypeError('tenant can only be of types unicode, str or None')

    def loadFromStr(self, tiipStr, verifyVersion=True):
        """
        Loads this object with values from a string or unicode representation of a TIIPMessage.
        @param tiipStr: The string to load properties from.
        @param verifyVersion: True to verify that tiipDict has the right protocol
        @raise: TypeError, ValueError
        @return: None
        """
        tiipDict = json.loads(tiipStr)
        self.loadFromDict(tiipDict, verifyVersion)

    def loadFromDict(self, tiipDict, verifyVersion=True):
        """
        Loads this object with values from a dictionary representation of a TIIPMessage.
        @param tiipDict: The dictionary to load properties from.
        @param verifyVersion: True to verify that tiipDict has the right protocol
        @raise: TypeError, ValueError
        @return: None
        """

        if verifyVersion:
            if 'pv' not in tiipDict or tiipDict['pv'] != self.__pv:
                raise ValueError('Incorrect tiip version "' + str(tiipDict['pv']) + '" expected "' + self.__pv + '"')

        if 'pv' not in tiipDict or tiipDict['pv'] != self.__pv:
            if tiipDict['pv'] == "tiip.2.0":
                if 'ct' in tiipDict:
                    ct = float(tiipDict['ct'])
                    ts = float(tiipDict['ts'])
                    tiipDict['ts'] = str(ct)
                    tiipDict['lat'] = str(ts - ct)
                tiipDict['ts'] = dt.utcfromtimestamp(float(tiipDict['ts'])).isoformat(timespec='microseconds') + 'Z'

        if 'ts' in tiipDict:
            self.ts = tiipDict['ts']
        if 'lat' in tiipDict:
            self.lat = tiipDict['lat']
        if 'mid' in tiipDict:
            self.mid = tiipDict['mid']
        if 'sid' in tiipDict:
            self.sid = tiipDict['sid']
        if 'type' in tiipDict:
            self.type = tiipDict['type']
        if 'src' in tiipDict:
            self.src = tiipDict['src']
        if 'targ' in tiipDict:
            self.targ = tiipDict['targ']
        if 'sig' in tiipDict:
            self.sig = tiipDict['sig']
        if 'ch' in tiipDict:
            self.ch = tiipDict['ch']
        if 'arg' in tiipDict:
            self.arg = tiipDict['arg']
        if 'pl' in tiipDict:
            self.pl = tiipDict['pl']
        if 'ok' in tiipDict:
            self.ok = tiipDict['ok']
        if 'ten' in tiipDict:
            self.ten = tiipDict['ten']

    def asVersion(self, version):
        if version == self.__pv:
            return str(self)
        elif version == "tiip.2.0":
            tiipDict = {}
            for key, val in self:
                tiipDict[key] = val
            if "lat" in tiipDict:
                ct = parser.parse(tiipDict["ts"]).timestamp()
                tiipDict["ct"] = str(ct)
                tiipDict["ts"] = str(ct + float(tiipDict["lat"]))
                tiipDict.pop("lat")
            else:
                tiipDict["ts"] = str(parser.parse(tiipDict["ts"]).timestamp())
            tiipDict["pv"] = version
            return json.dumps(tiipDict)
        else:
            raise ValueError('Incorrect tiip version. Can only handle versions: tiip.2.0 and tiip.3.0')
