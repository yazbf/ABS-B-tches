import threading

from receiver import receive_data

def start_receiver():
    receive_data()

thread = threading.Thread(target=start_receiver)
thread.start()
thread.join() #Wait for the receiver thread to finish (it won't, but this keeps the main thread alive)

# API is launched separately with uvicorn
#use uvicorn api:app --reload