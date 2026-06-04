import math

from geopy.distance import geodesic
from geopy.point import Point

GRAVITY = 9.81

def estimate_fall(plane):

    altitude_ft = plane.get("altitude")
    speed_knots = plane.get("speed")
    heading = plane.get("heading") #in degrees, 0 is north, increasing clockwise

    lat = plane.get("latitude")
    lon = plane.get("longitude")

    if None in [altitude_ft, speed_knots, heading, lat, lon]:
        return None

    # Convert units
    altitude_m = altitude_ft * 0.3048
    speed_mps = speed_knots * 0.514444

    # Free fall time
    time_to_ground = math.sqrt(
        (2 * altitude_m) / GRAVITY
    )

    # Horizontal travel distance
    distance_m = speed_mps * time_to_ground

    # Move point along heading
    origin = Point(lat, lon)

#calculate destination point given distance and heading geodesic is used since it accounts for Earth's curvature, which is important for longer distances
    destination = geodesic(
        meters=distance_m
    ).destination(origin, heading)

    return {
        "start": [lat, lon],
        "end": [
            destination.latitude,
            destination.longitude
        ],
        "distance_m": distance_m,
        "fall_time_s": time_to_ground
    }