import socket
import threading
import pickle

class ChatClient:
    def __init__(self):
        # initialize client 
        self.host = 'localhost'
        self.port = 9999
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        # connect to the server
        self.clientSocket.connect((self.host, self.port))
        
        # tart a thread to receive messages from the server
        receiveThread = threading.Thread(target=self.receiveMessages)
        receiveThread.start()

        # continuously send messages to the server
        while True:
            message = input()
            self.sendMessage(message)

    def receiveMessages(self):
        # continuously receive messages from the server
        while True:
            try:
                data = self.clientSocket.recv(1024)
                if not data:
                    break
                senderPort, message = pickle.loads(data)
                print(f"Message from client {senderPort}: {message}")
            except Exception as e:
                print(e)
                break

    def sendMessage(self, message):
        # send a message to the server
        try:
            senderPort = self.clientSocket.getsockname()[1]
            data = pickle.dumps((senderPort, message))  # include sender's port with the message
            self.clientSocket.send(data)
        except Exception as e:
            print(e)

if __name__ == "__main__":
    client = ChatClient()
    client.start()
