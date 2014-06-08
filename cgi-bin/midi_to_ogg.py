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
log_file = midi_dir + "log.txt"
write_log = True

f = None

def printHeader():
    print "Content-Type: audio/ogg\n"
    sys.stdout.flush()

def printErrorHeader():
    print "Content-Type: text/plain\n"
    sys.stdout.flush()

def finish():
    sys.stdout.flush()

# Avoid shell injection
def clean_input(path):
    return shlex.split(path)

# Prints the actual response to the ajax call
def return_finished_ogg(ogg_path, pre_encoded):
    try:
        encoded = urllib.quote(open(ogg_path, "rb").read().encode("base64"))
        printHeader()
        sys.stdout.write(encoded)
        finish()
        if (write_log):
            if (pre_encoded == True):
                f.write("Returned pre-encoded ogg!\n")
            else:
                f.write("Returned newly encoded ogg\n")
            f.close()
        sys.exit()
    except Exception as e:
        if (write_log):
            if (pre_encoded):
                f.write("Error returning pre-recorded ogg:\n")
            else:
                f.write("Error returning newly encoded ogg:\n")
            f.write(e)
            f.close()
        sys.exit()

# Takes a path ending in .mid
# Converts that file to .ogg
def convert(original_path, converted_path):

    wav_path = converted_path.replace(".ogg", ".wav")

    try:
        p = subprocess.Popen([convert_command, original_path, convert_flags[0], convert_flags[1], wav_path], close_fds=True, shell=False)
        p.wait()
        if (write_log):
            f.write("conversion returned successfully\n")
        p2 = subprocess.Popen([compress_command, wav_path], close_fds=False, stdin=None, stdout=None, stderr=None, shell=False)
        p2.wait()
        if (write_log):
            f.write("Compression returned successfully\n")
        os.remove(wav_path)
        if (write_log):
            f.write("Wav deletion returned successfully\n")
    except Exception as e:
        if (write_log):
            f.write("Error in converting file:\n")
            f.write(e)
            f.close()
        sys.exit()

if __name__ == "__main__":
    
    if (write_log):
        if (os.path.isfile(log_file) == True):
            os.remove(log_file)
        f = open(log_file, 'w')
        f.write("Opening log file\n")

    try:
        cgitb.enable()
    except Exception as e:
        if (write_log):
            f.write("Error at running cgitb.enable()\n")
            f.write(e)
            f.close()
        sys.exit()

    try:
        path = None
        form = cgi.FieldStorage()
        if (write_log):
            f.write("Opened fieldstorage\n")
    except Exception as e:
        if (write_log):
            f.write("Exception opening fieldstorage:\n")
            f.write(e)
            f.close()
        sys.exit()

    try:
        path = form["path"].value
        if (write_log):
            f.write("Got path: " + path + "\n")
    except Exception as e:
        if (write_log):
            f.write("Exception getting path: " + path + "\n")
            f.write(e)
            f.close()
        sys.exit()
 
    try:
        better_input = clean_input(path)[0]
        fullpath = midi_dir + better_input
        if (write_log):
            f.write("Cleaned input path successfully\n")
    except Exception as e:
        if (write_log):
            f.write("Error cleaning input: " + path + "\n")
            f.write(e)
            f.close()
        sys.exit()

    try:
        if (os.path.isfile(fullpath) == False):
            if (write_log):
                f.write("File does not exist: " + fullpath + "\n")
                f.close()
            sys.exit()
    except Exception as e:
        if (write_log):
            f.write("Error checking if file exists: " + fullpath + "\n")
            f.close()
        sys.exit()

    try:
        converted_path = fullpath.replace(".mid", ".ogg")
        if (write_log):
            f.write("Converted path is " + converted_path + "\n")
    except Exception as e:
        if (write_log):
            f.write("Exception at creating converted filepath:\n")
            f.write(e)
            f.close()
        sys.exit()
 
    try:
        # If the ogg is already converted
        if (os.path.isfile(converted_path) == True):
            return_finished_ogg(converted_path, True)
    except Exception as e:
        if (write_log):
            f.write("Error calling os.path.isfile()\n")
            f.close()
        sys.exit()

    # Time to convert!
    try:
        convert(fullpath, converted_path)
        if (write_log):
            f.write("Converted " + fullpath + " to " + converted_path + "\n")
    except Exception as e:
        if (write_log):
            f.write("Error converting file:\n")
            f.write(e)
            f.close()
        sys.exit()
   
    try:
        if (os.path.isfile(converted_path) == True):
            return_finished_ogg(converted_path, False)
            f.close()
        else:
            if (write_log):
                f.write("Newly converted ogg does not exist at " + converted_path + "\n")
                f.close()
    except Exception as e:
        if (write_log):
            f.write("Error returning newly converted ogg!\n")
            f.write(e)
            f.close()

