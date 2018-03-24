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

    print("-------------------------------")
    print("Welcome to song-directory-strip")
    print("-------------------------------")

    # Query song directory path string
    songDirectory = query("Please specify the path of the song (input) directory","/opt/Dropbox/chords/0-GUITAR/english")
    print("Will use song directory (input): " + songDirectory)

    # Query stripped song directory path string
    strippedSongDirectory = query("Please specify the path of the stripped song (output) directory","tmp")

    if os.path.isdir(strippedSongDirectory):
        yesNo = query('Path "' + strippedSongDirectory + '" already exists, are you sure (confirm with "y" or "yes" without quotes)','yes')
        if yesNo != "yes" and yesNo != "y":
            print "Ok, bye!"
            quit()
        else:
            print("Will use (existing) stripped song directory (output): " + strippedSongDirectory)
    else:
        os.makedirs(strippedSongDirectory)
        print("Will use (newly created) stripped song directory (output): " + strippedSongDirectory)

    print("----------------------")

    #sys.stdout.write(s)  #-- Screen output for debugging.

    rep = ""
    for dirname, dirnames, filenames in os.walk( songDirectory ):
        for filename in sorted(filenames):
            #debug
            print filename

