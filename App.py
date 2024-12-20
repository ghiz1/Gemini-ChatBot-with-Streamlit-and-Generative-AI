import streamlit as st
import os
import google.generativeai as genai
from pyngrok import ngrok
import streamlit as st
from generative_model import configure_model
from ngrok_launcher import start_ngrok


# Configure Google Generative AI
genai = configure_model()

# Set the title of the Streamlit app
st.title("AI Chat - Powered by Gemini")

# Sidebar for model selection
st.sidebar.title("Model Selection")
model_name = st.sidebar.selectbox("Select Model", ["gemini-1.5-flash", "gemini-pro"])

# Initialize the generative model
model = genai.GenerativeModel(model_name)

# Sidebar for generation parameters
st.sidebar.title("Generation Parameters")
temperature = st.sidebar.slider(
    "Temperature", min_value=0.0, max_value=1.0, value=0.7, key="temperature"
)
max_tokens = st.sidebar.slider(
    "Max Tokens", min_value=1, max_value=512, value=256, key="max_tokens"
)

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Chat with me!"}]

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat history for storing context
chat_history = []

# Function to handle query and response
def llm_function(query):
    """
    Processes the user query using the generative model and stores the response.
    """
    try:
        # Add the user query to chat history
        chat_history.append({"role": "user", "content": query})

        # Generate a response from the AI model
        response = model.generate_content(
            query,
            generation_config=genai.types.GenerationConfig(
                temperature=st.session_state.get("temperature", 0.7),
                max_output_tokens=st.session_state.get("max_tokens", 256),
            ),
        )

        # Display the assistant's response
        with st.chat_message("assistant"):
            st.markdown(response.text)

        # Store the conversation in session state for persistence
        st.session_state.messages.append({"role": "user", "content": query})
        st.session_state.messages.append({"role": "assistant", "content": response.text})

        # Append the assistant's response to chat history
        chat_history.append({"role": "assistant", "content": response.text})

    except Exception as e:
        # Handle and display errors
        st.error(f"An error occurred: {e}")

# Accept user input via chat input widget
query = st.chat_input("How can I help you?")

# Process the query when provided
if query:
    # Display the user input
    with st.chat_message("user"):
        st.markdown(query)

    # Call the function to process the input and generate a response
    llm_function(query)

# Start the ngrok tunnel
if __name__ == "__main__":
    public_url = start_ngrok(port=8501)
    st.sidebar.success(f"Your app is running at: {public_url}")
    print(f"Your Streamlit app is running at: {public_url}")