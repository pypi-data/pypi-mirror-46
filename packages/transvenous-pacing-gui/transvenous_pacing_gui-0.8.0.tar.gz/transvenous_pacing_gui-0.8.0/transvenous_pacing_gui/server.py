import socket
import threading

from queue import Queue

class Server:

    def __init__(self, port, host=socket.gethostname()):
        self.host = host
        self.port = port

    def start(self, queue):
        print("Starting Server Socket")
        self.server = socket.socket()
        self.server.bind((self.host, self.port))
        self.server.listen(5)
        
        self.server_thread = threading.Thread(target=self.listen, args=(queue,))
        self.server_thread.start()

        return self.server_thread

    def stop(self):
        print("Closing connection with client...")
        self.stop_accept()
        self.server_thread.join()
        self.connection.close()

    def receive_data(self, connection, address, queue):
        message = connection.recv(1024)

        queue.put(message)
        
        return message

    def set_hostname(self, host):
        self.host = host

    def get_hostname(self):
        return self.host

    def listen(self, queue):
        (self.connection, self.address) = self.server.accept()
        print("Connection established with client...")

        while True:
            message = self.receive_data(self.connection, self.address, queue)

            if message == b'close':
                break

    def stop_accept(self):
        try:
            with socket.socket() as tmp_client:
                tmp_client.connect((self.host, self.port))
                stop_message = "close"
                tmp_client.send(stop_message.encode())
                print("Forcing server closed")
        except Exception as e:
            print(e)

if __name__ == '__main__':
    queue = Queue()

    test_server = Server(port=911)
    test_server.start(queue)

    message = ''

    while True:
        if not queue.empty():
            message = queue.get()
            print(message)

            if message == b'close':
                break

    test_server.stop()
