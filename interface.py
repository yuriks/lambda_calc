#!/usr/bin/env python2

import sys
from optparse import OptionParser

def main():
    interactive = sys.stdin.isatty() and sys.stdout.isatty()

    parser = OptionParser(usage="usage: %prog [options]")
    parser.add_option('-m', '--machine', dest="machine_file",
                      help="File to read expression from, instead of stdin.")
    parser.add_option('-b', '--batch',
                      action="store_false", dest="interactive",
                      help="Run in batch mode: Evaluates the expression an retuns
                        normal form.")
    parser.add_option('-i', '--interactive',
                      action="store_true",  dest="interactive", default=interactive,
                      help="Run in interactive mode: Reads an input and evaluate
                        expression step-by-step.")

    options, args = parser.parse_args()

if __name__ == '__main__':
    main()
