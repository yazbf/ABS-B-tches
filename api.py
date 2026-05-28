import threading

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from aircraft_store import (
    get_all_aircraft,
    get_aircraft
)

from receiver import receive_data
from predict import estimate_fall

app = FastAPI()

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Start websocket receiver in background
threading.Thread(
    target=receive_data,
    daemon=True
).start()

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