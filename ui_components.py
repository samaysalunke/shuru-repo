"""
UI Components for Shuru Tech Chatbot
Modern, responsive components matching the Figma design
"""

import streamlit as st
import json
import os
from collections import Counter


def inject_new_styles():
    """Inject new light theme styles matching Figma design"""
    st.markdown("""
    <style>
    /* Import Inter font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* CSS Variables */
    :root {
        --primary-gradient: linear-gradient(135deg, #00B8A9 0%, #0088FF 100%);
        --text-dark: #1a1a1a;
        --text-light: #666666;
        --bg-white: #FFFFFF;
        --bg-gray: #F5F5F5;
        --border-green: #00B8A9;
        --shadow-light: 0 2px 8px rgba(0, 0, 0, 0.1);
        --border-radius: 12px;
        --border-radius-small: 8px;
    }
    
    /* Global styles - Clean Light Theme */
    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        background: var(--bg-white) !important;
        color: var(--text-dark) !important;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        height: 100vh;
        overflow: hidden;
    }
    
    /* Hide ALL Streamlit default elements */
    header[data-testid="stHeader"] {
        display: none !important;
    }
    
    .stApp > header {
        display: none !important;
    }
    
    #MainMenu {
        display: none !important;
    }
    
    footer {
        display: none !important;
    }
    
    .stDeployButton {
        display: none !important;
    }
    
    /* Hide Streamlit toolbar */
    [data-testid="stToolbar"] {
        display: none !important;
    }
    
    [data-testid="stDecoration"] {
        display: none !important;
    }
    
    .stActionButton {
        display: none !important;
    }
    
    /* Hide Streamlit branding and fork button */
    .stApp > div[data-testid="stDecoration"] {
        display: none !important;
    }
    
    /* Ensure full height without toolbar */
    .main .block-container {
        padding-top: 0 !important;
    }
    
    /* Main container */
    .main {
        height: 100vh;
        overflow: hidden;
        padding: 0 !important;
    }
    
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
    
    /* Header Styles */
    .chat-header {
        position: sticky;
        top: 0;
        z-index: 100;
        background: var(--bg-white);
        border-bottom: 1px solid #e5e5e5;
        padding: 1rem 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .logo-container {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .logo-image {
        height: 32px;
        width: auto;
        max-width: 120px;
        object-fit: contain;
    }
    
    .logo-subtitle {
        font-size: 16px;
        font-weight: 400;
        color: var(--text-light);
        margin: 0;
    }
    
    .help-icon {
        width: 32px;
        height: 32px;
        background: var(--bg-gray);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: var(--text-light);
        font-weight: 600;
        cursor: pointer;
        transition: background 0.2s;
    }
    
    .help-icon:hover {
        background: #e5e5e5;
    }
    
    /* Welcome Screen */
    .welcome-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 60vh;
        padding: 2rem;
        text-align: center;
    }
    
    
    .welcome-title {
        font-size: 28px;
        font-weight: 600;
        color: var(--text-dark);
        margin: 0 0 0.5rem 0;
    }
    
    .welcome-subtitle {
        font-size: 16px;
        color: var(--text-light);
        margin: 0 0 2rem 0;
    }
    
    /* Suggested Questions */
    .questions-container {
        display: flex;
        flex-direction: column;
        gap: 1rem;
        max-width: 600px;
        margin: 0 auto;
        padding: 0 2rem;
    }
    
    .question-button {
        background: var(--bg-white);
        border: 2px solid var(--border-green);
        border-radius: var(--border-radius);
        padding: 1rem 1.5rem;
        font-size: 16px;
        font-weight: 500;
        color: var(--text-dark);
        cursor: pointer;
        transition: all 0.2s;
        text-align: left;
        width: 100%;
    }
    
    .question-button:hover {
        background: #f0fdfa;
        border-color: #00a896;
        transform: translateY(-1px);
        box-shadow: var(--shadow-light);
    }
    
    /* Chat Messages */
    .chat-container {
        height: calc(100vh - 120px);
        overflow-y: auto;
        padding: 1rem 2rem 120px 2rem;
    }
    
    .message-container {
        display: flex;
        margin-bottom: 1.5rem;
        align-items: flex-start;
    }
    
    .message-container:last-child {
        margin-bottom: 2rem;
    }
    
    .message-container.user {
        justify-content: flex-end;
    }
    
    .message-container.assistant {
        justify-content: flex-start;
    }
    
    .message-avatar {
        width: 32px;
        height: 32px;
        background: var(--primary-gradient);
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: 600;
        font-size: 12px;
        margin-right: 0.75rem;
        flex-shrink: 0;
    }
    
    .message-avatar.user {
        margin-right: 0;
        margin-left: 0.75rem;
        background: #e5e5e5;
        color: var(--text-dark);
    }
    
    .message-bubble {
        max-width: 70%;
        padding: 1rem 1.25rem;
        border-radius: var(--border-radius);
        font-size: 16px;
        line-height: 1.5;
        word-wrap: break-word;
        overflow-wrap: break-word;
        box-sizing: border-box;
    }
    
    .message-bubble.user {
        background: var(--primary-gradient);
        color: white;
        border-bottom-right-radius: 4px;
    }
    
    .message-bubble.assistant {
        background: var(--bg-gray);
        color: var(--text-dark);
        border-bottom-left-radius: 4px;
    }
    
    /* Contact Button */
    .contact-button {
        display: inline-block;
        background: var(--primary-gradient);
        color: white;
        padding: 0.75rem 1.5rem;
        border-radius: var(--border-radius-small);
        text-decoration: none;
        font-weight: 500;
        font-size: 14px;
        margin-top: 1rem;
        transition: transform 0.2s;
        max-width: 100%;
        box-sizing: border-box;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    
    .contact-button:hover {
        transform: translateY(-1px);
        text-decoration: none;
        color: white;
    }
    
    /* Chat Input */
    .chat-input-container {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: var(--bg-white);
        border-top: 1px solid #e5e5e5;
        padding: 1rem 2rem;
        z-index: 100;
    }
    
    .stTextInput > div > div > input {
        border-radius: var(--border-radius) !important;
        border: 1px solid #d0d0d0 !important;
        padding: 0.75rem 1rem !important;
        font-size: 16px !important;
        background: var(--bg-white) !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.12), 0 1px 3px rgba(0, 0, 0, 0.08) !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--border-green) !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15), 0 0 0 3px rgba(0, 184, 169, 0.2) !important;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .chat-header {
            padding: 1rem;
        }
        
        .logo-image {
            height: 28px;
            max-width: 100px;
        }
        
        .logo-subtitle {
            font-size: 14px;
        }
        
        .help-icon {
            display: none;
        }
        
        .welcome-container {
            min-height: 50vh;
            padding: 1rem;
        }
        
        
        .welcome-title {
            font-size: 24px;
        }
        
        .welcome-subtitle {
            font-size: 14px;
        }
        
        .questions-container {
            padding: 0 1rem;
        }
        
        .question-button {
            padding: 0.875rem 1.25rem;
            font-size: 14px;
        }
        
        .chat-container {
            padding: 1rem 1rem 100px 1rem;
            height: calc(100vh - 100px);
        }
        
        .message-bubble {
            max-width: 85%;
            padding: 0.875rem 1rem;
            font-size: 14px;
            word-wrap: break-word;
            overflow-wrap: break-word;
            box-sizing: border-box;
        }
        
        .contact-button {
            padding: 0.625rem 1.25rem;
            font-size: 13px;
            margin-top: 0.75rem;
        }
        
        .chat-input-container {
            padding: 1rem;
        }
    }
    
    @media (max-width: 480px) {
        .logo-image {
            height: 24px;
            max-width: 80px;
        }
        
        .logo-subtitle {
            display: none;
        }
        
        .welcome-title {
            font-size: 20px;
        }
        
        .message-bubble {
            max-width: 90%;
            padding: 0.75rem 0.875rem;
        }
        
        .contact-button {
            padding: 0.5rem 1rem;
            font-size: 12px;
            margin-top: 0.5rem;
        }
        
    }
    </style>
    """, unsafe_allow_html=True)


