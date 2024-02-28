import socket 
import pickle  
import os 

# function to save file data to disk
def saveFile(fileData, saveDir):
    filename = os.path.basename(fileData['filename'])  # get filename from the file data
    savePath = os.path.join(saveDir, filename)  # make the complete save path
    
    with open(savePath, 'w') as f:  # open the file in write mode
        f.write(fileData['data'])  # write the file data to the file

    print(f"File saved to: {savePath}")  # print the save path after saving the file

# function to run the server
def runServer():
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP socket
    serverAddress = ('127.0.0.1', 12345)  # server address and port
    serverSocket.bind(serverAddress)  # binding
    serverSocket.listen(1)  # listening

    print("Server listening for incoming connections...")  # print that the server is listening
    
    while True:  #  accept incoming connections while true
        clientSocket, clientAddress = serverSocket.accept()  # accept the incoming connection

        try:
            print("Connected to:", clientAddress)  # print what client the server connected to

            saveDir = input("Enter the directory to save the file: ")  # ask user to input the directory to save the file
            os.makedirs(saveDir, exist_ok=True)  # create the directory if it doesnt exist
            
            fileReceived = clientSocket.recv(4096)  # receive file data from the client
            fileData = pickle.loads(fileReceived)  # deserialize file data
            saveFile(fileData, saveDir)  # save the received file data to disk

        except Exception as e:  
            print(f"Error: {e}")  # print error message if any
        finally:
            clientSocket.close()  # close the client socket 

if __name__ == "__main__":
    runServer()  # call the function to run the server
