import sqlite3
import pandas as pd
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
def create_connection():
    conn = sqlite3.connect('students.db')
    return conn

def create_table():
    conn = create_connection()
    with conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                department TEXT NOT NULL,
                year INTEGER NOT NULL,
                interests TEXT NOT NULL,
                linkedin_id TEXT,
                phone_number TEXT,
                email TEXT UNIQUE NOT NULL,
                user_id TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
    conn.close()

def add_student(name, department, year, interests, linkedin_id, phone_number, email, user_id, password):
    conn = create_connection()
    try:
        with conn:
            conn.execute('''
                INSERT INTO students (name, department, year, interests, linkedin_id, phone_number, email, user_id, password)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (name, department, year, interests, linkedin_id, phone_number, email, user_id, password))
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def verify_user(user_id, password):
    conn = create_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM students WHERE user_id = ? AND password = ?', (user_id, password))
    user_found = c.fetchone() is not None
    conn.close()
    return user_found

def find_matches(user_id):
    conn = create_connection()
    c = conn.cursor()
    c.execute('SELECT name, interests, email FROM students')
    students = c.fetchall()

    if not students:
        return []

    student_names = [student[0] for student in students]
    interests = [student[1] for student in students]
    student_emails = [student[2] for student in students]

    interests_lower = [interest.lower() for interest in interests]

    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform(interests_lower)
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    c.execute('SELECT name, interests FROM students WHERE user_id = ?', (user_id,))
    user_data = c.fetchone()
    conn.close()

    if user_data is None:
        return []

    user_name, user_interests = user_data
    user_interests_lower = user_interests.lower()

    user_index = student_names.index(user_name)
    sim_scores = list(enumerate(cosine_sim[user_index]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    match_indices = [i for i, score in sim_scores if i != user_index and score > 0]
    available_matches = [(student_names[i], student_emails[i]) for i in match_indices][:2]

    return available_matches

def get_students():
    conn = create_connection()
    df = pd.read_sql_query('SELECT * FROM students', conn)
    conn.close()
    return df

def delete_student(student_id):
    conn = create_connection()
    try:
        with conn:
            conn.execute('DELETE FROM students WHERE id = ?', (student_id,))
        return True
    except Exception as e:
        return False
    finally:
        conn.close()
def logout():
    st.session_state['logged_in'] = False
    st.session_state['username'] = ""
    st.session_state['user_type'] = None