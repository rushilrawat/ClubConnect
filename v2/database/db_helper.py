# database/db_helper.py

import sqlite3

DB_PATH = 'database/clubconnect.db'

def create_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn

def initialize_database():
    conn = create_connection()
    cursor = conn.cursor()

    # Create members table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS members (
        member_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT,
        phone_no TEXT,
        dob TEXT,
        gender TEXT,
        admission_no TEXT,
        class_year TEXT,
        section TEXT,
        club_name TEXT
    )
    """)

    # Create awards table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS awards (
        award_id INTEGER PRIMARY KEY AUTOINCREMENT,
        member_id INTEGER,
        competition_name TEXT,
        category TEXT,
        year TEXT,
        prize TEXT,
        FOREIGN KEY (member_id) REFERENCES members (member_id)
    )
    """)

    # Create users table (for login)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
    """)

    # Insert default admin if table is empty
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            INSERT INTO users (username, password) VALUES (?, ?)
        """, ("admin", "admin123"))

    conn.commit()
    conn.close()

# ========== MEMBER FUNCTIONS ==========
def add_member(name, email, phone_no, dob, gender, admission_no, class_year, section, club_name):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO members (name, email, phone_no, dob, gender, admission_no, class_year, section, club_name)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (name, email, phone_no, dob, gender, admission_no, class_year, section, club_name))
    conn.commit()
    conn.close()

def get_all_members():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM members")
    members = cursor.fetchall()
    conn.close()
    return members

def update_member(member_id, name, email, phone_no, dob, gender, admission_no, class_year, section, club_name):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE members 
        SET name=?, email=?, phone_no=?, dob=?, gender=?, admission_no=?, class_year=?, section=?, club_name=?
        WHERE member_id=?
    """, (name, email, phone_no, dob, gender, admission_no, class_year, section, club_name, member_id))
    conn.commit()
    conn.close()

def delete_member(member_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM members WHERE member_id=?", (member_id,))
    conn.commit()
    conn.close()

# ========== AWARD FUNCTIONS ==========
def add_award(member_id, competition_name, category, year, prize):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO awards (member_id, competition_name, category, year, prize)
        VALUES (?, ?, ?, ?, ?)
    """, (member_id, competition_name, category, year, prize))
    conn.commit()
    conn.close()

def get_awards_by_member(member_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM awards WHERE member_id=?", (member_id,))
    awards = cursor.fetchall()
    conn.close()
    return awards

def get_all_awards():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM awards")
    awards = cursor.fetchall()
    conn.close()
    return awards

def delete_award(award_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM awards WHERE award_id=?", (award_id,))
    conn.commit()
    conn.close()

# ========== LOGIN FUNCTIONS ==========
def verify_login(username, password):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user is not None

# ========== DASHBOARD UTILITIES ==========
def get_total_members():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM members")
    total = cursor.fetchone()[0]
    conn.close()
    return total

def get_total_awards():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM awards WHERE prize NOT IN ('Participation')")
    total = cursor.fetchone()[0]
    conn.close()
    return total

def get_top_performer():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT m.name, COUNT(a.award_id) as award_count
        FROM members m
        JOIN awards a ON m.member_id = a.member_id
        WHERE a.prize IN ('First', 'Second', 'Third')
        GROUP BY m.name
        ORDER BY award_count DESC
        LIMIT 1
    """)
    top_performer = cursor.fetchone()
    conn.close()
    return top_performer if top_performer else ("No Awards Yet", 0)

if __name__ == "__main__":
    initialize_database()