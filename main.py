from fastapi import FastAPI
import sqlite3

app = FastAPI()

# ✅ Create connection (Render safe)
def get_connection():
    return sqlite3.connect("parking.db")

# ✅ Initialize database
def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Create tables
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS slots (
        id INTEGER PRIMARY KEY,
        status TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        slot_id INTEGER
    )
    """)

    # Insert default slots only if empty
    cursor.execute("SELECT COUNT(*) FROM slots")
    count = cursor.fetchone()[0]

    if count == 0:
        for i in range(1, 6):
            cursor.execute(
                "INSERT INTO slots (id, status) VALUES (?, ?)",
                (i, "empty")
            )

    conn.commit()
    conn.close()

# Run on startup
init_db()

# ---------------- ROUTES ---------------- #

@app.get("/")
def home():
    return {"message": "Backend Running Successfully"}

# ✅ Get all slots
@app.get("/slots")
def get_slots():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM slots")
    data = cursor.fetchall()

    conn.close()

    return [
        {"slot_id": row[0], "status": row[1]}
        for row in data
    ]

# ✅ Update slot manually (for testing)
@app.post("/update/{slot_id}/{status}")
def update_slot(slot_id: int, status: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE slots SET status=? WHERE id=?",
        (status, slot_id)
    )

    conn.commit()
    conn.close()

    return {"message": f"Slot {slot_id} updated to {status}"}

# ✅ Book slot
@app.get("/book/{slot_id}")   # 🔥 changed to GET (matches Flutter)
def book_slot(slot_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT status FROM slots WHERE id=?",
        (slot_id,)
    )
    result = cursor.fetchone()

    if result and result[0] == "empty":
        cursor.execute(
            "INSERT INTO bookings (slot_id) VALUES (?)",
            (slot_id,)
        )
        cursor.execute(
            "UPDATE slots SET status='occupied' WHERE id=?",
            (slot_id,)
        )
        conn.commit()
        conn.close()
        return {"message": "Slot booked successfully"}
    else:
        conn.close()
        return {"message": "Slot already occupied"}