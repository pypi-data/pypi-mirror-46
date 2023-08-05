import socket

class Client:

    def __init__(self, port, host=socket.gethostname()):
        self.host = host
        self.port = port
        self.client = socket.socket()

    def start(self):
        print("Starting Client Socket")
        
        try:
            self.client.connect((self.host, self.port))
        except:
            print("Unable to connect...")

            return None

    def stop(self):
        stop_message = 'close'
        try:
            self.client.send(stop_message.encode())
            print("Closing connection with server...")
        except Exception as e:
            print(e)

        return True

    def set_hostname(self, host):
        self.host = host

    def get_hostname(self):
        return self.host

    def get_ip(self):
        return socket.gethostbyname(self.host)

    def send_data(self, message):
        try:
            self.client.send(message.encode())
        except:
            print("Unable to send a message...")

            return False

if __name__ == '__main__':
    test_client = Client(port=911)
    test_client.start()

    message = ''

    while True:
        message = input("Enter a message to send: ").lower()

        test_client.send_data(message)
        
        if message == 'close':
            test_client.stop()
            break
