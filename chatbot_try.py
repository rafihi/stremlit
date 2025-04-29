import streamlit as st
import google.generativeai as genai
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space
import time

# Set your API key
API_KEY = "AIzaSyAQ_FNPq-sPgyRD_grNagXz2lkWdow_5J0"

# Configure the generative AI
genai.configure(api_key=API_KEY)

# Set page configuration
st.set_page_config(
    page_title="EduGenius AI Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better aesthetics
st.markdown("""
<style>
    .chat-message {
        padding: 1.5rem; 
        border-radius: 0.8rem; 
        margin-bottom: 1rem; 
        display: flex;
        align-items: flex-start;
    }
    .chat-message.user {
        background-color: #2b313e;
        border-left: 5px solid #4CAF50;
    }
    .chat-message.bot {
        background-color: #343a46;
        border-left: 5px solid #2196F3;
    }
    .chat-message .avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        object-fit: cover;
        margin-right: 1rem;
    }
    .chat-message .message {
        flex: 1;
    }
    .stApp {
        background-color: #1a1d24;
        color: #ffffff;
    }
    .css-18e3th9 {
        padding-top: 0rem;
    }
    .css-1d391kg {
        padding-top: 1rem;
    }
    .stTextInput>div>div>input {
        background-color: #2b313e;
        color: white;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 20px;
        padding: 0.5rem 1rem;
        border: none;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    h1, h2, h3 {
        color: #4CAF50;
    }
    .avatar-container {
        display: flex;
        justify-content: center;
        margin-bottom: 1rem;
    }
    .sidebar .sidebar-content {
        background-color: #1a1d24;
    }
</style>
""", unsafe_allow_html=True)

# Function to create Gemini model with custom configuration
def get_gemini_model():
    generation_config = {
        "temperature": 0.7,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 1024,
    }
    
    safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
    ]
    
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        safety_settings=safety_settings,
    )
    
    return model

# Function to start chat with system prompt
def start_chat():
    model = get_gemini_model()
    
    system_prompt = """
    You are EduGenius, an educational AI assistant powered by Gemini 2.0 Flash.
    
    Guidelines:
    1. ONLY answer questions related to education, learning, academic subjects, teaching methodologies, student development, educational technologies, or educational institutions.
    2. For any questions outside the educational domain, politely decline and redirect the conversation toward educational topics.
    3. Provide accurate, informative, and helpful responses on educational topics.
    4. Use simple language for basic concepts and more technical terms when appropriate.
    5. When possible, structure your answers with clear headings, bullet points, or numbered lists.
    6. Always cite sources or mention when information might require further verification.
    7. Encourage critical thinking and provide multiple perspectives on controversial educational topics.
    8. Offer practical applications or examples to illustrate complex educational concepts.
    9. Be supportive and encouraging of learning efforts.
    10. Remember: your primary focus is education - do not engage with questions about politics, entertainment, personal advice, or other non-educational domains.
    
    Let's help users learn and grow through education!
    """
    
    chat = model.start_chat(history=[
        {
            "role": "user",
            "parts": ["This is your system prompt. Please follow these guidelines carefully: " + system_prompt]
        },
        {
            "role": "model",
            "parts": ["I understand my role as EduGenius. I will only answer questions related to education and learning, politely redirect non-educational queries, and follow all the guidelines provided. I'm ready to help users with their educational questions!"]
        }
    ])
    
    return chat

# Main content area
colored_header(
    label="EduGenius: Your Educational AI Assistant",
    description="Ask me anything about education, learning, and academic topics",
    color_name="green-70",
)

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    
if "chat" not in st.session_state:
    st.session_state.chat = start_chat()

# Display chat messages from history
chat_container = st.container()
with chat_container:
    for message in st.session_state.chat_history:
        with st.container():
            col1, col2 = st.columns([1, 12])
            
            if message["role"] == "user":
                with col1:
                    st.image("https://ui-avatars.com/api/?name=You&background=4CAF50&color=fff", width=50)
                with col2:
                    st.markdown(f"""
                    <div class="chat-message user">
                        <div class="message">
                            <span>{message["parts"]}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                with col1:
                    st.image("https://ui-avatars.com/api/?name=Edu&background=2196F3&color=fff", width=50)
                with col2:
                    st.markdown(f"""
                    <div class="chat-message bot">
                        <div class="message">
                            <span>{message["parts"]}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

# User input area
with st.container():
    with st.form(key="query_form", clear_on_submit=True):
        user_input = st.text_area("Your question:", key="input", height=100)
        submit_button = st.form_submit_button(label="Ask EduGenius")
        
    if submit_button and user_input:
        try:
            # Add user message to chat history
            st.session_state.chat_history.append({"role": "user", "parts": user_input})
            
            # Get AI response with a loading indicator
            with st.spinner("EduGenius is thinking..."):
                response = st.session_state.chat.send_message(user_input)
                ai_response = response.text
                
            # Add AI response to chat history
            st.session_state.chat_history.append({"role": "model", "parts": ai_response})
            
            # Rerun to display the updated chat
            st.rerun()
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            
            # If there's an API error, try to restart the chat
            if "chat" in st.session_state:
                st.session_state.chat = start_chat()

# Reset conversation button
if st.button("Start New Conversation"):
    st.session_state.chat_history = []
    st.session_state.chat = start_chat()
    st.rerun()

# Footer
st.markdown("""
---
<p style="text-align: center; color: gray;">
EduGenius is designed for educational purposes only. Always verify critical information with trusted sources.
</p>
""", unsafe_allow_html=True)