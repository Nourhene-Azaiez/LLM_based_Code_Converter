import streamlit as st
from utils.code_processing import CodeProcessor  # Import the module
import os

# Set the page layout to centered mode
st.set_page_config(layout="wide", page_title="Interactive Code Translator")

# Load custom CSS for styling
def load_css():
    css_file_path = "assets/styles.css"
    if os.path.exists(css_file_path):
        with open(css_file_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load CSS
load_css()

# Sidebar Content: Logo and Navbar
st.sidebar.image("assets/logo.png", width=150)
st.sidebar.markdown("<br>" * 14, unsafe_allow_html=True)
st.sidebar.markdown("""
    <div class="navbar">
        <a href="#">About</a>
        <a href="#">Contact</a>
    </div>
""", unsafe_allow_html=True)

col1, col2 = st.sidebar.columns(2)
with col1:
    st.image("assets/logo_EY.png", width=90)
with col2:
    st.image("assets/logo_supcom.png", width=130)

# App Title
st.markdown("""
<div class="title-container">
    <div class="title-icon">✨</div>
    <div class="title-text">Interactive Code Translator</div>
</div>
""", unsafe_allow_html=True)
st.write("")

# Container for displaying converted code and interaction
if 'converted_code' in st.session_state and st.session_state['converted_code']:
    with st.container():
        col21, col22, col23 = st.columns([3, 2, 2])
        with col21:
            st.subheader("Converted Code")
        with col23:
            st.download_button(
                label="Download",
                data=st.session_state["converted_code"],
                file_name="conversion_result.java",
                mime="text/plain",
                use_container_width=True,
            )

        # Display the converted code in a scrollable area
        converted_code = st.session_state["converted_code"]
        st.markdown(f'''
        <div class="code-container">
            <pre id="converted_code">{converted_code}</pre>
        </div>
        ''', unsafe_allow_html=True)

# Code conversion form (fixed at the bottom)
with st.form(key="code_conversion_form", clear_on_submit=False):
    input_code = st.text_area("Paste your code here:", height=80, key="input_code")

    # Side-by-side dropdowns for selecting input and output code types
    col1, col2, col3, col4 = st.columns([4, 4, 6, 3])

    with col1:
        conversion_type_input = st.selectbox("Input Code Type", ["Python", "Java"], key="input_type")

    with col2:
        conversion_type_output = st.selectbox("Output Code Type", ["Python", "Java"], key="output_type")

    # Styled Submit Button (acts as Convert button)
    with col4:
        st.write("")
        convert_button = st.form_submit_button("Convert", use_container_width=True)

    # Process the code if the submit button is clicked
    if convert_button:
        if input_code.strip():
            # Create a temporary file to store the input code
            temp_path = "/tmp/input_code.txt"
            with open(temp_path, "w") as f:
                f.write(input_code)

            # Use the CodeProcessor module to process the code
            processor = CodeProcessor(temp_path)
            chunks = processor.parse_and_chunk()  # Parse and chunk the code
            converted_code = processor.convert_code(chunks, target_language=conversion_type_output.lower())  # Convert code

            # Store converted code in session state
            st.session_state["converted_code"] = converted_code

            # Inform the user of success
            st.success("Code converted successfully!")
        else:
            st.warning("Please enter some code to convert!")
