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

