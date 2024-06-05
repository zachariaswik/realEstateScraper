import sqlite3

def create_table():
    conn = sqlite3.connect('pisos_listings.db')
    cursor = conn.cursor()
    # Potentially add id as primary key here...
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS listings (
        listingName TEXT PRIMARY KEY,
        location TEXT,
        price INTEGER,
        rooms INTEGER,
        bathrooms INTEGER,
        sizeConstr INTEGER,
        sizeUtil INTEGER,
        sizeSolar INTEGER,
        floor TEXT,
        type TEXT,
        exterior TEXT,
        interior TEXT,
        age TEXT,
        state TEXT,
        reference TEXT,
        communityCost INTEGER,
        description TEXT,
        Erating TEXT,
        CO2rating TEXT,
        Econsumption TEXT,
        CO2emission TEXT,
        last_update TEXT
    )
    ''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_table()
