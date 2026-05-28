from collections import defaultdict
import time

aircraft = defaultdict(dict)

def update_aircraft(msg):
    address = msg.get("address")

    if not address:
        return

    plane = aircraft[address]

    # Update fields if they exist
    for field in [
        "latitude",
        "longitude",
        "altitude",
        "speed",
        "heading",
        "callsign"
    ]:
        if field in msg:
            plane[field] = msg[field]

    plane["last_seen"] = time.time()

def get_all_aircraft():
    return aircraft
