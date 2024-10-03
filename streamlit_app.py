import streamlit as st
from transformers import pipeline

# Show title and description.
st.title("💬 SQL to PySpark Converter Chatbot (Hugging Face)")
st.write(
    "This chatbot uses a model from Hugging Face (Salesforce/codet5-base) to convert SQL queries into PySpark code. "
    "It ensures proper handling of SQL clauses, functions, and translates them into equivalent PySpark transformations."
)

# Load the Hugging Face model for text2text-generation
@st.cache_resource  # Cache the model to avoid reloading on every run
def load_model():
    return pipeline("text2text-generation", model="Salesforce/codet5-base")

# Load the model
model = load_model()

# Create a session state variable to store the chat messages.
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display the existing chat messages via `st.chat_message`.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Create a chat input field to allow the user to enter a message.
if prompt := st.chat_input("Enter your SQL query to convert to PySpark:"):

    # Store and display the current prompt.
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate a response using the Hugging Face model
    with st.chat_message("assistant"):
        st.markdown("Converting SQL to PySpark...")
        response = model(prompt, max_length=200, num_return_sequences=1)[0]["generated_text"]

    # Display the assistant's response and store it in session state.
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
