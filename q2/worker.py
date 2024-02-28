import socket 
import pickle  
import threading  

class TaskQueueWorker:
    # initializing host and port
    def __init__(self, host, port): 
        self.host = host 
        self.port = port

   # starts the worker node
    def start(self): 
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: # making socket
            s.bind((self.host, self.port))  # binding
            s.listen()  # listening
            print(f"Worker listening on {self.host}:{self.port}") 

            while True:
                conn, addr = s.accept()  # accepting a connection
                with conn:
                    print(f"Connected by {addr}")  
                    data = conn.recv(4096)  # receiving data from the connection
                    task = pickle.loads(data)  # pickling data to get task
                    result = self.executeTask(task)  # execute the task and store result
                    conn.sendall(pickle.dumps(result))  # unpickling the result and sending it back

    # executes the task
    def executeTask(self, task):
        function = task['function']  # get function to be executed from the task
        args = task['args']  # get the arguments for the function
        kwargs = task['kwargs']  # get the keyword arguments for the function
        result = function(*args, **kwargs)  # call function withe arguments and keyword arguments and storing the result
        return result  

# testing
def add(a, b):
    return a + b

if __name__ == "__main__":
    # create worker nodes instances
    worker1 = TaskQueueWorker('localhost', 5000)  
    worker2 = TaskQueueWorker('localhost', 5001)  
    # start threads for node instances
    threading.Thread(target=worker1.start).start() 
    threading.Thread(target=worker2.start).start()  
