#!/usr/bin/env python3

import os, sys, argparse, platform, getpass
from tkinter import Tk
from tkinter import messagebox
from Crypto import Random
from Crypto.Cipher import AES
from tkinter.filedialog import askdirectory
from pymsgbox import *

'''
def parse_args():
    # Create the arguments
    parser = argparse.ArgumentParser(description='Decrypt .DEMON files')
    parser.add_argument("-k", "--key", help="Set decryption key")
    return parser.parse_args()

args = parse_args()
'''

def pad(s):
    return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

def decrypt(ciphertext, key):
    iv = ciphertext[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext[AES.block_size:])
    return plaintext.rstrip(b"\0")

def decrypt_file(file_name, key):
    with open(file_name, 'rb') as f:
        ciphertext = f.read()
    dec = decrypt(ciphertext, key)
    with open(file_name[:-6], 'wb') as f:
        f.write(dec)

'''
if not args.key:
    print('Please, enter a VALID key to start decrytping your files')
    sys.exit(1)
else:
    key = args.key
'''

Tk().withdraw()

def dec_key():
    key = password(text='Please enter your decryption key', title='Enter Key', mask ='*')
    if key == None or key == '':
        messagebox.showwarning('Error', 'Please, enter your key.')
        return dec_key()
    elif not len(key) == 32:
        messagebox.showwarning('Invalid Key', 'Key should be 32 characters long')
        return dec_key()
    return key

def dec_path():
    path = askdirectory(title = 'Select directory with files to decrypt')
    if path == None or path == '':
        messagebox.showwarning('Error', 'No path selected, exiting...')
        sys.exit(1)
    path =  path + '/'
    return path

key = dec_key()
p = dec_path()

try:
    '''
    if platform.system() == 'Linux':
        #p = '/home/' + getpass.getuser() + '/'
        p = '/home/lv-laptop/Documents/directories/programmeren/python/demonware/test' + '/'
    elif platform.system() == 'Windows':
        p = 'C:\\Users\\' + getpass.getuser() + '\\'
    '''
    counter = 0
    for path, subdirs, files in os.walk(p):
        for name in files:
            if name.endswith(".DEMON"):
                decrypt_file(os.path.join(path, name), key)
                print("[Decrypting] %s" % name)
                counter = counter+1
                os.remove(os.path.join(path, name))
            else:
                print("[Skipped] %s" % name)
    print("\n[DONE] Decrypted %i files" % counter)

except KeyboardInterrupt:
    print("\nInterrupted!\n")
    sys.exit(0)
except Exception as e:
    print("\n[ ERROR ] %s" % e)
    sys.exit(1)
