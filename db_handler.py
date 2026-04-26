# import sqlite3
# import os

# # 1. Path Setup: This ensures the .db file stays in the same folder as this script
# BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# DB_PATH = os.path.join(BASE_DIR, 'scriptorium.db')

# def get_db_connection():
#     try:
#         conn = sqlite3.connect(DB_PATH)
#         # This allows us to access columns by name (e.g., row['name'])
#         conn.row_factory = sqlite3.Row 
#         return conn
#     except Exception as e:
#         print(f"Database connection error: {e}")
#         return None

# def initialize_database():
#     conn = get_db_connection()
#     if not conn: return
#     cursor = conn.cursor()

#     # Create Tables (Note: SQLite uses AUTOINCREMENT instead of AUTO_INCREMENT)
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS subjects (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             name TEXT NOT NULL,
#             year INTEGER NOT NULL,
#             branch TEXT NOT NULL
#         )
#     """)
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS teachers (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             name TEXT NOT NULL,
#             subject_id INTEGER,
#             FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE
#         )
#     """)

#     # Department Data
#     data = {
#         "IT": {
#             2: {
#                 "Operating Systems": ["Pf. Harpreet Kaur", "Dr. Kulvinder Singh Mann", "Dr. Pankaj Bhambri"],
#                 "Object Oriented Programming with Java": ["Dr. Akshay Girdhar", "Pf. Jaspreet Kaur", "Pf. Vandana"],
#                 "Advanced and Emerging Technologies": ["Dr. Amit Kamra", "Dr. Sachin Bagga", "Pf. Sarabmeet Singh"],
#                 "DataBase Management System": ["Pf. Neha Gupta", "Dr. Mohanjit Kaur Kang", "Pf. Gitanjali"],
#                 "Discrete Mathematics": ["Pf. Parminder Kaur Wadhwa", "Pf. Jasleen Kaur"],
#                 "Web Technologies": ["Pf. Himani Sharma", "Dr. Randeep Kaur", "Dr. Palwinder Kaur"]
#             },
#             3: {
#                 "DevOps": ["Dr. Kamaljit Kaur", "Pf. Himani Sharma"],
#                 "DAA ": ["Dr. Randeep Kaur", "Pf. Parminder Kaur Wadhwa"]
#             }
#         },
#         "CSE": {
#             2: {
#                 "Data Analytic Tools": ["Prof. Sita Rani", "Prof. Kapil Sharma" , "Prof. Shailja", "Prof. PreetKamal Singh" ],
#                 "Database Management System ": ["Prof. Jasmin Kaur" , "Prof. Khushi Dhunna" , "Dr. Kiran Jyoti", "Prof. Goldendeep Kaur"],
#                 "Computer Networks ":["Prof. Daljit Singh", "Prof. Palak Sood", "Prof. Satinderpal Singh", "Prof. Haredeep Singh Kang"],
#                 "Artificial Intelligence":["Prof. Jasdeep Kaur", "Prof. Aashish", "Prof. Diana Nagpal" , "Prof. Kawaljeet Kaur"],
#                 "Operating System" : ["Prof. Harkomalpreet", "Prof. Kajal Chugh", "Prof. Lakhvir Kaur", "Prof. Harshim"],
#                 "Environmental Sciences and Sustainability":["Prof. Komalpreet", "Prof. Hitika Dhawan", "Prof.Shreya", "Prof.Sumanpreet"],
#                 "Business Essential for Engineers":["Prof. Sunil Kumar", "Prof. Nisha"]
#             }
#         },
#         "ECE":{
#             2: {
#                 "Computer Networks" : ["Harminder Kaur"],
#                 "Object Oriented Programming & DS": ["Er. Harminder Kaur Aulakh"],
#                 "VHDL" : ["Dr. Gurjot Kaur Walia", "Dr. Navneet Kaur"]
#             }
#         }
#     }

#     # Clear existing data to avoid duplicates on re-run
#     cursor.execute("DELETE FROM teachers")
#     cursor.execute("DELETE FROM subjects")

#     # Insert Logic
#     for branch, years in data.items():
#         for year, subjects in years.items():
#             for subject_name, teachers in subjects.items():
#                 cursor.execute(
#                     "INSERT INTO subjects (name, year, branch) VALUES (?, ?, ?)",
#                     (subject_name, year, branch)
#                 )
#                 subject_id = cursor.lastrowid

#                 for teacher in teachers:
#                     cursor.execute(
#                         "INSERT INTO teachers (name, subject_id) VALUES (?, ?)",
#                         (teacher, subject_id)
#                     )

#     conn.commit()
#     conn.close()
#     print(f"Database Initialized Successfully at: {DB_PATH}")

# def get_subjects(year, branch):
#     conn = get_db_connection()
#     if not conn: return []
#     cursor = conn.cursor()
#     # SQLite uses '?' as a placeholder
#     cursor.execute("SELECT id, name FROM subjects WHERE year = ? AND branch = ?", (year, branch))
#     results = [dict(row) for row in cursor.fetchall()]
#     conn.close()
#     return results

# def get_teachers(subject_id):
#     conn = get_db_connection()
#     if not conn: return []
#     cursor = conn.cursor()
#     cursor.execute("SELECT name FROM teachers WHERE subject_id = ?", (subject_id,))
#     results = [dict(row) for row in cursor.fetchall()]
#     conn.close()
#     return results

# if __name__ == "__main__":
#     initialize_database()







import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '#N_joshi13',  
    'database': 'scriptorium_db'
}

def get_db_connection():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except Error as e:
        print(f"Error: {e}")
        return None

def initialize_database():
    conn = get_db_connection()
    if not conn: return
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subjects (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            year INT,
            branch VARCHAR(10)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS teachers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            subject_id INT,
            FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE
        )
    """)

    data = {
        "IT": {
            2: {
                "Operating Systems": ["Pf. Harpreet Kaur", "Dr. Kulvinder Singh Mann", "Dr. Pankaj Bhambri"],
                "Object Oriented Programming with Java": ["Dr. Akshay Girdhar", "Pf. Jaspreet Kaur", "Pf. Vandana"],
                "Advanced and Emerging Technologies": ["Dr. Amit Kamra", "Dr. Sachin Bagga", "Pf. Sarabmeet Singh"],
                "DataBase Management System": ["Pf. Neha Gupta", "Dr. Mohanjit Kaur Kang", "Pf. Gitanjali"],
                "Discrete Mathematics": ["Pf. Parminder Kaur Wadhwa", "Pf. Jasleen Kaur"],
                "Web Technologies": ["Pf. Himani Sharma", "Dr. Randeep Kaur", "Dr. Palwinder Kaur"]
            },
            3: {
                "DevOps": ["Dr. Kamaljit Kaur", "Pf. Himani Sharma"],
                "DAA ": ["Dr. Randeep Kaur", "Pf. Parminder Kaur Wadhwa"]
            }
        },
        "CSE": {
            2: {
                "Data Analytic Tools": ["Prof. Sita Rani", "Prof. Kapil Sharma" , "Prof. Shailja", "Prof. PreetKamal Singh" ],
                "Database Management System ": ["Prof. Jasmin Kaur" , "Prof. Khushi Dhunna" , "Dr. Kiran Jyoti", "Prof. Goldendeep Kaur"],
                "Computer Networks ":["Prof. Daljit Singh", "Prof. Palak Sood", "Prof. Satinderpal Singh", "Prof. Haredeep Singh Kang"],
                "Artificial Intelligence":["Prof. Jasdeep Kaur", "Prof. Aashish", "Prof. Diana Nagpal" , "Prof. Kawaljeet Kaur"],
                "Operating System" : ["Prof. Harkomalpreet", "Prof. Kajal Chugh", "Prof. Lakhvir Kaur", "P'rof. Harshim"],
                "Environmental Sciences and Sustainability":["Prof. Komalpreet", "Prof. Hitika Dhawan", "Prof.Shreya", "Prof.Sumanpreet"],
                "Business Essential for Engineers":["Prof. Sunil Kumar", "Prof. Nisha"]
            }
        },
       "ECE":{
            2: {
                "Computer Networks" : ["Harminder Kaur"],
                "Object Oriented Programming & DS": ["Er. Harminder Kaur Aulakh"],
                "VHDL" : ["Dr. Gurjot Kaur Walia", "Dr. Navneet Kaur"]
            }
        }
    }

    subject_id_map = {}
    for branch, years in data.items():
        for year, subjects in years.items():
            for subject_name, teachers in subjects.items():
                cursor.execute(
                    "INSERT INTO subjects (name, year, branch) VALUES (%s, %s, %s)",
                    (subject_name, year, branch)
                )
                subject_id = cursor.lastrowid
                subject_id_map[subject_name] = subject_id

                for teacher in teachers:
                    cursor.execute(
                        "INSERT INTO teachers (name, subject_id) VALUES (%s, %s)",
                        (teacher, subject_id)
                    )

    conn.commit()
    cursor.close()
    conn.close()
    print("Database Initialized and Seeded Successfully!")

def get_subjects(year, branch):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, name FROM subjects WHERE year = %s AND branch = %s", (year, branch))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

def get_teachers(subject_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT name FROM teachers WHERE subject_id = %s", (subject_id,))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

if __name__ == "__main__":
    initialize_database()