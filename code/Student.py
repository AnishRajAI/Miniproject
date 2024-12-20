import streamlit as st
from Database import add_student, verify_user, find_matches

def student_login():
    user_id = st.text_input("User ID", key="login_user_id")
    password = st.text_input("Password", type='password', key="login_password")
    if st.button("Login as User"):
        if verify_user(user_id, password):
            st.session_state['logged_in'] = True
            st.session_state['username'] = user_id
            st.session_state['user_type'] = 'student'
            st.success("Login successful! 🎉")
        else:
            st.error("Invalid User ID or Password.")

def student_registration():
    st.markdown("### New User Registration")
    with st.form(key='register_form'):
        name = st.text_input("Name")
        department = st.text_input("Department")
        year = st.number_input("Year", min_value=1, max_value=4)
        interests = st.text_input("Interests (comma separated)")
        linkedin_id = st.text_input("LinkedIn ID")
        phone_number = st.text_input("Phone Number")
        email = st.text_input("Email")
        user_id_reg = st.text_input("User ID")
        password_reg = st.text_input("Password", type='password')

        submit_button = st.form_submit_button("Register")
        if submit_button:
            if not (name and department and year and interests and email and user_id_reg and password_reg):
                st.error("All fields are required!")
            else:
                if add_student(name, department, year, interests, linkedin_id, phone_number, email, user_id_reg, password_reg):
                    st.success("Student registered successfully! 🎉")
                else:
                    st.error("Failed to register. User ID or Email might already be in use.")

def student_main():
    matched_students = find_matches(st.session_state['username'])
    st.subheader("Connected People: ")
    if matched_students:
        for student, email in matched_students:
            st.write(f"**{student}** -  Email: {email}")
    else:
        st.write("No connections found, try after some time🙂")