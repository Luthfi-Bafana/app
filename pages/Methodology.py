import streamlit as st
from PIL import Image

st.title("Methodology")

# Display the image
image_path = "Methodology.jpg"  
image = Image.open(image_path)
st.image(image, caption="Methodology", use_column_width=True)

st.subheader("Overview of Methodology")

st.write(f'''I obtained the information on financial aid programmes from the NUS and NTU websites and aggregated the information into an excel sheet.
         As depicted in the diagram above, the app takes in student profile inputs provided by the user through the streamlit app and I used 
        a combination of prompt chaining in order to filter the financial aid programmes that the student would qualify for according to the student's profile''')