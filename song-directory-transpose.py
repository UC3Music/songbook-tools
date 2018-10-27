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

from pychord import Chord
from pychord import ChordProgression

globalHalfTones = 0
songHalfTones = 0
applyCapoDropCorrection = True

def query(question, default, skipQuery=False):
    if skipQuery:
        return default
    sys.stdout.write(question + " [" + default + "] ? ")
    choice = raw_input()
    if choice == '':
        return default
    return choice

def recursivelyProcessBlockWithParenthesisAndExceptionsTreated( stringToProcess, processed):
    global songHalfTones
    #print 'String to process "' + stringToProcess + '".'
    afterSplit = re.split("  |_|!|\.\.\.|\.\.|: |\*|high|open|bass|riff|palm mute|notes|m6|madd11/|m7add11/|7sus2|8|m7b5|madd13|add13", stringToProcess, 1)  # 3rd parameter is maxsplit # Also works with single space, do this to catch faulty txt.
    #print '* Split by delimiters "' + str(afterSplit) + '".'
    #print 'songHalfTones:',songHalfTones
    if len(afterSplit[0]) != 0:
        chord = Chord(afterSplit[0])
        #print '* Extracted "' + chord.chord + '" chord.'
        chord.transpose( songHalfTones, "C#" )
        #print '* Transposed to "' + chord.chord + '" chord.'
        processed += chord.chord
        #print '* Processed after chord "' + processed + '".'
    #else:
        #print '* No chord to extract.'
    if len(afterSplit) == 1:
        return processed
    delimiterWas = ''
    if len(afterSplit[1]) == 0:
        delimiterWas = stringToProcess[len(afterSplit[0]):]
    else:
        delimiterWas = stringToProcess[len(afterSplit[0]):-len(afterSplit[1])]
    #print '* Delimiter was "' + delimiterWas + '".'
    processed += delimiterWas
    #print '* Processed after delimiter "' + processed + '".'
    #print '* Still must process "' + afterSplit[1] + '".'
    return recursivelyProcessBlockWithParenthesisAndExceptionsTreated( afterSplit[1], processed )

def processBlockWithParenthesis(matchobj):
    global songHalfTones
    # Print for debugging purposes: what is being treated
    print "--- " + matchobj.group(0)
    # Treat exceptions that are simply skipped and return
    if matchobj.group(0).find("bpm)") != -1:
        return matchobj.group(0)
    if matchobj.group(0).find("(all") != -1:
        return matchobj.group(0)
    # Treat exception that affects songHalfTones and returns: capo
    if matchobj.group(0).find("capo") != -1:
        if applyCapoDropCorrection:
            m = matchobj.group(0)
            got = re.findall('\d+', m)
            if len(got) != 1:
                print '*** ERROR (len(got) != 1)'
                quit()
            print '*** capo:',int(got[0])
            songHalfTones += int(got[0])
            print '*** new songHalfTones:',songHalfTones
            # Print for debugging purposes: info on modification and original source
            betweenParenthesis = matchobj.group(0).replace("(","").replace(")","")
            print "+++ (chords for no capo; generated from " + betweenParenthesis + ")"
            return "(chords for no capo; generated from " + betweenParenthesis + ")"
        else:
            return matchobj.group(0)
    # Treat exception that affects songHalfTones and returns: drop
    if matchobj.group(0).find("drop") != -1:
        if applyCapoDropCorrection:
            m = matchobj.group(0)
            got = re.findall('\d+', m)
            if len(got) != 1:
                print '*** ERROR (len(got) != 1)'
                quit()
            print '*** drop:',int(got[0])
            songHalfTones -= int(got[0])
            print '*** new songHalfTones:',songHalfTones
            # Print for debugging purposes: info on modification and original source
            betweenParenthesis = matchobj.group(0).replace("(","").replace(")","")
            print "+++ (chords for no drop; generated from " + betweenParenthesis + ")"
            return "(chords for no drop; generated from " + betweenParenthesis + ")"
        else:
            return matchobj.group(0)
    # Get betweenParenthesis and call actual process:
    betweenParenthesis = matchobj.group(0).replace("(","").replace(")","")
    final = recursivelyProcessBlockWithParenthesisAndExceptionsTreated( betweenParenthesis, "" )
    # Print for debugging purposes: final after processing betweenParenthesis
    print "+++ " + "(" + final + ")"
    return "(" + final + ")"

