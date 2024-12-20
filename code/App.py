import streamlit as st
from Student import student_login, student_registration, student_main
from Admin import admin_login, manage_students
from Database import create_table

# Set the page config
st.set_page_config(page_title="Knowledge Based Recommender System", layout="wide", page_icon="logo.jpg")

st.sidebar.image("logo.jpg", width=300)
st.sidebar.markdown("""
    <h1 style='text-align: center; font-size: 28px; font-weight: bold; color: #007BFF; font-family: "Helvetica", sans-serif;'>Welcome to Saveetha Engineering College</h1>
""", unsafe_allow_html=True)

# CSS Styling
st.markdown("""
    <style>
        body {
            background-color: #f0f2f5;
        }
        .title {
            font-size: 36px;
            font-weight: bold;
            color: #007BFF;
            text-align: center;
            margin-bottom: 20px;
            font-family: 'Helvetica', sans-serif;
        }
        .quote {
            font-size: 20px;
            font-style: italic;
            color: #888;
            text-align: center;
            margin: 10px 0;
            font-family: 'Helvetica', serif;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">Knowledge Based Recommender System</div>', unsafe_allow_html=True)
st.markdown('<div class="quote">Networking is not just about connecting people; it\'s about connecting people with ideas, and opportunities</div>', unsafe_allow_html=True)

# Initialize the database
create_table()

# Session state management
if 'user_type' not in st.session_state:
    st.session_state['user_type'] = None
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = ""
if 'show_registration' not in st.session_state:
    st.session_state['show_registration'] = False

def logout():
    st.session_state['logged_in'] = False
    st.session_state['username'] = ""
    st.session_state['user_type'] = None
    st.session_state['show_registration'] = False
    st.success("You have been logged out!")

# Main application logic
def main():
    if st.session_state['logged_in']:
        # Show logout button in the sidebar
        st.sidebar.button("Logout", on_click=logout)
        
        if st.session_state['user_type'] == 'admin':
            st.success(f"Logged in as: {st.session_state['username']}")
            manage_students()                       
        elif st.session_state['user_type'] == 'student':
            st.success(f"Logged in as: {st.session_state['username']}")
            student_main()
    else:
        login_form()

def login_form():
    # Sidebar selection for Login or Register
    option = st.sidebar.selectbox("Choose an option", ["User", "Admin", "Register New User"])

    if option == "User":
        student_login()
    elif option == "Admin":
        admin_login()
    elif option == "Register New User":
        student_registration()

    # Add forgot password note at the bottom
    st.markdown("Forgot password? Please contact [admin@gmail.com](mailto:admin@gmail.com)")


if __name__ == "__main__":
    main()