import re
import time
import platform

from base64 import b64encode, b64decode
from urllib.parse import quote, unquote

from multidict import MultiDict

from . import __version__


USER_AGENT = (
    'grpc-python-grpclib/{lib_ver} ({sys}; {py}/{py_ver})'
    .format(
        lib_ver=__version__,
        sys=platform.system(),
        py=platform.python_implementation(),
        py_ver=platform.python_version(),
    )
    .lower()
)

_UNITS = {
    'H': 60 * 60,
    'M': 60,
    'S': 1,
    'm': 10 ** -3,
    'u': 10 ** -6,
    'n': 10 ** -9,
}

_TIMEOUT_RE = re.compile(r'^(\d+)([{}])$'.format(''.join(_UNITS)))


def decode_timeout(value):
    match = _TIMEOUT_RE.match(value)
    if match is None:
        raise ValueError('Invalid timeout: {}'.format(value))
    timeout, unit = match.groups()
    return int(timeout) * _UNITS[unit]


def encode_timeout(timeout: float) -> str:
    if timeout > 10:
        return '{}S'.format(int(timeout))
    elif timeout > 0.01:
        return '{}m'.format(int(timeout * 10 ** 3))
    elif timeout > 0.00001:
        return '{}u'.format(int(timeout * 10 ** 6))
    else:
        return '{}n'.format(int(timeout * 10 ** 9))


class Deadline:

    def __init__(self, *, _timestamp):
        self._timestamp = _timestamp

    def __lt__(self, other):
        if not isinstance(other, Deadline):
            raise TypeError('comparison is not supported between '
                            'instances of \'{}\' and \'{}\''
                            .format(type(self).__name__, type(other).__name__))
        return self._timestamp < other._timestamp

    def __eq__(self, other):
        if not isinstance(other, Deadline):
            return False
        return self._timestamp == other._timestamp

    @classmethod
    def from_headers(cls, headers):
        timeout = min(map(decode_timeout,
                          (v for k, v in headers if k == 'grpc-timeout')),
                      default=None)
        if timeout is not None:
            return cls.from_timeout(timeout)
        else:
            return None

    @classmethod
    def from_timeout(cls, timeout):
        return cls(_timestamp=time.monotonic() + timeout)

    def time_remaining(self):
        return max(0, self._timestamp - time.monotonic())


class Metadata(MultiDict):
    pass


_UNQUOTED = ''.join([chr(i) for i in range(0x20, 0x24 + 1)]
                    + [chr(i) for i in range(0x26, 0x7E + 1)])


def encode_grpc_message(message: str) -> str:
    return quote(message, safe=_UNQUOTED, encoding='utf-8')


def decode_grpc_message(value: str) -> str:
    return unquote(value, encoding='utf-8', errors='replace')


_KEY_RE = re.compile(r'^[0-9a-z_.\-]+$')
_VALUE_RE = re.compile(r'^[ !-~]+$')  # 0x20-0x7E - space and printable ASCII
_SPECIAL = {
    'te',
    'content-type',
    'user-agent',
}


def decode_metadata(headers):
    metadata = Metadata()
    for key, value in headers:
        if key.startswith((':', 'grpc-')) or key in _SPECIAL:
            continue
        elif key.endswith('-bin'):
            metadata.add(key, b64decode(value.encode('ascii')
                                        + (b'=' * (len(value) % 4))))
        else:
            metadata.add(key, value)
    return metadata


def encode_metadata(metadata):
    if hasattr(metadata, 'items'):
        metadata = metadata.items()
    result = []
    for key, value in metadata:
        if key in _SPECIAL or key.startswith('grpc-') or not _KEY_RE.match(key):
            raise ValueError('Invalid metadata key: {!r}'.format(key))
        if key.endswith('-bin'):
            if not isinstance(value, bytes):
                raise TypeError('Invalid metadata value type, bytes expected: '
                                '{!r}'.format(value))
            result.append((key, b64encode(value).rstrip(b'=').decode('ascii')))
        else:
            if not isinstance(value, str):
                raise TypeError('Invalid metadata value type, str expected: '
                                '{!r}'.format(value))
            if not _VALUE_RE.match(value):
                raise ValueError('Invalid metadata value: {!r}'.format(value))
            result.append((key, value))
    return result
