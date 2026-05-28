from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from aircraft_store import get_all_aircraft

app = FastAPI()

#So Cors is a browser security setting which is blocking the planes from popping up on the frontend.
# This allows all origins to access the API, which is fine for development but should be restricted in production.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/planes")
def planes():
    return get_all_aircraft()