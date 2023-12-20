import sqlite3

DATABASE_FILE = 'your_database.db'

def initialize_database():
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()

        # Create the Data table if not exists
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id TEXT,
                state TEXT,
                time TEXT,
                sequence_number INTEGER,
                Datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Create the Notification table if not exists
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Notification (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id TEXT,
                message TEXT,
                state TEXT,
                time TEXT
            )
        ''')

        conn.commit()