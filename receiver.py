from websockets.sync.client import connect
import json

from aircraft_store import update_aircraft

WS_URL = "ws://192.87.172.82:1338"

def receive_data():

    with connect(WS_URL) as websocket:

        print("Connected to websocket")

        while True:

            try:
                msg = websocket.recv()
                msg = json.loads(msg)

                update_aircraft(msg)

            except json.JSONDecodeError:
                print("Bad JSON packet")

            except Exception as e:
                print("Receiver error:", e)
                break


if __name__ == "__main__":
    receive_data()