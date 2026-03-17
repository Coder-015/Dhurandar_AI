import sqlite3
import json
import datetime
import os

DB_FILE = 'dhurandar_logs.db'

class LogGenerator:
    """Log generator and storage system for DhurandarAI."""
    
    def __init__(self, db_path=DB_FILE):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initialize the SQLite database schema."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS security_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                device TEXT NOT NULL,
                event TEXT NOT NULL,
                value REAL,
                severity TEXT NOT NULL,
                raw_json TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def generate_log(self, device, event, value, severity):
        """Generate a simulated log entry and save it to the database."""
        timestamp = datetime.datetime.utcnow().isoformat() + "Z"
        
        log_entry = {
            "timestamp": timestamp,
            "device": device,
            "event": event,
            "value": value,
            "severity": severity
        }
        
        # Store in database
        self._save_to_db(log_entry)
        
        # Output as JSON string
        json_log = json.dumps(log_entry)
        print(f"[LOG GENERATED] {json_log}")
        return json_log
        
    def _save_to_db(self, log_dict):
        """Save a log dictionary to the SQLite database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            '''INSERT INTO security_logs (timestamp, device, event, value, severity, raw_json) 
               VALUES (?, ?, ?, ?, ?, ?)''',
            (
                log_dict['timestamp'],
                log_dict['device'],
                log_dict['event'],
                log_dict['value'],
                log_dict['severity'],
                json.dumps(log_dict)
            )
        )
        conn.commit()
        conn.close()
        
    def get_recent_logs(self, limit=10):
        """Retrieve recent logs from the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT raw_json FROM security_logs ORDER BY id DESC LIMIT ?', (limit,))
        rows = cursor.fetchall()
        conn.close()
        return [json.loads(row[0]) for row in rows]

if __name__ == '__main__':
    # Simple test when run directly
    logger = LogGenerator()
    logger.generate_log("fw1", "PORT_SCAN", 0, "medium")
