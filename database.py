# database.py
import sqlite3

def setup_database():
    connection = sqlite3.connect('game_save.db')
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS game_state (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        player_name TEXT,
        level INTEGER,
        score INTEGER,
        inventory TEXT
    )
    ''')
    connection.commit()
    connection.close()

def save_game(player_name, level, score, inventory):
    connection = sqlite3.connect('game_save.db')
    cursor = connection.cursor()
    inventory_str = ','.join(inventory)
    cursor.execute('''
    INSERT INTO game_state (player_name, level, score, inventory)
    VALUES (?, ?, ?, ?)
    ''', (player_name, level, score, inventory_str))
    connection.commit()
    connection.close()
    print("Game saved successfully!")

def load_game():
    connection = sqlite3.connect('game_save.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM game_state ORDER BY id DESC LIMIT 1')
    row = cursor.fetchone()
    connection.close()
    if row:
        inventory = row[4].split(',')
        return {
            'player_name': row[1],
            'level': row[2],
            'score': row[3],
            'inventory': inventory
        }
    else:
        print("No save data found!")
        return None
