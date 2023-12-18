import firebase_admin
from firebase_admin import credentials, firestore
import sqlite3


cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred)

class DatabaseData:

    # Initializing a connection to a SQLite database and configuring a connection to Firebase
    def __init__(self):
        self.connection = sqlite3.connect("game_history.db")
        self.create_history_table()
        db = firestore.client()
        self.cloud_database = db.collection('game_history').document()
    
    # Getting data from Firebase
    def get_cloud_database(self):
        return self.cloud_database.get()
    
    # Inserting data to Firebase
    def insert_to_cloud_database(self, winner, players):
        data = {
            'winner_name': winner.name,
            'player1_score': players[0].score,
            'player2_score': players[1].score
        }
        self.cloud_database.set(data)
    
    # Creating a game history table in SQLite database
    def create_history_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS game_history (
                game_id INTEGER PRIMARY KEY AUTOINCREMENT,
                game_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                winner_name TEXT,
                player1_score INTEGER,
                player2_score INTEGER
            )
        ''')
        self.connection.commit()
    
    # Retrieve the entire game history from the local SQLite database
    def get_database(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM game_history')
        history = cursor.fetchall()
        return history
    
    # Inserting the game winner and score information into to the local SQLite database
    def insert_to_database(self, winner, players):
        cursor = self.connection.cursor()
        cursor.execute('''
            INSERT INTO game_history (winner_name, player1_score, player2_score)
            VALUES (?, ?, ?)
        ''', (winner.name, players[0].score, players[1].score))
        self.connection.commit()
