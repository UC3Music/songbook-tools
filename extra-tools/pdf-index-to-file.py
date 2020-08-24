#!/usr/bin/env python

import sys, os

import poppler

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

# Thanks: Oz123 @ http://stackoverflow.com/questions/7131906/how-to-extract-pdf-index-table-of-contents-with-poppler
def walk_index(manifestFd,iterp, doc):
    while iterp.next():
      link=iterp.get_action()
      s = doc.find_dest(link.dest.named_dest)
      print(link.title) #,' ', doc.get_page(s.page_num).get_label()
      manifestFd.write(link.title + '\n')
      child = iterp.get_child()
      if child:
        walk_index(manifestFd,child, doc)

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

    print("----------------------------")
    print("Welcome to pdf-index-to-file")
    print("----------------------------")

    parser = argparse.ArgumentParser(formatter_class = MyArgumentDefaultsHelpFormatter)

    parser.add_argument('--input',
                        help='name of the input pdf file',
                        default='songbook.pdf')
    parser.add_argument('--output',
                        help='name of the output txt file',
                        default='manifest.txt')
    parser.add_argument('--yes',
                        help='accept all, skip all queries',
                        nargs='?',
                        default='NULL')  # required, see below
    args = parser.parse_args()

    skipQueries = False
    if args.yes is not 'NULL':  # if exists and no contents, replaces 'NULL' by None
        print("Detected --yes parameter: will skip queries")
        skipQueries = True

    # Query the input pdf file
    path_to_pdf = query("Please specify the name of the input pdf file", args.input, skipQueries)
    if not os.path.isabs(path_to_pdf):
	path_to_pdf = os.path.abspath('.') + "/" + path_to_pdf
    print("Will extract manifest from file: " + path_to_pdf)

    # Query output string
    manifest = query("Please specify the name of the output txt file", args.output, skipQueries)
    print("Will extract manifest to file: " + manifest)
    manifestFd = open(manifest, 'a')

    uri = ("file:///"+path_to_pdf)
    doc = poppler.document_new_from_file(uri, None)

    iterp = poppler.IndexIter(doc)
    link = iterp.get_action()
    s = doc.find_dest(link.dest.named_dest)
    print(link.title) #,' ', doc.get_page(s.page_num).get_label()
    manifestFd.write(link.title + '\n')
    walk_index(manifestFd,iterp, doc)
    manifestFd.close()
