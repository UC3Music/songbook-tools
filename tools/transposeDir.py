#!/usr/bin/python

import sys, os

import mmap  # Thanks Steven @ http://stackoverflow.com/questions/4940032/search-for-string-in-txt-file-python

import subprocess

import readline

readline.set_completer_delims(' \t\n;')
readline.parse_and_bind("tab: complete")
readline.parse_and_bind("set match-hidden-files off")

def query(question, default):
    sys.stdout.write(question + " [" + default + "] ? ")
    choice = raw_input()
    if choice == '':
        return default
    return choice

if __name__ == '__main__':

    print("-----------------------")
    print("Welcome to transposeDir")
    print("-----------------------")

    # Query song directory path string
    songDirectory = query("Please specify the path of the input song directory","/opt/Dropbox/lyrics/english")
    print("Will use song directory (input): " + songDirectory)

    # Query transposed song directory path string
    transposedSongDirectory = query("Please specify the path of the input song directory","/opt/Dropbox/lyrics/transposed_english")

    if os.path.isdir(transposedSongDirectory):
        yesNo = query('Path "' + transposedSongDirectory + '" already exists, are you sure (confirm with "yes" without quotes)','no')
        if yesNo != "yes":
            print "Ok, bye!"
            quit()
        else:
            print("Will use (existing) transposed song directory (output): " + transposedSongDirectory)
    else:
        os.makedirs(transposedSongDirectory)
        print("Will use (newly created) transposed song directory (output): " + transposedSongDirectory)

    # Query transposition
    halfTones = int( query("Please specify half tones of transposition","0") )
    print("Will use half tones of transposition: " + str(halfTones))

    print("----------------------")

    for dirname, dirnames, filenames in os.walk( songDirectory ):
        for filename in sorted(filenames):
            name, extension = os.path.splitext(filename)
            song = open( os.path.join(dirname, filename) )
            print name
            contents = song.read()
            song.close()

