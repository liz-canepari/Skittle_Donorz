# database.py
import sqlite3

def create_connection(db_name="game_data.db"):
    """
    Create a connection to the SQLite database.
    If the database does not exist, it will be created automatically.
    """
    conn = sqlite3.connect(db_name)  # Creates or opens the database file automatically
    return conn

def create_tables():
    """
    Create the necessary tables in the database if they don't already exist.
    """
    conn = create_connection()  # Connect to the SQLite database
    cursor = conn.cursor()  # Create a cursor object to execute SQL commands

    # Create players table (if it doesn't exist already)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            level INTEGER NOT NULL,
            score INTEGER NOT NULL,
            position_x INTEGER,
            position_y INTEGER
        )
    ''')

    # Create inventory table (if it doesn't exist already)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY,
            player_id INTEGER,
            item_name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            FOREIGN KEY (player_id) REFERENCES players(id)
        )
    ''')

    # Create game_saves table (to store checkpoints)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS game_saves (
            id INTEGER PRIMARY KEY,
            player_id INTEGER,
            save_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            checkpoint_x INTEGER,
            checkpoint_y INTEGER,
            FOREIGN KEY (player_id) REFERENCES players(id)
        )
    ''')

    conn.commit()  # Commit the changes to the database
    conn.close() 
    

def save_game(player_id, name, level, score, position_x, position_y):
    """
    Save the player's current game state to the database.
    This function creates the database and tables automatically if they don't exist.
    """
    conn = create_connection()  # Connect to the database (will create if not existing)
    cursor = conn.cursor()

    # Save or update the player's data (id, level, score, position)
    cursor.execute('''
        INSERT OR REPLACE INTO players (id, name, level, score, position_x, position_y)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (player_id, name, level, score, position_x, position_y))

    # Save the checkpoint data (position where player left off)
    cursor.execute('''
        INSERT INTO game_saves (player_id, checkpoint_x, checkpoint_y)
        VALUES (?, ?, ?)
    ''', (player_id, position_x, position_y))

    conn.commit()  # Commit the changes to the database
    conn.close()


def load_game(player_id):
    """
    Load the player's saved game data from the database.
    """
    conn = create_connection()  # Connect to the database
    cursor = conn.cursor()

    # Load player data (level, score, position)
    cursor.execute('SELECT * FROM players WHERE id = ?', (player_id,))
    player_data = cursor.fetchone()

    # Load player's inventory items
    cursor.execute('SELECT * FROM inventory WHERE player_id = ?', (player_id,))
    inventory_data = cursor.fetchall()

    # Load last game save (checkpoint data)
    cursor.execute('SELECT * FROM game_saves WHERE player_id = ? ORDER BY save_time DESC LIMIT 1', (player_id,))
    checkpoint_data = cursor.fetchone()

    conn.close()

    return {
        "player_data": player_data,  # Contains level, score, position
        "inventory_data": inventory_data,  # Contains items and quantities
        "checkpoint_data": checkpoint_data  # Contains checkpoint position
    }
