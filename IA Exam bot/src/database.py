"""
Database operations for DHS IA Exam Bot
"""

import sqlite3
from pathlib import Path
from datetime import datetime
from config.settings import DATABASE_PATH


class Database:
    """Database management class"""
    
    def __init__(self, db_path=DATABASE_PATH):
        self.db_path = db_path
        self.connection = None
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables"""
        self.connection = sqlite3.connect(self.db_path)
        cursor = self.connection.cursor()
        
        # Create applications table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                status TEXT DEFAULT 'DRAFT',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                submission_date TIMESTAMP
            )
        """)
        
        # Create exam results table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS exam_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                exam_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                score INTEGER,
                passed BOOLEAN,
                time_taken_minutes INTEGER,
                attempt_number INTEGER,
                category TEXT,
                FOREIGN KEY (user_id) REFERENCES applications(user_id)
            )
        """)
        
        # Create exam answers table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS exam_answers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                result_id INTEGER NOT NULL,
                question_id INTEGER,
                user_answer TEXT,
                correct_answer TEXT,
                is_correct BOOLEAN,
                FOREIGN KEY (result_id) REFERENCES exam_results(id)
            )
        """)
        
        # Create audit log table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                action TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                details TEXT
            )
        """)
        
        self.connection.commit()
    
    def add_application(self, user_id, name, email):
        """Add a new application"""
        cursor = self.connection.cursor()
        try:
            cursor.execute("""
                INSERT INTO applications (user_id, name, email, status)
                VALUES (?, ?, ?, 'DRAFT')
            """, (user_id, name, email))
            self.connection.commit()
            self.log_action(user_id, "APPLICATION_CREATED", f"Application created for {name}")
            return True
        except sqlite3.IntegrityError:
            return False
    
    def get_application(self, user_id):
        """Retrieve an application"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM applications WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        if row:
            columns = [col[0] for col in cursor.description]
            return dict(zip(columns, row))
        return None
    
    def update_application_status(self, user_id, status):
        """Update application status"""
        cursor = self.connection.cursor()
        cursor.execute("""
            UPDATE applications 
            SET status = ?, updated_at = CURRENT_TIMESTAMP
            WHERE user_id = ?
        """, (status, user_id))
        self.connection.commit()
        self.log_action(user_id, "STATUS_UPDATED", f"Status changed to {status}")
    
    def save_exam_result(self, user_id, score, passed, time_taken, attempt_num, category):
        """Save exam result"""
        cursor = self.connection.cursor()
        cursor.execute("""
            INSERT INTO exam_results (user_id, score, passed, time_taken_minutes, attempt_number, category)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, score, passed, time_taken, attempt_num, category))
        self.connection.commit()
        result_id = cursor.lastrowid
        
        status = "PASSED" if passed else "FAILED"
        self.log_action(user_id, "EXAM_COMPLETED", f"Exam completed with score {score} - {status}")
        
        return result_id
    
    def save_exam_answers(self, result_id, answers):
        """Save exam answers"""
        cursor = self.connection.cursor()
        for answer in answers:
            cursor.execute("""
                INSERT INTO exam_answers (result_id, question_id, user_answer, correct_answer, is_correct)
                VALUES (?, ?, ?, ?, ?)
            """, (result_id, answer['question_id'], answer['user_answer'], 
                  answer['correct_answer'], answer['is_correct']))
        self.connection.commit()
    
    def get_exam_history(self, user_id):
        """Get exam history for a user"""
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT * FROM exam_results 
            WHERE user_id = ?
            ORDER BY exam_date DESC
        """, (user_id,))
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in rows]
    
    def log_action(self, user_id, action, details):
        """Log an action"""
        cursor = self.connection.cursor()
        cursor.execute("""
            INSERT INTO audit_log (user_id, action, details)
            VALUES (?, ?, ?)
        """, (user_id, action, details))
        self.connection.commit()
    
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
