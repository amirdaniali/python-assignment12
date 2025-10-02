import streamlit as st  # Importing the Streamlit library

# Basic text elements
st.title("My First Streamlit App")  # Adds a big title at the top of the app
st.header("Section 1")  # Adds a section header — good for breaking content into parts
st.subheader("Header")  # Slightly smaller than header — useful for structure
st.subheader("Subheader")  # Another level down — keeps things organized
st.text("Simple text")  # Displays plain, unformatted text — like a basic message
st.markdown(
    "**Bold** and *italic* text"
)  # Markdown lets you add simple formatting like bold and italics

# Display data
st.write(
    "Automatic data display"
)  # Streamlit's flexible method — handles strings, numbers, dataframes, and more
st.code(
    "print('Hello World')", language="python"
)  # Nicely formats code blocks with syntax highlighting
st.latex(r"\int_{a}^{b} x^2 dx")  # Renders LaTeX math formulas — great for equations
