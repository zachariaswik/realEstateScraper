import sqlite3

def create_table():
    conn = sqlite3.connect('pisos_listings.db')
    cursor = conn.cursor()
    # Potentially add id as primary key here...
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS listings (
        listingName PRIMARY KEY,
        location TEXT,
        price INTEGER,
        rooms INTEGER,
        bathrooms INTEGER,
        size INTEGER,
        floor TEXT,
        type TEXT
    )
    ''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_table()
