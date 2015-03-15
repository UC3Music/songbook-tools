#!/usr/bin/python

import sys, os

def query(question, default):
    sys.stdout.write(question + " [" + default + "] ? ")
    choice = raw_input()
    if choice == '':
        return default
    return choice

if __name__ == '__main__':

    print("----------------------")
    print("Welcome to genSongbook")
    print("----------------------")

    # Query song directory path string
    songDirectory = query("Please specify the path of the input song directory","./english")
    print("Will use song directory: " + songDirectory)

    # Query template file path string
    templateFile = query("Please specify the path of the template file","template/english.tex")
    print("Will use template file: " + templateFile)

    print("----------------------")

    templateFileFd = open(templateFile, 'r')
    s = templateFileFd.read()
    sys.stdout.write(s)

    print("----------------------")

    outFd = open("out.tex", 'w')
    outFd.write(s)

