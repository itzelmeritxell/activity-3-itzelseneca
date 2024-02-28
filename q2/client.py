import socket
import pickle

class TaskQueueClient:
    def __init__(self, workerNodes): # initializing workernodes
        self.workerNodes = workerNodes

    def distributeTask(self, task): # distributes a task to worker nodes
        results = [] # will hold results

        # go through nodes
        for node in self.workerNodes:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                try:
                    s.connect(node) # connect to the worker node
                    s.sendall(pickle.dumps(task)) # send the task serialized using pickle
                    data = s.recv(4096) # receive the result from the worker node
                    result = pickle.loads(data)
                    results.append(result) # add the result to the results list
                except Exception as e: # handle any errors
                    print(f"Error executing task on {node}: {e}")
        return results

# testing
if __name__ == "__main__":
    from worker import add
    
    # define tasks
    task1 = {'function': add, 'args': (5, 3), 'kwargs': {}}
    task2 = {'function': add, 'args': (10, 20), 'kwargs': {}}

    # create client and distribute tasks
    client = TaskQueueClient([('localhost', 5000), ('localhost', 5001)])
    results = client.distributeTask(task1)
    print("Results of task 1:", results)
    results = client.distributeTask(task2)
    print("Results of task 2:", results)
