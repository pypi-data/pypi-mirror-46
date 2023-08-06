from infi.pyutils.lazy import cached_function

import json
import time
import gevent
from io import StringIO

import logbook
logger = logbook.Logger(__name__, level=logbook.CRITICAL)  # by default don't log errors


class DecodeError(Exception):
    pass


class EncodeError(Exception):
    pass


class GreenletFriendlyStringIO(StringIO):
    """ A StringIO subclass that yields to other greenlets every ~0.01 secs """
    def __init__(self):
        StringIO.__init__(self)  # can't use super() since StringIO is an old-style class
        self.last_sleep = 0

    def write(self, s):
        StringIO.write(self, s.decode('utf8'))
        t = time.time()
        if t - self.last_sleep > 0.01:
            gevent.sleep(0)
            self.last_sleep = t


@cached_function
def can_dumps_sort_keys():
    from platform import python_version
    from pkg_resources import parse_version
    return parse_version(python_version()) >= parse_version("2.7.5")


def encode(python_object, indent=None, large_object=False):
    """:returns: a JSON-representation of the object"""
    # sorted keys is easier to read; however, Python-2.7.2 does not have this feature
    kwargs = dict(indent=indent)
    if can_dumps_sort_keys():
        kwargs.update(sort_keys=True)
    try:
        if large_object:
            out = GreenletFriendlyStringIO()
            json.dump(python_object, out, **kwargs)
            return out.getvalue()
        else:
            return json.dumps(python_object, **kwargs)
    except Exception:
        logger.exception()
        raise EncodeError('Cannot encode {!r}', python_object)


def decode(json_string):
    """:returns: a Python object"""
    try:
        return json.loads(json_string)
    except:
        raise DecodeError()
