import socket  
import pickle  

# function to serialize file data
def serializeFile(filePath):
    with open(filePath, 'r') as file:  # open the file in read mode
        fileData = {'filename': filePath, 'data': file.read()}  # read the file data and store it along with filename
    return pickle.dumps(fileData)  # serialize the file data using pickle

# function to run the client
def runClient():
    try:
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP socket
        serverAddress = ('127.0.0.1', 12345)  # server address and port
        clientSocket.connect(serverAddress)  # connecting to the server

        filePath = input("Enter the file path of the file to be transferred: ")  # asking user to input file path
        fileToSend = serializeFile(filePath)  # serializing the file to send
        clientSocket.sendall(fileToSend)  # sending the serialized file to the server

        print("File sent successfully.")  
        
    except Exception as err: 
        print(f"Error: {err}")  # Printing the error message if any

    finally:
        clientSocket.close()  # closing the client socket after execution

if __name__ == "__main__":
    runClient()  # calling the function to run the client
