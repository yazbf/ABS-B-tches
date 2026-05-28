from fastapi import FastAPI
from aircraft_store import get_all_aircraft

app = FastAPI()

@app.get("/planes")
def planes():
    return get_all_aircraft()