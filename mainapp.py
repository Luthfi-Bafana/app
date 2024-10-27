# Set up and run this Streamlit App
import streamlit as st
from logics.new_programs import filter_programmes, df, filter_further, check_programme_eligibility, give_info
from helper_functions.utility import check_password

# Streamlit App Configuration
st.set_page_config(
    layout="centered",
    page_title="My Streamlit App"
)

st.title("Streamlit App")

# Check if the password is correct.  
if not check_password():  
    st.stop()
    
st.sidebar.success("Select a page")

# Form for user input
form = st.form(key="form")
form.subheader("Enter your profile")

# Widgets to reflect student's financial condition
student_school = form.selectbox(
    "Select your school",
    options=["National University of Singapore (NUS)", "Nanyang Technological University (NTU)"]
)

scheme = form.radio(
    "Select the schemes you're interested in",
    options=["Hostel/Accomodation Fees", "Living Expenses", "Overseas Programmes", "Tuition Fees", "Tuition Fees and Living Expenses"]
)

student_type = form.radio(
    "Select your student type",
    options=["Singapore Citizen or Permanent Resident", "International Students"]
)

student_pci = form.slider(
    "Enter your Per Capita Income (PCI) in SGD",
    min_value=0, max_value=5000, step=100, value=2000
)

if form.form_submit_button("Submit"):
    st.toast(f"User Input Submitted")

    filtered_df = filter_programmes(df, student_school, scheme, student_type)
    further_filtered_df = filter_further(filtered_df, student_pci)
        
    # Display the filtered dataframe in Streamlit
    if not further_filtered_df.empty:
        st.subheader(f"Financial Aid programmes applicable for you")
        st.dataframe(further_filtered_df)
    else:
        st.write(f"No programmes found for {scheme} with the specified conditions.")

#----------------------2nd use case--------------------------------#

# Additional section for LLM-generated response
st.subheader("Ask for more information")

# Text input and submit button for LLM-generated response
user_question = st.text_area("Enter your question or message here", height=150)
if st.button("Submit Question"):
    st.toast("Processing your question...")
    response = give_info(df, user_question)  # Call the LLM function with the user input
    
    # Display the LLM response
    st.write("Response:")
    st.write(response)

#mainapppy-rehvfzi4kea2ssbdp5qczv
#financial-programs-app.streamlit.app