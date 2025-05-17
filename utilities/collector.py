import sqlite3

db_path = "database/database.db"

def init_db():
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS collectors (
                user_id TEXT NOT NULL,
                pokemon_name TEXT NOT NULL,
                PRIMARY KEY (user_id, pokemon_name)
            )
        ''')
        conn.commit()

def add_collector(user_id: int, pokemon_name: str):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR IGNORE INTO collectors (user_id, pokemon_name) VALUES (?, ?)",
            (str(user_id), pokemon_name.lower())
        )
        conn.commit()

def get_collectors_for_pokemon(pokemon_name: str):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT user_id FROM collectors WHERE pokemon_name = ?",
            (pokemon_name.lower(),)
        )
        return [int(row[0]) for row in cursor.fetchall()]
