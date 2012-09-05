__author__ = 'yli'

class ByteCode(object):

    def __init__(self, byteCode, mnemonic, opCodeCount=0):
        self.byteCode = byteCode
        self.mnemonic = mnemonic
        self.opCodeCount = opCodeCount

    def getByteCode(self):
        return self.byteCode

    def getMnemonic(self):
        return self.mnemonic

    def getOpCodeCount(self):
        return self.opCodeCount

    def __eq__(self, other):
        return self.byteCode == other.byteCode

    def __str__(self):
        return "%s(0x%x)" % (self.mnemonic, self.byteCode)


allByteCodes = [
    ByteCode(0x32, 'aaload'),
    ByteCode(0x53, 'aastore'),
    ByteCode(0x01, 'aconst_null'),
    ByteCode(0x19, 'aload', 1),
    ByteCode(0x2a, 'aload_0'),
    ByteCode(0x2b, 'aload_1'),
    ByteCode(0x2c, 'aload_2'),
    ByteCode(0x3d, 'aload_3'),
    ByteCode(0xdb, 'anewarray', 2),
    ByteCode(0xb0, 'areturn'),
    ByteCode(0xbe, 'arraylength'),
    ByteCode(0x3a, 'astore', 1),
    ByteCode(0x4b, 'astore_0'),
    ByteCode(0x4c, 'astore_1'),
    ByteCode(0x4d, 'astore_2'),
    ByteCode(0x4e, 'astore_3'),
    ByteCode(0xbf, 'athrow'),

    ByteCode(0x33, 'baload'),
    ByteCode(0x54, 'bastore'),
    ByteCode(0x10, 'bipush'),

    ByteCode(0x34, 'caload'),
    ByteCode(0x55, 'castore'),
    ByteCode(0xc0, 'checkcast', 2),
]