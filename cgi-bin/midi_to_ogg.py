#!/usr/bin/python

import os
import sys
import urllib
import cgi
import cgitb
import subprocess
import shlex

midi_dir = "../midis/"
convert_command = "/usr/bin/timidity"
convert_flags = ["-Ow", "-o"]
compress_command = "/usr/bin/oggenc"

def printHeader():
    print "Content-Type: text/html\n"
    sys.stdout.flush()

def finish():
    sys.stdout.flush()

# Avoid shell injection
def clean_input(path):
    return shlex.split(path)

# Takes a path ending in .mid
# Converts that file to .ogg
def convert(original_path, converted_path):

    wav_path = converted_path.replace(".ogg", ".wav")

    try:
        p = subprocess.Popen([convert_command, original_path, convert_flags[0], convert_flags[1], wav_path], close_fds=True, stdin=None, stdout=None, stderr=None, shell=False)
        p.wait()
        p2 = subprocess.Popen([compress_command, wav_path], close_fds=True, stdin=None, stdout=None, stderr=None, shell=False)
        p2.wait()
        os.remove(wav_path)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    cgitb.enable()

    path = None
    form = cgi.FieldStorage()

    try:
        path = "marblegarden.mid"
    except Exception as e:
        print(e)
        printHeader()
        print "POST request did not have a path in it"
        finish()
 
    better_input = clean_input(path)[0]
    fullpath = midi_dir + better_input

    if (os.path.isfile(fullpath) == False):
        printHeader()
        print "Error: File does not exist: " + fullpath
        finish()
        sys.exit()

    converted_path = fullpath.replace(".mid", ".ogg")
 
    # If the ogg is already converted
    if (os.path.isfile(converted_path) == True):
        try:
            encoded = urllib.quote(open(converted_path, "rb").read().encode("base64"))
            printHeader()
            print(encoded)
            finish()
            sys.exit()
        except Exception as e:
            print(e)
            printHeader()
            print "Error returning pre-converted ogg"
            finish()
            sys.exit()

    # Time to convert!
    convert(fullpath, converted_path)
    
    try:
        encoded = urllib.quote(open(converted_path, "rb").read().encode("base64"))
        printHeader()
        sys.stdout.write(encoded)
        sys.stdout.flush()
    except Exception as e:
        print(e)
        printHeader()
        print "Something broke in returning a newly converted ogg"
        print better_input
        print converted_path
        finish()

