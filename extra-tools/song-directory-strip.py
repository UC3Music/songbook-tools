#!/usr/bin/env python

import sys, os

import mmap  # Thanks Steven @ http://stackoverflow.com/questions/4940032/search-for-string-in-txt-file-python

import subprocess

import readline

readline.set_completer_delims(' \t\n;')
readline.parse_and_bind("tab: complete")
readline.parse_and_bind("set match-hidden-files off")

import argparse

import re

def query(question, default, skipQuery=False):
    if skipQuery:
        return default
    sys.stdout.write(question + " [" + default + "] ? ")
    choice = raw_input()
    if choice == '':
        return default
    return choice

if __name__ == '__main__':

    print("-------------------------------")
    print("Welcome to song-directory-strip")
    print("-------------------------------")

    parser = argparse.ArgumentParser(formatter_class = argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--input',
                        help='specify the path of the default song (input) directory',
                        default='examples/')
    parser.add_argument('--output',
                        help='specify the path of the default song (output) directory',
                        default='out/')
    parser.add_argument('--yes',
                        help='accept all, skip all queries',
                        nargs='?',
                        default='NULL')  # required, see below
    args = parser.parse_args()

    skipQueries = False
    if args.yes is not 'NULL':  # if exists and no contents, replaces 'NULL' by None
        print("Detected --yes parameter: will skip queries")
        skipQueries = True

    # Query the path of the song (input) directory
    inputDirectory = query("Please specify the path of the song (input) directory", args.input, skipQueries)
    print("Will use song (input) directory: " + inputDirectory)

    # Query the path of the song (output) directory
    outputDirectory = query("Please specify the path of the song (output) directory", args.output, skipQueries)

    if os.path.isdir(outputDirectory):
        yesNo = query('Path "' + outputDirectory + '" already exists, are you sure (confirm with "y" or "yes" without quotes)', 'yes', skipQueries)
        if yesNo != "yes" and yesNo != "y":
            print "Ok, bye!"
            quit()
        else:
            print("Will use (existing) song (output) directory: " + outputDirectory)
    else:
        os.makedirs(outputDirectory)
        print("Will use (newly created) song (output) directory: " + outputDirectory)

    print("----------------------")

    #sys.stdout.write(s)  #-- Screen output for debugging.

    rep = ""
    for dirname, dirnames, filenames in os.walk(inputDirectory):
        for filename in sorted(filenames):
            #debug
            print filename
            songIn = open( os.path.join(dirname, filename) )
            songOut = open(os.path.join(outputDirectory, filename), "w")
            contents = songIn.read()
            contents = re.sub("\([^)]*\)", '', contents)
            songOut.write(contents)
            songOut.close()
            songIn.close()
