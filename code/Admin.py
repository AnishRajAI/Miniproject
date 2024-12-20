import streamlit as st
from Database import get_students, delete_student, add_student, create_connection
import pandas as pd

def admin_login():
    admin_user = st.text_input("Admin Username", key="admin_user")
    admin_password = st.text_input("Admin Password", type='password', key="admin_password")
    if st.button("Login as Admin"):
        # Hardcoded admin credentials
        if admin_user == "admin" and admin_password == "password123":
            st.session_state['logged_in'] = True
            st.session_state['username'] = admin_user
            st.session_state['user_type'] = 'admin'
            st.success("Admin Login successful! 🎉")
        else:
            st.error("Invalid Admin Username or Password.")

def manage_students():
    st.subheader("Student Database")
    students = get_students()
    st.dataframe(students)

    # Create tabs for Add, Edit, and Delete student operations
    tab1, tab2, tab3 = st.tabs(["Add Student", "Edit Student", "Delete Student"])

    # Add Student Tab
    with tab1:
        st.subheader("Add New Student")
        name = st.text_input("Name (Add)")
        department = st.text_input("Department (Add)")
        year = st.number_input("Year (Add)", min_value=1, max_value=4)
        interests = st.text_input("Interests (Add)")
        linkedin_id = st.text_input("LinkedIn ID (Add)")
        phone_number = st.text_input("Phone Number (Add)")
        email = st.text_input("Email (Add)")
        user_id = st.text_input("User ID (Add)")
        password = st.text_input("Password (Add)", type='password')

        if st.button("Add Student"):
            if add_student(name, department, year, interests, linkedin_id, phone_number, email, user_id, password):
                st.success("Student added successfully!")
            else:
                st.error("Email or User ID already exists!")

    # Edit Student Tab
    with tab2:
        st.subheader("Edit Existing Student")
        student_id = st.number_input("Student ID to edit", min_value=1, step=1)
        if student_id:
            students = get_students()
            student = students[students['id'] == student_id]
            if not student.empty:
                student = student.iloc[0]
                name = st.text_input("Name (Edit)", value=student['name'])
                department = st.text_input("Department (Edit)", value=student['department'])
                year = st.number_input("Year (Edit)", min_value=1, max_value=4, value=student['year'])
                interests = st.text_input("Interests (Edit)", value=student['interests'])
                linkedin_id = st.text_input("LinkedIn ID (Edit)", value=student['linkedin_id'])
                phone_number = st.text_input("Phone Number (Edit)", value=student['phone_number'])
                email = st.text_input("Email (Edit)", value=student['email'])
                user_id = st.text_input("User ID (Edit)", value=student['user_id'])
                password = st.text_input("Password (Edit)", value=student['password'], type='password')

                if st.button("Update Student"):
                    # Check if email or user_id already exists
                    if email != student['email'] or user_id != student['user_id']:
                        if not add_student(name, department, year, interests, linkedin_id, phone_number, email, user_id, password):
                            st.error("Update failed: Email or User ID already exists.")
                        else:
                            st.success("Student updated successfully!")
                    else:
                        with create_connection() as conn:
                            conn.execute('''
                                UPDATE students
                                SET name = ?, department = ?, year = ?, interests = ?, linkedin_id = ?, phone_number = ?, password = ?
                                WHERE id = ?
                            ''', (name, department, year, interests, linkedin_id, phone_number, password, student_id))
                            st.success("Student updated successfully!")

    # Delete Student Tab
    with tab3:
        st.subheader("Delete Student")
        student_id = st.number_input("Student ID to delete", min_value=1, step=1)
        if st.button("Delete Student"):
            if delete_student(student_id):
                st.success("Student deleted successfully!")
            else:
                st.error("Error deleting student. Please check the ID.")
