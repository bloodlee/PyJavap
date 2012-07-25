__author__ = 'jasonlee'

from PyJavapInternal import doFlagToStr

ACC_PUBLIC = 0x0001
ACC_FINAL  = 0x0010
ACC_SUPER  = 0x0020
ACC_INTERFACE = 0x0200
ACC_ABSTRACT = 0x0400
ACC_SYNTHETIC = 0x1000
ACC_ANNOTATION = 0x2000
ACC_ENUM = 0x4000

__flagToName = {
    ACC_PUBLIC: 'public',
    ACC_FINAL: 'final',
    ACC_SUPER: 'super',
    ACC_INTERFACE: 'interface',
    ACC_ABSTRACT: 'abstract',
    ACC_SYNTHETIC: 'synthetic',
    ACC_ANNOTATION: 'annotation',
    ACC_ENUM: 'enum',
    }

def flagToStr(flag):
    """
    Return the string of flag
    """

    return doFlagToStr(flag, __flagToName)