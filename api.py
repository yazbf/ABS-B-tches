from fastapi import FastAPI
from aircraft_store import (
    get_all_aircraft,
    get_aircraft
)

from predict import estimate_fall

app = FastAPI()

@app.get("/planes")
def planes():
    return get_all_aircraft()

@app.get("/predict/{icao}")
def predict(icao: str):

    plane = get_aircraft(icao)

    if not plane:
        return {"error": "Plane not found"}

    prediction = estimate_fall(plane)

    if not prediction:
        return {"error": "Not enough data"}

    return prediction