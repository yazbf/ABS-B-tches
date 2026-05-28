from geopy.distance import geodesic

def calculate_speed(prev_pos, new_pos, dt):

    distance_m = geodesic(prev_pos, new_pos).meters

    return distance_m / dt
import math

GRAVITY = 9.81

def estimate_fall_distance(
    altitude_m,
    speed_mps
):

    time_to_ground = math.sqrt(
        (2 * altitude_m) / GRAVITY
    )

    horizontal_distance = (
        speed_mps * time_to_ground
    )

    return horizontal_distance