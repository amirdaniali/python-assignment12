import streamlit as st  # Importing the Streamlit library

# Text input
st.header("Section 2")  # A new section to group interactive input components
name = st.text_input(
    "Enter your name", "John Doe"
)  # Simple text field with a default value
description = st.text_area(
    "Description", "Write something..."
)  # Multi-line text box for longer input

# Numeric input
age = st.number_input(
    "Age", min_value=0, max_value=120, value=25
)  # Number picker with min/max range
score = st.slider(
    "Score", 0, 100, 50
)  # Slider to pick a number in a range — great for ratings or scores

# Selection widgets
option = st.selectbox(
    "Choose an option", ["A", "B", "C"]
)  # Dropdown menu — user picks one option
options = st.multiselect(
    "Multiple options", ["X", "Y", "Z"]
)  # Allows multiple selections at once

# Date and time
date = st.date_input("Select date")  # Calendar-style date picker
time = st.time_input("Select time")  # Clock-style time picker

# Buttons and checkbox
if st.button("Click me"):  # A button that runs code when clicked
    st.write("Button clicked!")  # Responds when the button is pressed

if st.checkbox("Show/Hide"):  # Checkbox to toggle something on/off
    st.write("Visible content")  # Displays this text only if the box is checked
