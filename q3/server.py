import socket
import threading
import pickle

class ChatServer:
    def __init__(self):
        # initializing ChatServer class with host, port, server_socket, clients list, and lock
        self.host = 'localhost'
        self.port = 9999
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []
        self.lock = threading.Lock()

    def start(self):
        try:
            # binding server socket to host and port
            self.serverSocket.bind((self.host, self.port))
            # listening for connections
            self.serverSocket.listen(5)
            print("Server is listening on {}:{}".format(self.host, self.port))

            # creating a thread to accept clients
            acceptThread = threading.Thread(target=self.acceptClients)
            acceptThread.start()
            acceptThread.join()  # join threads
        finally:
            # closing server socket
            self.serverSocket.close()

    def acceptClients(self):
        while True:
            # accepting client connection
            clientSocket, clientAddress = self.serverSocket.accept()
            print("Connection from", clientAddress)
            self.clients.append(clientSocket)

            # creating a thread to handle the client
            clientThread = threading.Thread(target=self.handleClient, args=(clientSocket,))
            clientThread.start()

    def handleClient(self, clientSocket):
        try:
            # getting client address
            clientAddress = clientSocket.getpeername()
            while True:
                data = clientSocket.recv(1024)
                if not data:
                    break  # if recv() returns an empty bytes object, the client has disconnected

                # getting client message on the server side and displaying it   
                senderPort, message = pickle.loads(data) 
                print(f"Message from client {clientAddress}: {message}")

                # broadcasting client message across clients
                self.broadcast(data, clientSocket)

        except ConnectionResetError:
            # handle client disconnecting abruptly (closing the terminal)
            self.removeClient(clientSocket, clientAddress)
        except Exception as e:
            print(e)
        finally:
            self.removeClient(clientSocket, clientAddress)

    # broadcasting a message to all clients except the sender
    def broadcast(self, data, senderSocket):
        with self.lock:
            for client in self.clients:
                if client != senderSocket:
                    try:
                        client.send(data)
                    except Exception as e:
                        # if an error occurs while sending data to a client, remove the client
                        print(e)
                        self.removeClient(client)

    # removing a client from the list of active clients
    def removeClient(self, clientSocket, clientAddress):
        with self.lock:
            if clientSocket in self.clients:
                self.clients.remove(clientSocket)
                # closing the client socket
                clientSocket.close()
                print(f"Client {clientAddress} disconnected. Total clients:", len(self.clients))


if __name__ == "__main__":
    server = ChatServer()
    server.start()
