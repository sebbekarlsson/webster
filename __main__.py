from webster.web.SpiderNet import SpiderNet
from webster.CommandParser import CommandParser
import threading
import sys
import socket
import json


def user_connection(conn):
    while conn:
        try:
            data = conn.recv(1024)

            if data:
                try:
                    commandparser.parse(data, conn)
                except Exception as e:
                    conn.send(str(e))
            else:
                conn.close()
        except:
            conn.close()


commandparser = CommandParser()

if __name__ == '__main__':
    if len(sys.argv) == 1:
        quit()

    if sys.argv[1] == 'server':
        net = SpiderNet([
            'http://www.ica.se/',
            'https://www.coop.se/',
            'http://duva.se/',
            'http://www.ember.se/',
            'https://lidkoping.se/',
            'https://www.flashback.org/',
            'https://sv.wordpress.org/',
            'http://www.gotene.se/index.html'
            ])

        try:
            net.start()
        
            HOST = 'localhost'
            PORT = 54337
            s = None
            for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC,
                                          socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
                af, socktype, proto, canonname, sa = res
                try:
                    s = socket.socket(af, socktype, proto)
                except socket.error as msg:
                    s = None
                    continue
                try:
                    s.bind(sa)
                    s.listen(1)
                except socket.error as msg:
                    s.close()
                    s = None
                    continue
                break
            if s is None:
                print('could not open socket')
                sys.exit(1)

            print('SERVER RUNNING ON PORT: {}'.format(PORT))
           
            while True:
                conn, addr = s.accept()
                if conn:
                    t = threading.Thread(target=user_connection, args=(conn,))
                    t.daemon = True
                    t.start()

        except KeyboardInterrupt:
            net.running = False
            quit()
    else:
        HOST = 'localhost'
        PORT = 54337
        s = None
        for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM):
            af, socktype, proto, canonname, sa = res
            try:
                s = socket.socket(af, socktype, proto)
            except socket.error as msg:
                s = None
                continue
            try:
                s.connect(sa)
            except socket.error as msg:
                s.close()
                s = None
                continue
            break
        if s is None:
            print('could not open socket')
            sys.exit(1)

        try:
            while True:
                input = raw_input("> ")
                s.sendall(b'{}'.format(input))
                data = s.recv(1024 * 1024)
                if data:
                    print(str(data))

            s.close()
        except KeyboardInterrupt:
            quit()
