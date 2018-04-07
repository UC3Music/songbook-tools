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

    print("-------------------------------------")
    print("Welcome to song-directory-to-songbook")
    print("-------------------------------------")

    # Query song directory path string
    songDirectory = query("Please specify the path of the input song directory","/opt/Dropbox/chords/0-GUITAR/english")
    print("Will use song directory: " + songDirectory)

    # Query template file path string
    templateFile = query("Please specify the path of the template file","template/english.tex")
    print("Will use template file: " + templateFile)

    # Query optional avoiding-manifest file path string
    manifestFile = query("(optional) Please specify the path of a avoiding-manifest file","")
    if manifestFile == "":
        print("Not using avoiding-manifest file.")
    else:
        print("Will use avoiding-manifest file: " + manifestFile)
        manifestFileFd = open(manifestFile, 'r')
        manifestMmap = mmap.mmap(manifestFileFd.fileno(), 0, access=mmap.ACCESS_READ)
        manifestFileFd.close()

    print("----------------------")

    templateFileFd = open(templateFile, 'r')
    s = templateFileFd.read()
    #sys.stdout.write(s)  #-- Screen output for debugging.

    rep = ""
    for dirname, dirnames, filenames in os.walk( songDirectory ):
        for filename in sorted(filenames):
            name, extension = os.path.splitext(filename)
            if manifestFile != "":
                if manifestMmap.find(name) != -1:
                    print "Skipping:", name
                    continue
            rep += "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n"
            rep += "\\chapter{" + name + "}\n"  #-- Note that we use \\ instead of \.
            songName = name.split(" - ")[-1]
            rep += "\\index{{song}}{" + songName + "}\n"
            rep += "\\begin{alltt}\n"
            song = open( os.path.join(dirname, filename) )
            rep += song.read()
            song.close()
            rep += "\\end{alltt}\n"
            rep += "\n"
    #sys.stdout.write(rep)  #-- Screen output for debugging.

    rep = rep.replace("(","\\textbf{(")
    rep = rep.replace(")",")}")

    rep = rep.replace("[","\\textit{[")
    rep = rep.replace("]","]}")

    rep = rep.replace("{{song}}","[song]")

    s = s.replace("genSongbook",rep)

    outFd = open("out.tex", 'w')
    outFd.write(s)
    outFd.close()

    #http://stackoverflow.com/questions/6818102/detect-and-handle-a-latex-warning-error-generated-via-an-os-system-call-in-pytho
    #pdftex_process = subprocess.Popen(['pdflatex', '-interaction=nonstopmode', '%s'%topic], shell=False, stdout=subprocess.PIPE)
    pdftex_process = subprocess.call(['pdflatex', 'out'])
    pdftex_process = subprocess.call(['pdflatex', 'out'])

