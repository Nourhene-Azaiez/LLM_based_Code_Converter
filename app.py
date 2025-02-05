import streamlit as st
from utils.code_processing import *
import os

# Load custom CSS for chat styling
def load_css():
    with open("assets/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# App title with an emoji for better UX
st.title("💬 Code Converter Chatbot")

# Load custom CSS
load_css()

# Sidebar for settings
with st.sidebar:
    # Title at the header
    st.title("⚙️ Settings")
    
    
    # Expander for additional settings
    with st.expander("💡 Tips"):
        st.write("1. Select your input and output languages.")
        st.write("2. Paste your code and click 'Convert'.")
        st.write("3. View the converted code in the chat history.")

# Language selection
code_types = ["Select a language...","Python", "JavaScript", "Java", "TypeScript", "PHP", "Ruby"]

# Display chat history using Streamlit's chat format
for msg in st.session_state.messages:
    role = "user" if msg["role"] == "user" else "assistant"
    
    with st.chat_message(role):
        st.markdown(f"**{role.capitalize()} ({msg['input_language']} → {msg['output_language']}):**")
        st.code(msg["content"], language=msg["output_language"].lower())

# Input form at the bottom
with st.form(key="chat_input_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        input_language = st.selectbox("📝 Input Language", code_types, index=0)
    with col2:
        output_language = st.selectbox("🎯 Output Language", code_types, index=0)
    
    input_code = st.text_area("✍️ Code Input", height=150, placeholder="Paste your code here...")
    submit_button = st.form_submit_button("🚀 Convert Code")

# Handle code conversion
if submit_button:
    if input_language == "Select a language...":
        st.warning("Please select a valid input language.")
    if output_language == "Select a language...":
        st.warning("Please select a valid output language.")
    if input_code.strip() == "":
        st.warning("⚠️ Please enter some code to convert.")
    else:
        # Add user input to chat history
        st.session_state.messages.append({
            "role": "user",
            "content": input_code,
            "input_language": input_language,
            "output_language": output_language
        })
        # **Force rerun** to show user message before processing
        st.rerun()


if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    last_message = st.session_state.messages[-1]
    # Show a loading spinner while processing
    with st.spinner("⏳ Converting code..."):
        ext = "py" if input_language == "Python" else \
        "java" if input_language == "Java" else \
        "js" if input_language == "JavaScript" else \
        "ts" if input_language == "TypeScript" else \
        "rb" if input_language == "Ruby" else \
        "php" if input_language == "PHP" else \
        "css" if input_language == "CSS" else \
        None
        temp_path = f"/tmp/input_code.{ext}"
        
        with open(temp_path, "w") as f:
            f.write(input_code)

        # Use the CodeProcessor module to process the code
        description,converted_code,score=process_code(temp_path,output_language)

    # Create a formatted response with markdown
    converted_code_md = f"""📝 Converted Code
Input Language:{input_language}  
Output Language: {output_language}  
{description}


Conversion Result:

{converted_code}
Conversion Score: {score}
"""

    # Add assistant response to chat history
    st.session_state.messages.append({
        "role": "assistant",
        "content": converted_code_md,
        "input_language": input_language,
        "output_language": output_language
    })

    # Rerun the app to update the chat history
    st.rerun()
