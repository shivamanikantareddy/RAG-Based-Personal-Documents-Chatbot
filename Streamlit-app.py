import streamlit as st
import requests
from typing import List
import time

# Configuration
API_BASE_URL = "http://localhost:8000"  # Change this to your backend URL

# Page configuration
st.set_page_config(
    page_title="Personal Knowledge Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for beautiful UI
st.markdown("""
    <style>
    /* Main container styling */
    .main {
        padding: 2rem;
    }
    
    /* Header styling */
    .header-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    .header-title {
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-align: center;
    }
    
    .header-subtitle {
        color: rgba(255,255,255,0.9);
        font-size: 1.1rem;
        text-align: center;
        margin-top: 0.5rem;
    }
    
    /* Button styling */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        border-radius: 10px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* File uploader styling */
    .uploadedFile {
        background: #f8f9fa;
        color: black;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
    }
    
    /* Chat message styling */
    .chat-message {
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1rem;
        animation: slideIn 0.3s ease;
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: 20%;
    }
    
    .assistant-message {
        background: #f8f9fa;
        color: #333;
        margin-right: 20%;
        border: 1px solid #e9ecef;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Success/Error message styling */
    .success-box {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .error-box {
        background: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    /* Info card styling */
    .info-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
    
    /* Loading animation */
    .loading {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(102, 126, 234, 0.3);
        border-radius: 50%;
        border-top-color: #667eea;
        animation: spin 1s ease-in-out infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'files_uploaded' not in st.session_state:
    st.session_state.files_uploaded = False

def check_api_health():
    """Check if the backend API is available"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def render_header():
    """Render the header section"""
    st.markdown("""
        <div class="header-container">
            <h1 class="header-title">🤖 Personal Knowledge Assistant</h1>
            <p class="header-subtitle">Your intelligent document companion powered by AI</p>
        </div>
    """, unsafe_allow_html=True)

def home_page():
    """Render the home page"""
    render_header()
    
    # Check API health
    if not check_api_health():
        st.error("⚠️ Backend API is not available. Please ensure the FastAPI server is running.")
        return
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
            <div class="info-card">
                <h2 style="color: #667eea; text-align: center;">Welcome! 👋</h2>
                <p style="text-align: center; font-size: 1.1rem; color: #555;">
                    Upload your documents and start chatting with your personal AI assistant.
                    Your documents will be processed and indexed for intelligent conversations.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Features section
        st.markdown("### ✨ Features")
        
        features_col1, features_col2 = st.columns(2)
        
        with features_col1:
            st.markdown("""
                - 📄 **Multiple File Support**
                - 🔍 **Smart Document Search**
                - 💬 **Natural Conversations**
            """)
        
        with features_col2:
            st.markdown("""
                - 🧠 **Context-Aware Responses**
                - 🚀 **Fast Processing**
                - 🔒 **Secure & Private**
            """)
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # Upload files button
        if st.button("📤 Upload Files", key="upload_btn", use_container_width=True):
            st.session_state.page = 'upload'
            st.rerun()
        
        # If files already uploaded, show chat option
        if st.session_state.files_uploaded:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("💬 Go to Chat", key="chat_btn", use_container_width=True):
                st.session_state.page = 'chat'
                st.rerun()

def upload_page():
    """Render the file upload page"""
    render_header()
    
    # Back button
    if st.button("← Back to Home", key="back_home"):
        st.session_state.page = 'home'
        st.rerun()
    
    st.markdown("## 📤 Upload Your Documents")
    st.markdown("Select one or more files to upload. Supported formats include - Scanned PDF, PDF, TXT, DOCX, PPTX, and more.")
    
    # File uploader
    uploaded_files = st.file_uploader(
        "Choose files",
        accept_multiple_files=True,
        type=['pdf', 'txt', 'docx', 'pptx', 'xlsx', 'xls', 'csv', 'md'],
        help="Upload documents you want to chat about"
    )
    
    if uploaded_files:
        st.markdown("### 📋 Selected Files")
        
        # Display selected files
        for idx, file in enumerate(uploaded_files, 1):
            file_size = len(file.getvalue()) / (1024 * 1024)  # Convert to MB
            st.markdown(f"""
                <div class="uploadedFile">
                    <strong>{idx}. {file.name}</strong><br>
                    <small>Size: {file_size:.2f} MB | Type: {file.type}</small>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Upload button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 Process & Upload Files", key="process_btn", use_container_width=True):
                with st.spinner("Processing and storing your files... This may take a moment."):
                    try:
                        # Prepare files for upload
                        files_data = []
                        for file in uploaded_files:
                            file.seek(0)  # Reset file pointer
                            files_data.append(
                                ('files', (file.name, file.getvalue(), file.type))
                            )
                        
                        # Send request to backend
                        response = requests.post(
                            f"{API_BASE_URL}/load_knowledge",
                            files=files_data,
                            timeout=300  # 5 minutes timeout for large files
                        )
                        
                        if response.status_code == 200:
                            st.markdown("""
                                <div class="success-box">
                                    ✅ <strong>Success!</strong> Your files have been processed and stored successfully.
                                </div>
                            """, unsafe_allow_html=True)
                            
                            st.session_state.files_uploaded = True
                            time.sleep(1)
                            
                            # Redirect to chat
                            st.session_state.page = 'chat'
                            st.rerun()
                        else:
                            error_message = response.json().get('detail', 'Unknown error occurred')
                            st.markdown(f"""
                                <div class="error-box">
                                    ❌ <strong>Error:</strong> {error_message}
                                </div>
                            """, unsafe_allow_html=True)
                    
                    except requests.exceptions.Timeout:
                        st.markdown("""
                            <div class="error-box">
                                ⏱️ <strong>Timeout:</strong> The request took too long. Please try with smaller files.
                            </div>
                        """, unsafe_allow_html=True)
                    
                    except Exception as e:
                        st.markdown(f"""
                            <div class="error-box">
                                ❌ <strong>Error:</strong> {str(e)}
                            </div>
                        """, unsafe_allow_html=True)

def chat_page():
    """Render the chat interface page"""
    render_header()
    
    # Navigation buttons
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("← Back to Home", key="back_home_chat"):
            st.session_state.page = 'home'
            st.rerun()
    
    with col2:
        if st.button("🗑️ Clear Conversation", key="clear_chat"):
            try:
                # Send quit command to backend
                response = requests.post(
                    f"{API_BASE_URL}/chat_assistant",
                    json={"query": "quit"},
                    timeout=10
                )
                st.session_state.chat_history = []
                st.success("Conversation cleared!")
                time.sleep(1)
                st.rerun()
            except Exception as e:
                st.error(f"Error clearing conversation: {str(e)}")
    
    st.markdown("## 💬 Chat with Your Documents")
    st.markdown("Ask questions about your uploaded documents and get intelligent responses.")
    
    # Chat container
    chat_container = st.container()
    
    # Display chat history
    with chat_container:
        if st.session_state.chat_history:
            for message in st.session_state.chat_history:
                if message['role'] == 'user':
                    st.markdown(f"""
                        <div class="chat-message user-message">
                            <strong>You:</strong><br>
                            {message['content']}
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                        <div class="chat-message assistant-message">
                            <strong>🤖 Assistant:</strong><br>
                            {message['content']}
                        </div>
                    """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div class="info-card">
                    <p style="text-align: center; color: #667eea; font-size: 1.1rem;">
                        👋 Start a conversation by typing your question below!
                    </p>
                </div>
            """, unsafe_allow_html=True)
    
    # Chat input
    st.markdown("<br>", unsafe_allow_html=True)
    
    with st.form(key='chat_form', clear_on_submit=True):
        user_input = st.text_input(
            "Your question:",
            placeholder="Ask me anything about your documents...",
            label_visibility="collapsed"
        )
        submit_button = st.form_submit_button("Send 📤", use_container_width=True)
    
    if submit_button and user_input.strip():
        # Add user message to chat history
        st.session_state.chat_history.append({
            'role': 'user',
            'content': user_input
        })
        
        # Show loading state
        with st.spinner("Thinking..."):
            try:
                # Send request to backend
                response = requests.post(
                    f"{API_BASE_URL}/chat_assistant",
                    json={"query": user_input},
                    timeout=60
                )
                
                if response.status_code == 200:
                    response_data = response.json()
                    assistant_response = response_data.get('response', 'No response received')
                    
                    # Add assistant message to chat history
                    st.session_state.chat_history.append({
                        'role': 'assistant',
                        'content': assistant_response
                    })
                    
                    st.rerun()
                else:
                    error_message = response.json().get('error', 'Unknown error occurred')
                    st.error(f"Error: {error_message}")
            
            except requests.exceptions.Timeout:
                st.error("Request timeout. Please try again.")
            
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

# Main app logic
def main():
    if st.session_state.page == 'home':
        home_page()
    elif st.session_state.page == 'upload':
        upload_page()
    elif st.session_state.page == 'chat':
        chat_page()

if __name__ == "__main__":
    main()
