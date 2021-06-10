#!/usr/bin/env python3
# Name: Rob Lodes (rlodes), Michael Farley (mijfarle)
# PI: Miten Jain
# bme160 final project

import glob
from mitoUtils import SamReader, mitoDictionary

########################################################################
# CommandLine
########################################################################
class CommandLine():
    '''
    Handle the command line, usage and help requests.

    CommandLine uses argparse, now standard in 2.7 and beyond.
    it implements a standard command line argument parser with various argument options,
    a standard usage and help.

    attributes:
    all arguments received from the commandline using .add_argument will be
    avalable within the .args attribute of object instantiated from CommandLine.
    For example, if myCommandLine is an object of the class, and requiredbool was
    set as an option using add_argument, then myCommandLine.args.requiredbool will
    name that option.
    '''

    def __init__(self, inOpts=None):
        '''
        Implement a parser to interpret the command line argv string using argparse.
        '''

        import argparse
        self.parser = argparse.ArgumentParser(
            description='Program prolog - a brief description of what this thing does',
            epilog='Program epilog - some other stuff you feel compelled to say',
            add_help=True,  # default is True
            prefix_chars='-',
            usage='%(prog)s [options] -option1[default] <input >output'
            )
        self.parser.add_argument('-p', '--path', action='store', default=None, nargs='?',
                                 help='Location of the data files. Format: ./data/*.txt')
        self.parser.add_argument('-d', '--distance', type=int, choices=(0, 3, 5, 7, 10, 25, 100), default=10,
                                 action='store', help='number of bases to either side of the POI')
        self.parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.1')
        if inOpts is None:
            self.args = self.parser.parse_args()
        else:
            self.args = self.parser.parse_args(inOpts)

########################################################################
# Main
########################################################################

def main(inFile=None, options=None):
    '''
    The Main function.
    Input: pysam files in the data subdirectory
    Output: fasta file with seqs of interest to STDOUT
    Example use: python mito.py
    '''

    thisCommandLine = CommandLine(options)

    if (thisCommandLine.args.path is None):
        thisCommandLine.args.path = './data/*.txt'

    files = glob.glob(thisCommandLine.args.path, recursive = True)     # Employs glob to return a list of file names
    myMito = mitoDictionary()

    mySam = SamReader(files[0])                             # input the first file
    for row in mySam.readSam():
        myMito.addPrimeRow(row)

    for file in range(1, len(files)):                       # input from second file on
        mySam = SamReader(files[file])
        for row in mySam.readSam():
            myMito.addRow(row)

    distance = thisCommandLine.args.distance       # number of bases to each side of the point of interest

    for index in range(0, len(files)):
        myMito.outputFasta(files[index], distance, index)

    # print(thisCommandLine.args)                       # for debugging
    
if __name__ == "__main__":
    main()


