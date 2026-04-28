from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ✅ CORS FIX (VERY IMPORTANT)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# SAMPLE DATA (if not already there)
slots = [
    {"slot_id": 1, "status": "occupied"},
    {"slot_id": 2, "status": "empty"},
    {"slot_id": 3, "status": "occupied"},
    {"slot_id": 4, "status": "empty"},
    {"slot_id": 5, "status": "empty"},
]

@app.get("/slots")
def get_slots():
    return slots

@app.post("/book/{slot_id}")
def book_slot(slot_id: int):
    for slot in slots:
        if slot["slot_id"] == slot_id:
            slot["status"] = "occupied"
    return {"message": "Booked"}