def display_new_header():
    """Display the new header with logo and help icon"""
    st.markdown("""
    <div class="chat-header">
        <div class="logo-container">
            <img src="https://www.shurutech.com/images/logo-black-text.png" alt="Shuru Tech" class="logo-image">
            <div class="logo-subtitle">ShuruNow</div>
        </div>
        <div class="help-icon">?</div>
    </div>
    """, unsafe_allow_html=True)


def display_welcome_screen():
    """Display the welcome screen with greeting"""
    st.markdown("""
    <div class="welcome-container">
        <h1 class="welcome-title">How can I help you today?</h1>
        <p class="welcome-subtitle">Ask me anything or choose from these suggestions</p>
    </div>
    """, unsafe_allow_html=True)


def generate_top_questions():
    """Generate top 3 questions based on knowledge base analysis"""
    try:
        # Load knowledge base
        kb_path = 'knowledge_base.json'
        if not os.path.exists(kb_path):
            return [
                "What services does Shuru Tech offer?",
                "How can AI transform my business operations?", 
                "Tell me about your RAG chatbot capabilities"
            ]
        
        with open(kb_path, 'r') as f:
            data = json.load(f)
        
        case_studies = data.get('case_studies', [])
        if not case_studies:
            return [
                "What services does Shuru Tech offer?",
                "How can AI transform my business operations?",
                "Tell me about your RAG chatbot capabilities"
            ]
        
        # Analyze industries
        industries = [cs.get('industry', '') for cs in case_studies if cs.get('industry')]
        industry_counts = Counter(industries)
        top_industry = industry_counts.most_common(1)[0][0] if industry_counts else "technology"
        
        # Analyze common problems
        problems = [cs.get('problem', '') for cs in case_studies if cs.get('problem')]
        
        # Generate questions based on analysis
        questions = [
            f"Tell me about your {top_industry} solutions",
            "How can you help optimize business operations?",
            "What AI and automation services do you offer?"
        ]
        
        return questions[:3]
        
    except Exception as e:
        # Fallback questions
        return [
            "What services does Shuru Tech offer?",
            "How can AI transform my business operations?",
            "Tell me about your RAG chatbot capabilities"
        ]


