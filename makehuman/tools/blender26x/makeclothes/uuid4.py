"""
UUID4 generator that does not rely on ctypes.

This file contains parts from the python standard library uuid module.
__author__ = 'Ka-Ping Yee <ping@zesty.ca>'
"""

def uuid4():
    """Generate a random UUID."""

    # Avoid use of ctypes, get randomness from urandom or the 'random' module.
    try:
        import os
        return UUID4(bytes=os.urandom(16))
    except:
        import random
        bytes = [chr(random.randrange(256)) for i in range(16)]
        return UUID4(bytes=bytes)

class UUID4(object):
    """Instances of the UUID4 class represent UUIDs version 4 as specified in RFC 4122."""

    def __init__(self, bytes):

        if len(bytes) != 16:
            raise ValueError('bytes is not a 16-char string')
        int = long(('%02x'*16) % tuple(map(ord, bytes)), 16)

        version = 4
        # Set the variant to RFC 4122.
        int &= ~(0xc000 << 48L)
        int |= 0x8000 << 48L
        # Set the version number.
        int &= ~(0xf000 << 64L)
        int |= version << 76L
        self.__dict__['int'] = int

    def __repr__(self):
        return 'UUID4(%r)' % str(self)

    def __str__(self):
        hex = '%032x' % self.int
        return '%s-%s-%s-%s-%s' % (
            hex[:8], hex[8:12], hex[12:16], hex[16:20], hex[20:])

