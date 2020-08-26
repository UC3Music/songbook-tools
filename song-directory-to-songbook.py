#!/usr/bin/env python

import sys, os, shutil

import mmap  # Thanks Steven @ http://stackoverflow.com/questions/4940032/search-for-string-in-txt-file-python

import subprocess

import readline

readline.set_completer_delims(' \t\n;')
readline.parse_and_bind("tab: complete")
readline.parse_and_bind("set match-hidden-files off")

import argparse

def query(question, default, skipQuery=False):
    if skipQuery:
        return default
    sys.stdout.write(question + " [" + default + "] ? ")
    choice = input()
    if choice == '':
        return default
    return choice

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

    print("-------------------------------------")
    print("Welcome to song-directory-to-songbook")
    print("-------------------------------------")

    parser = argparse.ArgumentParser(formatter_class = MyArgumentDefaultsHelpFormatter)

    parser.add_argument('--input',
                        help='path of the default song input directory',
                        default='examples/')
    parser.add_argument('--output',
                        help='name of the output pdf file',
                        default='Songbook.pdf')
    parser.add_argument('--template',
                        help='name of the LaTeX template file [specifies language, etc]',
                        default='template/english.tex')
    parser.add_argument('--manifest',
                        help='name of a file-avoiding manifest file [if desired]',
                        default='')
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

    # Query the path of the song output file
    outputFile = query("Please specify the name of the output pdf file", args.output, skipQueries)
    print("Will use the output pdf file: " + outputFile)
    outputFileDirAndName, outputFileExtension = os.path.splitext(outputFile)
    outputFileDir, outputFileName = os.path.split(outputFileDirAndName)

    # Query the path of the template file
    templateFile = query("Please specify the path of the LaTeX template file [specifies language, format]", args.template, skipQueries)
    print("Will use template file: " + templateFile)

    # Query (optional) the path of a file-avoiding manifest file
    manifestFile = query("Please specify the name of a file-avoiding manifest file [if desired]", args.manifest, skipQueries)
    if manifestFile == "":
        print("Not using file-avoiding manifest file.")
    else:
        print("Will use file-avoiding manifest file: " + manifestFile)
        manifestFileFd = open(manifestFile, 'r', encoding="utf8")
        manifestMmap = mmap.mmap(manifestFileFd.fileno(), 0, access=mmap.ACCESS_READ)
        manifestFileFd.close()

    print("----------------------")

    templateFileFd = open(templateFile, 'r', encoding="utf8")
    s = templateFileFd.read()
    #sys.stdout.write(s)  #-- Screen output for debugging.

    rep = ""
    for dirname, dirnames, filenames in os.walk(inputDirectory):
        for filename in sorted(filenames):
            name, extension = os.path.splitext(filename)
            if manifestFile != "":
                if manifestMmap.find(name) != -1:
                    print("Skipping:", name)
                    continue
            rep += "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n"
            rep += "\\chapter{" + name + "}\n"  #-- Note that we use \\ instead of \.
            songName = name.split(" - ")[-1]
            #-- We cannot use [] yet (they will be replaced because choir), so use {{}}.
            rep += "\\index{{aux-song-index-file}}{" + songName + "}\n"
            rep += "\\begin{alltt}\n"
            print("os.path.join(dirname, filename)",os.path.join(dirname, filename))
            song = open(os.path.join(dirname, filename), encoding="utf8")
            rep += song.read()
            song.close()
            rep += "\\end{alltt}\n"
            rep += "\n"
    #sys.stdout.write(rep)  #-- Screen output for debugging.

    #-- replace chords delimiter ()
    rep = rep.replace("(","\\textbf{(")
    rep = rep.replace(")",")}")

    #-- replace choir delimiter []
    rep = rep.replace("[","\\textit{[")
    rep = rep.replace("]","]}")

    #-- now we can do this
    rep = rep.replace("{{aux-song-index-file}}","[aux-song-index-file]")

    #-- replace template contents
    s = s.replace("TITLE", outputFileName)
    s = s.replace("genSongbook",rep)

    outputFileTex = outputFileDirAndName + ".tex"
    outFd = open(outputFileTex, 'w', encoding="utf8")
    outFd.write(s)
    outFd.close()

    #http://stackoverflow.com/questions/6818102/detect-and-handle-a-latex-warning-error-generated-via-an-os-system-call-in-pytho
    #pdftex_process = subprocess.Popen(['pdflatex', '-interaction=nonstopmode', '%s'%topic], shell=False, stdout=subprocess.PIPE)

    #-- Seems to be only miktex: '-aux-directory='+outputFileDir
    #-- Messes with makeindex: '-output-directory='+outputFileDir
    ret = subprocess.call(['pdflatex', outputFileTex])
    if ret != 0:
     if ret < 0:
         print("pdflatex (1 of 2): Killed by signal", -ret)
         sys.exit(-ret)
     else:
         print("pdflatex (1 of 2): Command failed with return code", ret)
         sys.exit(ret)

    ret = subprocess.call(['pdflatex', outputFileTex])
    if ret != 0:
     if ret < 0:
         print("pdflatex (2 of 2): Killed by signal", -ret)
         sys.exit(-ret)
     else:
         print("pdflatex (2 of 2): Command failed with return code", ret)
         sys.exit(ret)

    shutil.move(outputFileName+".pdf", outputFileDirAndName+".pdf")

    os.remove("aux-song-index-file.idx")
    os.remove("aux-song-index-file.ilg") # from makeindex
    os.remove("aux-song-index-file.ind") # from makeindex

    os.remove(outputFileName + ".aux")
    os.remove(outputFileName + ".log")
    os.remove(outputFileName + ".out")
    os.remove(outputFileName + ".toc")

    os.remove(outputFileTex)  # may be interested in keeping

    print('DONE! Generated', outputFileDirAndName+'.pdf')
