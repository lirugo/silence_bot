import csv
import os

BOOKINGS_FILE = "bookings.csv"

def _ensure_file():
    if not os.path.exists(BOOKINGS_FILE):
        with open(BOOKINGS_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["date", "time", "user_id", "username"])

def is_slot_available(date: str, time: str) -> bool:
    _ensure_file()
    with open(BOOKINGS_FILE, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["date"] == date and row["time"] == time:
                return False
    return True

def mark_slot_as_booked(date: str, time: str, user_id: int, username: str):
    _ensure_file()
    with open(BOOKINGS_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([date, time, user_id, username or "unknown"])

def get_all_bookings() -> list[tuple[str, str, str, str]]:
    if not os.path.exists(BOOKINGS_FILE):
        return []

    with open(BOOKINGS_FILE, newline="") as f:
        reader = csv.DictReader(f)
        return [(row["date"], row["time"], row["user_id"], row["username"]) for row in reader]

def delete_all_bookings():
    if os.path.exists(BOOKINGS_FILE):
        with open(BOOKINGS_FILE, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["date", "time", "user_id", "username"])
            writer.writeheader()