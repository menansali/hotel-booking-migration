import psycopg2
from pymongo import MongoClient
from datetime import date

# PostgreSQL connection
pg_conn = psycopg2.connect(
    dbname="hotelmenagement_db",  # updated database name
    user="postgres",          # <- replace with your PostgreSQL username
    password="",  # <- replace with your PostgreSQL password
    host="localhost",
    port="5432"
)
pg_cursor = pg_conn.cursor()

# MongoDB connection
mongo_client = MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["hotel_mongo"]
mongo_guests = mongo_db["guests"]

# Clear old data if rerunning
mongo_guests.delete_many({})

# Fetch all guests
pg_cursor.execute("SELECT guest_id, name, email, phone FROM guests")
guests = pg_cursor.fetchall()

for guest in guests:
    guest_id, name, email, phone = guest

    # Fetch bookings for the guest
    pg_cursor.execute("""
        SELECT b.booking_id, b.check_in_date, b.check_out_date, b.status,
               r.room_id, r.room_number, r.type, r.price_per_night,
               p.amount, p.payment_date, p.method
        FROM bookings b
        JOIN rooms r ON b.room_id = r.room_id
        LEFT JOIN payments p ON b.booking_id = p.booking_id
        WHERE b.guest_id = %s
    """, (guest_id,))
    
    bookings = []
    for booking in pg_cursor.fetchall():
        (booking_id, check_in, check_out, status,
         room_id, room_number, room_type, price,
         amount, payment_date, method) = booking

        booking_doc = {
            "booking_id": booking_id,
            "check_in_date": check_in.isoformat(),
            "check_out_date": check_out.isoformat(),
            "status": status,
            "room": {
                "room_id": room_id,
                "room_number": room_number,
                "type": room_type,
                "price_per_night": float(price)
            }
        }

        if amount is not None:
            booking_doc["payment"] = {
                "amount": float(amount),
                "payment_date": payment_date.isoformat() if payment_date else None,
                "method": method
            }

        bookings.append(booking_doc)

    # Final guest document
    guest_doc = {
        "guest_id": guest_id,
        "name": name,
        "email": email,
        "phone": phone,
        "bookings": bookings
    }

    # Insert into MongoDB
    mongo_guests.insert_one(guest_doc)

print("✅ Migration completed successfully!")

# Clean up
pg_cursor.close()
pg_conn.close()
mongo_client.close()
