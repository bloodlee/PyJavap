__author__ = 'jasonlee'

from PyJavapInternal import doFlagToStr

ACC_PUBLIC = 0x0001
ACC_PRIVATE = 0x0002
ACC_PROTECTED = 0x0004
ACC_STATIC = 0x0008
ACC_FINAL  = 0x0010
ACC_SYNCHRONIZED = 0x0020
ACC_BRIDGE = 0x0040
ACC_VARARGS = 0x0080
ACC_NATIVE = 0x0100
ACC_ABSTRACT = 0x0400
ACC_STRICT = 0x0800
ACC_SYNTHETIC = 0x1000

__flagToName = {
    ACC_PUBLIC: 'public',
    ACC_PRIVATE: 'private',
    ACC_PROTECTED: 'protected',
    ACC_STATIC: 'static',
    ACC_FINAL: 'final',
    ACC_SYNCHRONIZED: 'synchronized',
    ACC_BRIDGE: 'volatile',
    ACC_VARARGS: 'varargs',
    ACC_NATIVE: 'native',
    ACC_ABSTRACT: 'abstract',
    ACC_STRICT: 'strict',
    ACC_SYNTHETIC: 'synthetic',
}

def flagToStr(flag):
    """
    Return the string of flag
    """
    return doFlagToStr(flag, __flagToName)