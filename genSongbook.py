#!/usr/bin/python

import cmd  #-- Thanks: http://pymotw.com/2/cmd/

class GenSongbook(cmd.Cmd):
    """Main class."""
    prompt = '>> '
    intro = 'Welcome to GenSongbook. Type "help" for help.'
    
    def do_greet(self, person):
        if person:
            print "hi,", person
        else:
            print 'hi'
    
    def help_greet(self):
        print '\n'.join([ 'greet [person]',
                           'Greet the named person',
                           ])
    
    def do_EOF(self, line):
        return True

if __name__ == '__main__':
    GenSongbook().cmdloop()

