# A simple socket client. It will go through all ports set as command line
# option and open X number of connections per port

import socket
import argparse
import random
import threading
from time import sleep


def send_data(socket, host, port):
    while True:
        socket.sendall(str(random.random()))
        data = socket.recv(1024)
        print("Received {0} from {1}:{2}".format(data, host, port))
        sleep(1)


def main():

    parser = argparse.ArgumentParser(description='sum the integers at the command line')
    parser.add_argument('--minport', type=int, required=True, help='The lowest port number')
    parser.add_argument('--maxport', type=int, required=True, help='The highest port number')
    parser.add_argument('--nconn', type=int, required=True, help='number of connections per port')
    parser.add_argument('--host', required=True, help='host to connect to')
    args = parser.parse_args()

    sockets = {}
    for port in range(args.minport, args.maxport):
        sockets[port] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sockets[port].connect((args.host, port))
        except socket.error as e:
            print("Socket on port {0} --> {1}".format(port, e))
            continue
        for i in range(args.nconn):
            thread = threading.Thread(target=send_data, args=((sockets[port], args.host, port)))
            thread.start()


if __name__ == "__main__":
    main()
