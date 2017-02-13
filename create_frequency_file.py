#!/usr/bin/env python3.4
#
# @file    create_frequency_file.py
# @brief   Encapsulates the steps to create frequency.csv from raw word frequencies
# @author  Michael Hucka
#
# <!---------------------------------------------------------------------------
# Copyright (C) 2015 by the California Institute of Technology.
# This software is part of CASICS, the Comprehensive and Automated Software
# Inventory Creation System.  For more information, visit http://casics.org.
# ------------------------------------------------------------------------- -->

import csv
import math
import plac
import re
import sys

sys.path.append('../common')

from utils import *
from logger import *


# Utilities
# .............................................................................

def simple_undesirable(w):
    '''Single letters, or repeated 2-letter sequences such as 'aa' or 'Bb'.'''
#    return len(w) == 1 or (len(w) == 2 and w[0].lower() == w[1].lower())
    return (len(w) == 2 and w[0].lower() == w[1].lower())


def special_case_undesirable(w):
    '''Things that end up in the word lists but are not useful.'''
    return 'py' == w.lower()


def undesirable(w):
    return simple_undesirable(w) or special_case_undesirable(w)


# Main
# .............................................................................

def create_frequency_file(inputfile=None, outputfile=None, debug=False,
                          loglevel='info'):
    log = Logger(os.path.splitext(sys.argv[0])[0], console=True).get_log()
    if debug:
        log.set_level('debug')
    else:
        log.set_level(loglevel)
    try:
        with open(inputfile, 'r') as input:
            with open(outputfile, 'w') as output:
                if debug:
                    import ipdb; ipdb.set_trace()
                total = 0
                for line in input:
                    (word, count) = line.split()
                    if undesirable(word):
                        log.debug('skipping undesirable word {}'.format(word))
                    else:
                        output.write(word)
                        output.write(',')
                        output.write(count)
                        output.write('\n')
                        total += 1
                log.info('{} words written to {}'.format(total, outputfile))
    except Exception as err:
        log.error(err)


create_frequency_file.__annotations__ = dict(
    debug      = ('drop into ipdb opening files', 'flag',   'd'),
    inputfile  = ('input text file',              'option', 'i'),
    outputfile = ('output CSV file',              'option', 'o'),
    loglevel   = ('logging level: "debug" or "info"', 'option', 'L'),
)

if __name__ == '__main__':
    plac.call(create_frequency_file)