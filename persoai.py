import openai
import streamlit as st

# Add your OpenAI API key directly into the script
openai.api_key = "your-api-key"  # Replace with your actual API key

# Custom CSS to style the app
st.markdown("""
    <style>
        /* Styling for the ZADE heading */
        h1#zade-title {
            font-family: 'Brush Script MT', cursive;
            font-size: 60px;
            color: white;
            text-align: center;
            margin-bottom: 0;
        }

        /* Styling for the chat bubbles */
        .chat-bubble {
            background-color: #6A0DAD;  /* Dark purple */
            color: white;
            border-radius: 10px;
            padding: 10px;
            margin: 10px 0;
            font-family: sans-serif;  /* Normal font for ZADE responses */
        }

        .chat-bubble-za {
            background-color: #4B0082;  /* Alternate purple */
        }

        /* Styling for the name outside the chat bubbles */
        .name-label {
            font-weight: bold;
            margin-bottom: 0;
            font-family: sans-serif;  /* Normal font */
        }

        /* Hover effects for the buttons */
        button:hover {
            background-color: #6A0DAD !important;
            color: white !important;
        }

        /* Centered and styled form buttons */
        .stButton button {
            background-color: #6A0DAD;
            color: white;
            border: none;
            padding: 8px 16px;
            font-size: 16px;
            font-family: sans-serif;
        }

    </style>
""", unsafe_allow_html=True)

# Streamlit app setup
st.markdown("<h1 id='zade-title'>𝔃𝓪𝓭𝓮 </h1>", unsafe_allow_html=True)

# Add back the fun prompt to ask ZADE something
st.write("Ask ZADE something fun!")

# Initialize conversation history (store it in session state)
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []

# Initialize for tracking the latest question and response
if 'latest_question' not in st.session_state:
    st.session_state.latest_question = ""

if 'latest_response' not in st.session_state:
    st.session_state.latest_response = ""


# Function to handle any query with emotional intelligence and follow-up responses
def assistant_response(user_input):
    # Store the latest question
    st.session_state.latest_question = user_input
    messages = [
                   {"role": "system",
                    "content": "You are ZADE, a playful AI assistant for children or anyone. You respond in a fun, friendly, and helpful way. Always use simple language, be kind, and make learning exciting!"}
               ] + st.session_state.conversation_history

    messages.append({"role": "user", "content": user_input})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    reply = response['choices'][0]['message']['content']

    # Store the latest response
    st.session_state.latest_response = reply

    return reply


# Input box for user to ask questions, wrapped in a form to handle submission separately
with st.form(key='input_form'):
    input_value = st.text_input("", key="input_text")

    # Buttons for "Ask"
    col1, col2 = st.columns([0.5, 0.5])
    with col1:
        submit_button = st.form_submit_button(label='Ask')

# Handle query submission via the form
if submit_button and input_value:
    response = assistant_response(input_value)

# Display only ZADE's latest response
if st.session_state.latest_response:
    st.markdown(
        f'<p class="name-label">ZADE:</p><div class="chat-bubble chat-bubble-za">{st.session_state.latest_response}</div>',
        unsafe_allow_html=True)

    st.markdown("---")  # Separator line

# Display the conversation history starting from the first interaction
st.markdown("### Convo History")

# If there’s at least one previous conversation, display the full history
if len(st.session_state.conversation_history) > 0:
    # Looping through the conversation in  order (from first question onwards)
    for idx, entry in enumerate(st.session_state.conversation_history):
        color_class = "chat-bubble-za" if entry["role"] == "assistant" else ""
        role = "ZADE" if entry["role"] == "assistant" else "You"

        st.markdown(f'<p class="name-label">{role}:</p><div class="chat-bubble {color_class}">{entry["content"]}</div>',
                    unsafe_allow_html=True)

# After displaying, add the latest question and response to the conversation history only in the next round
if st.session_state.latest_question and st.session_state.latest_response and submit_button:
    st.session_state.conversation_history.append({"role": "user", "content": st.session_state.latest_question})
    st.session_state.conversation_history.append({"role": "assistant", "content": st.session_state.latest_response})
    st.session_state.latest_question = ""
    st.session_state.latest_response = ""

# Button to end conversation (optional)
if st.button("End Conversation"):
    st.session_state.conversation_history = []  # Clear conversation history
    st.write("𝓱𝓪𝓿𝓮 𝓪 𝓷𝓲𝓬𝓮 𝓭𝓪𝔂!!")
