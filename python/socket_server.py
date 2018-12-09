# Based on the asyncore code at https://pymotw.com/2/asyncore/#servers
# I've done this with multiprocessing.Process but it could have been made 
# with threading.Thread too
from multiprocessing import Process
import asyncore
import socket
import sys


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


if __name__ == "__main__":
    ports = range(65000, 65050)
    socketservers = []
    for port in ports:
        print("Starting thread on port: ", port)
        try:
            server = SocketServer('localhost', port)
            socketservers.append(Process(target=asyncore.loop))
        except socket.error as e:
            print(e)
            continue

    for sserver in socketservers:
        sserver.start()

    while socketservers:
        socketservers.pop().join()
