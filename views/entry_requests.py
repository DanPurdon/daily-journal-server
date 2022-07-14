import sqlite3
import json
from models import Entry

def get_all_entries():
    # Open a connection to the database
    with sqlite3.connect("./kennel.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            a.id,
            a.concept,
            a.entry,
            a.mood_id,
            a.date
        FROM journal_entries a
                """)

        # Initialize an empty list to hold all entry representations
        entries = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:
            # Create an entry instance from the current row
            entry = Entry(row['id'], row['name'], row['breed'], row['status'],
                            row['customer_id'], row['location_id'])

            # Create a Location instance from the current row
            # location = Location(row['location_id'], row['location_name'], row['location_address'])
            # customer = Customer(row['customer_id'], row['customer_name'], row['customer_address'], row['customer_email'], row['customer_password'])
            

            # Add the dictionary representation of the location to the entry
            # entry.location = location.__dict__
            # entry.customer = customer.__dict__

            # Add the dictionary representation of the entry to the list
            entries.append(entry.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(entries)

def get_single_entry(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.breed,
            a.status,
            a.customer_id
            a.location_id
        FROM entry a
        WHERE a.id = ?
        """, ( id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an entry instance from the current row
        entry = Entry(data['id'], data['name'], data['breed'],
                            data['status'], data['customer_id'],
                            data['location_id'])

        return json.dumps(entry.__dict__)