def display_suggested_questions():
    """Display suggested question buttons"""
    questions = generate_top_questions()
    
    st.markdown('<div class="questions-container">', unsafe_allow_html=True)
    
    for i, question in enumerate(questions):
        if st.button(question, key=f"suggested_q_{i}", use_container_width=True):
            st.session_state.selected_prompt = question
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)


def display_contact_button():
    """Display the Contact Us button with gradient styling"""
    st.markdown("""
    <div style="margin-top: 1rem;">
        <a href="https://www.shurutech.com/contact-us" target="_blank" style="text-decoration: none;">
            <div class="contact-button">Contact Us</div>
        </a>
    </div>
    """, unsafe_allow_html=True)


def display_chat_message(role, content):
    """Display a chat message with custom styling"""
    if role == "user":
        st.markdown(f"""
        <div class="message-container user">
            <div class="message-bubble user">{content}</div>
            <div class="message-avatar user">You</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="message-container assistant">
            <div class="message-avatar">AI</div>
            <div class="message-bubble assistant">{content}</div>
        </div>
        """, unsafe_allow_html=True)


# Legacy function names for backward compatibility
def inject_dashboard_styles():
    """Legacy function - redirects to new styles"""
    inject_new_styles()


def display_dark_header():
    """Legacy function - redirects to new header"""
    display_new_header()


def display_dark_greeting():
    """Legacy function - redirects to welcome screen"""
    display_welcome_screen()


def display_dark_prompts():
    """Legacy function - redirects to suggested questions"""
    display_suggested_questions()


def display_sales_cta():
    """Legacy function - redirects to contact button"""
    display_contact_button()