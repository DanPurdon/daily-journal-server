import sqlite3
import json
from models import Entry, Mood

def get_all_entries():
    # Open a connection to the database
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:

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
            a.date,
            m.label mood_label
        FROM journal_entries a
        JOIN moods m
            ON a.mood_id = m.id
                """)

        # Initialize an empty list to hold all entry representations
        entries = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:
            # Create an entry instance from the current row
            entry = Entry(row['id'], row['concept'], row['entry'], row['mood_id'],
                            row['date'])

            # Create a Location instance from the current row
            mood = Mood(row['mood_id'], row['mood_label'])
            # customer = Customer(row['customer_id'], row['customer_name'], row['customer_address'], row['customer_email'], row['customer_password'])
            

            # Add the dictionary representation of the location to the entry
            entry.mood = mood.__dict__
            # entry.customer = customer.__dict__

            # Add the dictionary representation of the entry to the list
            entries.append(entry.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(entries)

def get_single_entry(id):
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            a.id,
            a.concept,
            a.entry,
            a.mood_id,
            a.date
        FROM journal_entries a
        WHERE a.id = ?
        """, ( id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an entry instance from the current row
        entry = Entry(data['id'], data['concept'], data['entry'], data['mood_id'],
                            data['date'])

        return json.dumps(entry.__dict__)

def delete_entry(id):
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM journal_entries
        WHERE id = ?
        """, (id, ))

def get_entries_with_search(term):

    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        select
            a.id,
            a.concept,
            a.entry,
            a.mood_id,
            a.date
        FROM journal_entries a
        WHERE a.entry LIKE ? 
        """, ( f"%{term}%", ))

        entries = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            entry = Entry(row['id'], row['concept'], row['entry'], row['mood_id'],
                            row['date'])
            entries.append(entry.__dict__)

    return json.dumps(entries)