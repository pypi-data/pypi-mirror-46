import sys
import logging
import argparse

from matchreport.analysis.analyser import analyse
from matchreport.collect.formatter import cleanAndFormatData
from matchreport.communicate.matchreport import createMatchReport
from matchreport.helpers.filehelper import loadDataFromFile


def parseCommandLine():
    parser = argparse.ArgumentParser()

    parser.add_argument("-gaamatch", help="The full path and filename of export from GAAMatch")
    parser.add_argument("-outputDirectory", help="The report output file name and location")

    args = parser.parse_args()

    return args


def main(argv):
    args = parseCommandLine()

    mobileAppOutput = loadDataFromFile(args.gaamatch)

    formattedData = cleanAndFormatData(mobileAppOutput)

    analysis = analyse(formattedData)

    createMatchReport(args.outputDirectory, analysis)


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stderr, level=logging.INFO)

    main(sys.argv[1:])
