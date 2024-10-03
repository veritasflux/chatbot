import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("💬 SQL to PySpark Converter Chatbot")
st.write(
    "This chatbot uses OpenAI's GPT-3.5 model to convert SQL queries to PySpark code. "
    "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys). "
    "You can also learn how to build this app step by step by [following our tutorial](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps)."
)

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
openai_api_key = client
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:

    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    # Define a system message with rules for SQL to PySpark conversion
    system_message = """
    You are a chatbot that helps convert SQL queries into PySpark code. 
    Your goal is to accurately interpret SQL queries and generate their PySpark equivalents.
    Here are the rules you should follow when interpreting SQL queries:
    
    1. Ensure the SQL syntax is correct and includes all required clauses.
    2. Check for SELECT, FROM, WHERE, GROUP BY, and ORDER BY clauses.
    3. Handle common SQL functions like COUNT, SUM, AVG, MIN, MAX.
    4. Translate SQL joins into their PySpark equivalent.
    5. Always use the PySpark 'DataFrame' API for transformations.
    6. If there are unsupported SQL functions, return an appropriate error message.
    7. Ensure the resulting PySpark code is valid and functional.
    8. Use 'df' as the default DataFrame name for your PySpark queries.
    9. Translate SQL conditions into PySpark filter operations.
    """

    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": system_message}]

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt := st.chat_input("Enter your SQL query:"):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response using the OpenAI API.
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        # Stream the response to the chat using `st.write_stream`, then store it in 
        # session state.
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
