#!/usr/bin/env python
# -*- coding: utf-8 -*- 
""" Command line application that responds to any messages you say to Bot """
from __future__ import division, print_function, absolute_import

import argparse
import sys
import logging

from aichat.brain import respond, Responder
from aichat import console


logger = logging.getLogger('aichat')

__author__ = "Aira"
__copyright__ = "Aira"
__license__ = "mit"


def main(args):
    """Main entry point allowing external calls

    Args:
      args ([str]): command line parameter list

    Prints out the response from the response function


    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-c', '--console', action='store_true',
        help="Persist a chat session in the terminal (a bot console).")
    parser.add_argument(
        '-t', '--telnet', action='store_true',
        help="WARNING: NOT YET IMPLEMENTED!!! Start a `mud-pi`-like telnet server based.")
    parser.add_argument(
        'inputs', type=str, nargs='*',
        help="User input statement, text message, or utterance. Words separated by spaces.")

    args = parser.parse_args()

    if getattr(args, 'console', None):  # start a console app that requires you to type "quit" or "ctrl-c" to exit
        console.Console()
    else:  # just do a one-off reply to the user statement
        responder = Responder()
        responder.respond(' '.join(args.inputs))


def run():
    """Entry point for console_scripts """
    main(sys.argv[1:])


def run_console():
    """Entry point for console_scripts """
    if '-c' not in sys.argv[1:] and '--console' not in sys.argv[1:]:
        sys.argv.append('--console')
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
