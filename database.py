import sqlite3

DB_NAME = 'cinema.db'

def setup_database():
    """Creates the database and default tables if they don't exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Create Movies Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            price INTEGER NOT NULL
        )
    ''')
    
    # Create Bookings Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            movie_id INTEGER,
            seat_number TEXT,
            user_name TEXT,
            FOREIGN KEY(movie_id) REFERENCES movies(id)
        )
    ''')
    
    # Add dummy data if empty
    cursor.execute('SELECT count(*) FROM movies')
    if cursor.fetchone()[0] == 0:
        movies = [
            ('Avengers: Secret Wars', 250),
            ('Pushpa 2: The Rule', 200),
            ('Interstellar (Re-release)', 300),
            ('The Batman Part II', 220)
        ]
        cursor.executemany('INSERT INTO movies (title, price) VALUES (?, ?)', movies)
        conn.commit()
        print("Database initialized.")
        
    conn.close()

def get_all_movies():
    """Fetches all movies to display in the list."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, price FROM movies")
    data = cursor.fetchall()
    conn.close()
    return data

def get_movie_details(movie_id):
    """Gets the title and price for a specific movie ID."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT price, title FROM movies WHERE id=?", (movie_id,))
    data = cursor.fetchone()
    conn.close()
    return data

def get_booked_seats(movie_id):
    """Returns a list of occupied seats for a specific movie."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT seat_number FROM bookings WHERE movie_id=?", (movie_id,))
    data = [row[0] for row in cursor.fetchall()]
    conn.close()
    return data

def add_booking(movie_id, seat, user_name):
    """Saves a new booking to the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO bookings (movie_id, seat_number, user_name) VALUES (?, ?, ?)", 
                   (movie_id, seat, user_name))
    conn.commit()
    conn.close()