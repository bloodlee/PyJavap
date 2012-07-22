__author__ = 'jasonlee'

from PyJavapInternal.Parser import Parser, ParsingResult

if __name__ == '__main__':

    import argparse

    description= 'Parse java class file'

    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('-cf', type=str, help='java class file', required=True)

    options = parser.parse_args()

    clsParser = Parser(options.cf)
    clsResult = clsParser.parse()

    if clsResult:
        print clsResult.__str__()
    else:
        print 'Parsing failed. Please check the log.'


