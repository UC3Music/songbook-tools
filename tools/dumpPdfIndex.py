#!/usr/bin/python

import os, sys

import poppler

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

# Thanks: Oz123 @ http://stackoverflow.com/questions/7131906/how-to-extract-pdf-index-table-of-contents-with-poppler
def walk_index(iterp, doc):
    while iterp.next():
      link=iterp.get_action()
      s = doc.find_dest(link.dest.named_dest)
      print link.title #,' ', doc.get_page(s.page_num).get_label()
      child = iterp.get_child()
      if child:
        walk_index(child, doc)

if __name__ == '__main__':
    # Query path_to_pdf string
    path_to_pdf = query("Please specify the pdf file","out.pdf")
    if not os.path.isabs(path_to_pdf):
	path_to_pdf = os.path.abspath('.') + "/" + path_to_pdf
    print("Will extract manifest from file: " + path_to_pdf)

    uri = ("file:///"+path_to_pdf)
    doc = poppler.document_new_from_file(uri, None)

    iterp = poppler.IndexIter(doc)
    link = iterp.get_action()
    s = doc.find_dest(link.dest.named_dest)
    #print link.title #,' ', doc.get_page(s.page_num).get_label()
    walk_index(iterp, doc)