class MyArgumentDefaultsHelpFormatter(argparse.HelpFormatter):

    def _split_lines(self, text, width):
        return text.splitlines()

    def _get_help_string(self, action):
        help = action.help
        if '%(default)' not in action.help:
            if action.default is not argparse.SUPPRESS:
                defaulting_nargs = [argparse.OPTIONAL, argparse.ZERO_OR_MORE]
                if action.option_strings or action.nargs in defaulting_nargs:
                    help += ' (default: "%(default)s")'
        return help

if __name__ == '__main__':

    print("-----------------------------------")
    print("Welcome to song-directory-transpose")
    print("-----------------------------------")

    parser = argparse.ArgumentParser(formatter_class = MyArgumentDefaultsHelpFormatter)

    parser.add_argument('--input',
                        help='path of the default song input directory',
                        default='examples/')
    parser.add_argument('--output',
                        help='path of the default song output directory',
                        default='out/')
    parser.add_argument('--transpose',
                        help='half tones of transposition',
                        default='0')
    parser.add_argument('--capoDropCorrection',
                        help='if automatic capo/drop correction should be applied',
                        default='yes')
    parser.add_argument('--yes',
                        help='accept all, skip all queries',
                        nargs='?',
                        default='NULL')  # required, see below
    args = parser.parse_args()

    skipQueries = False
    if args.yes is not 'NULL':  # if exists and no contents, replaces 'NULL' by None
        print("Detected --yes parameter: will skip queries")
        skipQueries = True

    # Query the path of the song input directory
    inputDirectory = query("Please specify the path of the song input directory", args.input, skipQueries)
    print("Will use song input directory: " + inputDirectory)

    # Query the path of the song output directory
    outputDirectory = query("Please specify the path of the song output directory", args.output, skipQueries)

    if os.path.isdir(outputDirectory):
        yesNo = query('Path "' + outputDirectory + '" already exists, are you sure (confirm with "y" or "yes" without quotes)', 'yes', skipQueries)
        if yesNo != "yes" and yesNo != "y":
            print("Ok, bye!")
            quit()
        else:
            print("Will use (existing) song output directory: " + outputDirectory)
    else:
        os.makedirs(outputDirectory)
        print("Will use (newly created) song output directory: " + outputDirectory)

    # Query transposition
    globalHalfTones = int( query("Please specify half tones of transposition (e.g. 7 or -5 for soprano ukelele and guitalele)", args.transpose, skipQueries) )
    print("Will use half tones of transposition: " + str(globalHalfTones))

    # Query capoDropCorrection
    while True:
        yesNo = query('Apply capo/drop correction (answer with "y"/"yes" or "n"/"no" without quotes)?', args.capoDropCorrection, skipQueries)
        if yesNo == "yes" or yesNo == "y":
            print("Will apply capo/drop correction")
            applyCapoDropCorrection = True
            break
        elif yesNo == "no" or yesNo == "n":
            print("Will not apply capo/drop correction")
            applyCapoDropCorrection = False
            break

    print("----------------------")

    for dirname, dirnames, filenames in os.walk(inputDirectory):
        for filename in sorted(filenames):
            songHalfTones = globalHalfTones
            #debug
            print filename
            print '*** songHalfTones:',songHalfTones
            name, extension = os.path.splitext(filename)
            songIn = open( os.path.join(dirname, filename) )
            songOut = open(os.path.join(outputDirectory, filename), "w")
            contents = ""
            if globalHalfTones != 0:
                contents += "(all chords have been pre-transposed " + str(globalHalfTones) + " semitones)" + os.linesep  + os.linesep
                print "+++ (all chords have been pre-transposed " + str(globalHalfTones) + " semitones)"
            contents += songIn.read()
            contents = re.sub("\([^)]*\)", processBlockWithParenthesis, contents) # line that really does it
            songOut.write(contents)
            songOut.close()
            songIn.close()
