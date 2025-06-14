# 🏨 Hotel Booking and Management System – Relational to NoSQL Migration

This project demonstrates the migration of a relational PostgreSQL database to a NoSQL MongoDB document store. It simulates a hotel booking system with guests, rooms, bookings, and payments, showcasing how a normalized relational model can be transformed into an embedded NoSQL model using Python.

---

## 📌 Project Objectives

- Design a relational database with integrity constraints and relationships.
- Populate the database with realistic data.
- Choose and justify a suitable NoSQL database.
- Migrate the data programmatically from PostgreSQL to MongoDB.
- Translate relational models into document-based structures.
- Document and demonstrate the migration process.

---

## 🧱 Technologies Used

| Tool         | Purpose                                 |
|--------------|------------------------------------------|
| PostgreSQL   | Relational Database                      |
| MongoDB      | NoSQL Database (Document model)          |
| Python       | Data migration scripting                 |
| psycopg2     | PostgreSQL client for Python             |
| pymongo      | MongoDB client for Python                |
| MongoDB Compass | GUI for MongoDB                       |

---

## 🗃️ Database Design

### ✅ Relational Model (PostgreSQL)

Tables:
- `guests`: stores guest details
- `rooms`: stores room info and pricing
- `bookings`: tracks room reservations
- `payments`: links to bookings with payment info

Relationships:
- Each booking links a guest and a room
- Each payment links to one booking

### ✅ NoSQL Model (MongoDB)

Each document in the `guests` collection includes:
- Guest information
- Embedded array of `bookings`
  - Each booking includes room details
  - If available, embedded payment info

---

## 🔄 Data Migration

### 📜 Migration Script

- Connects to PostgreSQL
- Extracts and joins data across tables
- Converts SQL rows into MongoDB documents
- Inserts documents into the `hotel_mongo.guests` collection

### ▶️ Run Instructions

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
