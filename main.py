import threading

from receiver import receive_data

def start_receiver():
    receive_data()

thread = threading.Thread(target=start_receiver)
thread.start()

# API is launched separately with uvicorn