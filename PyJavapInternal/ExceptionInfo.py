__author__ = 'jason'

class ExceptionInfo(object):

    def __init__(self, startPC, endPC, handlerPC, exceptionClass):
        self.startPC = startPC
        self.endPC = endPC
        self.handlerPC = handlerPC
        self.exceptionClass = exceptionClass

    def __str__(self):
        return "%5d\t%5d\t%5d\t%s" % (self.startPC, self.endPC, self.handlerPC, self.exceptionClass)

