#!/usr/bin/python

import sys

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
    path = query("Please specify the path of the input song directory","./english")
    print("Will use: " + path)
    
