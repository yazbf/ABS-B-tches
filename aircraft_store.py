from collections import defaultdict
import time

aircraft = defaultdict(dict)

def update_aircraft(msg):

    address = msg.get("address")

    if not address:
        return

    plane = aircraft[address]

    # Save previous position before overwriting
    if "latitude" in plane and "longitude" in plane:

        plane["prev_latitude"] = plane["latitude"]
        plane["prev_longitude"] = plane["longitude"]
        plane["prev_time"] = plane.get("last_seen")

    # Update fields
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

def get_aircraft(icao):
    return aircraft.get(icao)