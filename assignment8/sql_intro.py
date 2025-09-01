import sqlite3
from sqlite3 import Error


# Task 3: Populate Tables with Data
def add_publisher(cursor, publisher_name):
    try:
        cursor.execute(
            "INSERT INTO publishers (publisher_name) VALUES (?)", (publisher_name,))
    except sqlite3.IntegrityError:
        print(f"{publisher_name} is already in the database.")


def add_magazine(cursor, magazine_name, publisher_id):
    try:
        cursor.execute(
            "INSERT INTO magazines (magazine_name, publisher_id) VALUES (?, ?)", (magazine_name, publisher_id))
    except sqlite3.IntegrityError:
        print(f"{magazine_name} is already in the database.")


def add_subscriber(cursor, subscriber_name, address):
    cursor.execute(
        "SELECT * FROM subscribers WHERE subscriber_name = ? AND address = ?", (subscriber_name, address))
    if cursor.fetchone():
        print(f"{subscriber_name} at {address} already exist.")
        return
    cursor.execute(
        "INSERT INTO subscribers (subscriber_name, address) VALUES (?,?)", 
        (subscriber_name, address))


def register_subscription(cursor, subscriber, magazine, expiration_date):
    cursor.execute(
        "SELECT subscriber_id FROM subscribers WHERE subscriber_name = ?", 
        (subscriber,))
    results = cursor.fetchone()
    if results:
        subscriber_id = results[0]
    else:
        print(f"There was no subscriber named {subscriber}.")
        return
    

    cursor.execute(
        "SELECT magazine_id FROM magazines WHERE magazine_name = ?", 
        (magazine,))
    results = cursor.fetchone()
    if results:
        magazine_id = results[0]
    else:
        print(f"There was no magazine named {magazine}.")
        return
    

    # Check if this subscription already exists
    cursor.execute(
        "SELECT * FROM subscriptions WHERE subscriber_id = ? AND magazine_id = ?",
        (subscriber_id, magazine_id)
    )
    if cursor.fetchone():
        print(f"Subscriber {subscriber} already subscribed to {magazine}.")
        return

    # If not, insert the new subscription
    cursor.execute(
        "INSERT INTO subscriptions (subscriber_id, magazine_id, expiration_date) VALUES (?, ?, ?)", 
        (subscriber_id, magazine_id, expiration_date))


# Task 1: Create a New SQLite Database
try:
    with sqlite3.connect('../db/magazines.db') as conn:
        conn.execute("PRAGMA foreign_keys = 1")
        cursor = conn.cursor()

        # Task 2: Define Database Structure
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS publishers (
            publisher_id INTEGER PRIMARY KEY,
            publisher_name TEXT NOT NULL UNIQUE
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS magazines (
            magazine_id INTEGER PRIMARY KEY,
            magazine_name TEXT NOT NULL UNIQUE,
            publisher_id INTEGER NOT NULL,
            FOREIGN KEY (publisher_id) REFERENCES publishers(publisher_id) ON UPDATE CASCADE
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS subscribers (
            subscriber_id INTEGER PRIMARY KEY,
            subscriber_name TEXT NOT NULL,
            address TEXT NOT NULL
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS subscriptions (
            subscription_id INTEGER PRIMARY KEY,
            subscriber_id INTEGER NOT NULL,
            magazine_id INTEGER NOT NULL,
            expiration_date TEXT NOT NULL,
            FOREIGN KEY (subscriber_id) REFERENCES subscribers(subscriber_id) ON UPDATE CASCADE,
            FOREIGN KEY (magazine_id) REFERENCES magazines(magazine_id) ON UPDATE CASCADE,
            UNIQUE(subscriber_id, magazine_id)
        )
        """)

        # Insert sample data into tables
        add_publisher(cursor, "TechPress")
        add_publisher(cursor, "HealthMedia")
        add_publisher(cursor, "TravelWorld")

        add_magazine(cursor, "Python Monthly", 1)
        add_magazine(cursor, "Fitness Weekly", 2)
        add_magazine(cursor, "Adventure Times", 3)

        add_subscriber(cursor, "Alice", "123 Main St, St.Louis, MO")
        add_subscriber(cursor, "Bob", "456 Oak Ave, Edwardsville, IL")
        add_subscriber(cursor, "Charlie", "789 Pine Rd, Chicago, IL")

        register_subscription(cursor, "Alice", "Python Monthly", "2024-12-31")
        register_subscription(cursor, "Bob", "Fitness Weekly", "2024-11-15")
        register_subscription(cursor, "Charlie", "Adventure Times", "2025-01-20")

        conn.commit()

        # Task 4: Write SQL Queries
        # 4.1. Write a query to retrieve all information from the subscribers table.
        cursor.execute("SELECT * FROM subscribers")
        result = cursor.fetchall()
        for row in result:
            print(row)
    

        # 4.2. Write a query to retrieve all magazines sorted by name.
        cursor.execute("SELECT * FROM magazines ORDER BY magazine_name")
        result = cursor.fetchall()
        for row in result:
            print(row)

        # 4.3. Write a query to find magazines for a particular publisher, one of the publishers you created. This requires a JOIN.
        publisher_name = "TechPress"
        cursor.execute("""
            SELECT m.magazine_name, p.publisher_name 
            FROM magazines as m 
            JOIN publishers as p 
            ON m.publisher_id = p.publisher_id
            WHERE p.publisher_name = ?
        """, (publisher_name,))
        result = cursor.fetchall()
        for row in result:
            print(row)

except Error as e:
    print(f"An error occurred: {e}")
