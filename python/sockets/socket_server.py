# Based on the asyncore code at https://pymotw.com/2/asyncore/#servers
# I've done this with multiprocessing.Process but it could have been made 
# with threading.Thread too
from multiprocessing import Process
import threading
import asyncore
import socket
import sys
import argparse 


class SocketServer(asyncore.dispatcher):
    """Main class to receive connections from clients and
    dispatch handlers for each client.
    The socket is reusable"""

    def __init__(self, host, port, maxconn=5):
        self.host = host
        self.port = port
        self.maxconn = maxconn

        asyncore.dispatcher.__init__(self)

        # Do the socket work
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind((host, port))
        self.set_reuse_addr()
        self.addr = self.socket.getsockname()
        self.listen(self.maxconn)
        return

    def handle_accept(self):
        """Method to handle connections to the socket"""
        client = self.accept()
        if client:
            JobHandler(sock=client[0])
        return

    def handle_close(self):
        self.close()
        return


class JobHandler(asyncore.dispatcher):
    """Class to handle the work to do when receiving messages
    from the client"""

    def __init__(self, sock, buf=1024):
        self.buf = buf
        asyncore.dispatcher.__init__(self, sock=sock)
        self.data_to_write = []
        return

    def writable(self):
        """Checks that we have received data"""
        return bool(self.data_to_write)

    def handle_write(self):
        """Sends back the message we have just received"""
        data = self.data_to_write.pop()
        sent = self.send(data[:self.buf])
        if sent < len(data):
            remaining = data[sent:]
            self.data_to_write.append(remaining)

    def handle_read(self):
        """Read the incoming message"""
        data = self.recv(self.buf)
        self.data_to_write.insert(0, data)

    def handle_close(self):
        self.close()


def handle_options():
    """Handle the command line options"""
    parser = argparse.ArgumentParser(description='Starts a \
                server listening on various ports')
    parser.add_argument('startport', type=int, help='starting port \
                where the server listen to')
    parser.add_argument('numports', type=int, help='number of ports \
                to listen to')
    parser.add_argument('--thread', '-t', action='store_true', help='Use threads')
    parser.add_argument('--process', '-p', action='store_true', help='Use processes')
    args = parser.parse_args()
    if args.thread and args.process:
        print("Only one option between thread and process can be specified")
        sys.exit(1)
    return args


if __name__ == "__main__":
    args = handle_options()
    ports = range(args.startport, args.startport+args.numports)
    start_server = Process if args.process else threading.Thread
    socketservers = []
    for port in ports:
        print("Starting {0} on port: {1}".format("thread" if args.thread else "process", port))
        try:
            server = SocketServer('localhost', port)
            socketservers.append(start_server(target=asyncore.loop))
        except socket.error as e:
            print(e)
            continue

    for sserver in socketservers:
        sserver.start()

    while socketservers:
        socketservers.pop().join()
