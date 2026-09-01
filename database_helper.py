import sqlite3
import os
from werkzeug.security import generate_password_hash

DB_PATH = os.path.join(os.path.dirname(__file__), 'database', 'event.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Registrations table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS registrations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        registration_id TEXT UNIQUE NOT NULL,
        full_name TEXT NOT NULL,
        mobile TEXT UNIQUE NOT NULL,
        email TEXT NOT NULL,
        college_id TEXT UNIQUE NOT NULL,
        department TEXT NOT NULL,
        year TEXT NOT NULL,
        blood_group TEXT NOT NULL,
        age INTEGER NOT NULL,
        gender TEXT NOT NULL,
        preferred_slot TEXT NOT NULL,
        emergency_name TEXT NOT NULL,
        emergency_phone TEXT NOT NULL,
        address TEXT,
        registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        status TEXT DEFAULT 'Registered'
    )
    ''')

    # 2. Volunteers table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS volunteers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        college_id TEXT NOT NULL,
        department TEXT NOT NULL,
        year TEXT NOT NULL,
        phone TEXT NOT NULL,
        preferred_role TEXT NOT NULL,
        registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        status TEXT DEFAULT 'Active'
    )
    ''')

    # 3. Admins table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS admins (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        name TEXT NOT NULL,
        role TEXT DEFAULT 'Coordinator'
    )
    ''')

    # Insert default admin if not exists (username: admin, password: admin@griet2026)
    cursor.execute('SELECT id FROM admins WHERE username = ?', ('admin',))
    if not cursor.fetchone():
        hashed_pw = generate_password_hash('admin@griet2026')
        cursor.execute(
            'INSERT INTO admins (username, password_hash, name, role) VALUES (?, ?, ?, ?)',
            ('admin', hashed_pw, 'NSS GRIET Coordinator', 'Event Lead')
        )

    # Insert sample seed data if table is empty
    cursor.execute('SELECT COUNT(*) as count FROM registrations')
    reg_count = cursor.fetchone()['count']
    if reg_count == 0:
        sample_donors = [
            ('GRIET-BD-0001', 'Rahul Sharma', '9876543210', 'rahul.s@griet.in', '22241A0501', 'Computer Science & Engineering', '3rd Year', 'O+', 20, 'Male', '09:30 AM - 10:30 AM', 'Suresh Sharma', '9876543200', 'Hyderabad', 'Registered'),
            ('GRIET-BD-0002', 'Sneha Reddy', '9876543211', 'sneha.r@griet.in', '23241A1205', 'Information Technology', '2nd Year', 'A+', 19, 'Female', '10:30 AM - 11:30 AM', 'Venkat Reddy', '9876543201', 'Bachupally, Hyderabad', 'Confirmed'),
            ('GRIET-BD-0003', 'Vikram Varma', '9876543212', 'vikram.v@griet.in', '21241A0410', 'Electronics & Communication', '4th Year', 'B+', 21, 'Male', '11:30 AM - 12:30 PM', 'Anil Varma', '9876543202', 'Kukatpally', 'Registered'),
            ('GRIET-BD-0004', 'Ananya Patel', '9876543213', 'ananya.p@griet.in', '22241A0215', 'Electrical & Electronics', '3rd Year', 'AB+', 20, 'Female', '01:30 PM - 02:30 PM', 'Rajesh Patel', '9876543203', 'Miyapur', 'Confirmed'),
            ('GRIET-BD-0005', 'Karthik Rao', '9876543214', 'karthik.r@griet.in', '24241A0308', 'Mechanical Engineering', '1st Year', 'O-', 18, 'Male', '02:30 PM - 03:30 PM', 'Ramesh Rao', '9876543204', 'Nizampet', 'Registered'),
            ('GRIET-BD-0006', 'Dr. P. Srinivas', '9876543215', 'srinivas.p@griet.in', 'EMP-CSE-104', 'Computer Science & Engineering', 'Faculty / Staff', 'A-', 38, 'Male', '10:30 AM - 11:30 AM', 'Lakshmi P', '9876543205', 'Pragathi Nagar', 'Confirmed')
        ]
        cursor.executemany('''
        INSERT INTO registrations (
            registration_id, full_name, mobile, email, college_id, department,
            year, blood_group, age, gender, preferred_slot, emergency_name,
            emergency_phone, address, status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', sample_donors)

    cursor.execute('SELECT COUNT(*) as count FROM volunteers')
    vol_count = cursor.fetchone()['count']
    if vol_count == 0:
        sample_volunteers = [
            ('Sai Teja', '22241A0599', 'Computer Science & Engineering', '3rd Year', '9876500001', 'Registration Desk'),
            ('Pooja K', '23241A1245', 'Information Technology', '2nd Year', '9876500002', 'Donor Assistance'),
            ('Manish G', '21241A0488', 'Electronics & Communication', '4th Year', '9876500003', 'Crowd Management'),
            ('Divya S', '22241A0234', 'Electrical & Electronics', '3rd Year', '9876500004', 'Refreshments')
        ]
        cursor.executemany('''
        INSERT INTO volunteers (name, college_id, department, year, phone, preferred_role)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', sample_volunteers)

    conn.commit()
    conn.close()

def get_next_registration_id():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM registrations ORDER BY id DESC LIMIT 1')
    last_row = cursor.fetchone()
    conn.close()
    
    if last_row:
        next_num = last_row['id'] + 1
    else:
        next_num = 1
    return f"GRIET-BD-{next_num:04d}"
