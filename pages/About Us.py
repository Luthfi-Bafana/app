import streamlit as st

st.title("About this App")

st.write("This is a Streamlit App that offers two main use cases")

st.write('''Financial aid programmes are very important to university students, both local and international. However, online information on relevant programmes is very dense and hard to sift through.
        This application seeks NUS and NTU students navigate the maze of financial aid programmes information online by providing a one-stop app to discover financial aid programme information tailored to each student's profile.''')

with st.expander("First use case: Finding tailored financial aid programmes"):
    st.write('''
        1. Enter the relevant information pertaining to your student status and financial information
        2. Click the submit button
        3. The app will generate the financial aid programme which you qualify for along with the associated relevant information about those courses in a dataframe.
    ''')

with st.expander("Second Use Case: General information"):
    st.write('''
        1. Enter a general query about financial aid programme (eg. Find me information about NUS financial aid programmes addressing Tuition Fees).
        2. Click the submit button
        3. The app will generate a text completion based on your query, providing the information that you need
    ''')