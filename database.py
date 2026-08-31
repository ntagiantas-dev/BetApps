# database.py
import sqlite3
import json

class LiveStatDatabase:
    def __init__(self, db_name="livestatarena.db"):
        self.db_name = db_name
        self.init_db()

    def get_connection(self):
        return sqlite3.connect(self.db_name)

    def init_db(self):
        """
        Δημιουργεί τους πίνακες στη βάση δεδομένων αν δεν υπάρχουν:
        - teams_pregame: Για τα στατιστικά και pregame data των 5 ομάδων.
        - live_matches_log: Για τα live rows και τα xG ανά λεπτό/φάση για τα γραφικά.
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        # Πίνακας για Pregame Data
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS teams_pregame (
                team_name TEXT PRIMARY KEY,
                country TEXT,
                form_data TEXT,
                xg_avg REAL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Πίνακας για Live Rows & xG (για γραφικά)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS live_matches_log (
                match_id TEXT,
                minute INTEGER,
                home_team TEXT,
                away_team TEXT,
                home_xg REAL,
                away_xg REAL,
                possession_json TEXT,
                raw_data TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()
        conn.close()

    def save_pregame_data(self, team_name, country, form_data, xg_avg):
        """Αποθηκεύει ή ενημερώνει τα pregame data μιας ομάδας."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO teams_pregame (team_name, country, form_data, xg_avg)
            VALUES (?, ?, ?, ?)
        """, (team_name, country, json.dumps(form_data), xg_avg))
        conn.commit()
        conn.close()

    def log_live_row(self, match_id, minute, home_team, away_team, home_xg, away_xg, possession_dict, raw_data):
        """
        Καταγράφει μια γραμμή live δεδομένων (Live Row), 
        συμπεριλαμβανομένων των xG για να τροφοδοτήσει τα γραφικά.
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO live_matches_log 
            (match_id, minute, home_team, away_team, home_xg, away_xg, possession_json, raw_data)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            match_id, 
            minute, 
            home_team, 
            away_team, 
            home_xg, 
            away_xg, 
            json.dumps(possession_dict), 
            json.dumps(raw_data)
        ))
        conn.commit()
        conn.close()

    def get_match_xg_history(self, match_id):
        """
        Επιστρέφει την ιστορική εξέλιξη των xG για έναν αγώνα, 
        ιδανικό για τη δημιουργία γραφημάτων (charts) στον χρήστη.
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT minute, home_xg, away_xg FROM live_matches_log 
            WHERE match_id = ? ORDER BY minute ASC
        """, (match_id,))
        rows = cursor.fetchall()
        conn.close()
        
        # Μορφοποίηση δεδομένων έτοιμη για γράφημα
        history = [{"minute": r[0], "home_xg": r[1], "away_xg": r[2]} for r in rows]
        return history