"""
21st.dev UI Components for Shuru Tech Chatbot
Modern, responsive chat interface using 21st.dev components
"""

import streamlit as st
from typing import List, Dict, Any

def inject_21st_styles():
    """Inject 21st.dev inspired styles for modern chat interface"""
    st.markdown("""
    <style>
    /* 21st.dev Modern Chat Interface Styles */
    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        background: #ffffff;
        color: #1a1a1a;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        height: 100vh;
        overflow: hidden;
    }
    
    /* Remove default Streamlit padding */
    .main .block-container {
        padding: 0;
        max-width: 100%;
        background: #ffffff;
    }
    
    /* Hide sidebar */
    .stSidebar {
        display: none;
    }
    
    /* Modern header */
    .chat-header {
        background: #ffffff;
        border-bottom: 1px solid #e5e7eb;
        padding: 1rem 1.5rem;
        display: flex;
        justify-content: center;
        align-items: center;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        height: 60px;
    }
    
    .shuru-logo {
        height: 32px;
        filter: none;
        display: block;
        margin: 0 auto;
    }
    
    /* Main chat container */
    .chat-container {
        background: #ffffff;
        height: calc(100vh - 120px);
        display: flex;
        flex-direction: column;
        overflow: hidden;
    }
    
    /* Empty state - centered greeting */
    .empty-state {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100%;
        padding: 2rem;
        text-align: center;
    }
    
    .greeting-title {
        font-size: 2rem;
        font-weight: 600;
        color: #1a1a1a;
        margin-bottom: 0.5rem;
    }
    
    .greeting-subtitle {
        font-size: 1rem;
        color: #6b7280;
        margin-bottom: 2rem;
    }
    
    /* Modern prompt buttons - Streamlit button styling */
    .stButton > button {
        background: #f9fafb !important;
        border: 1px solid #e5e7eb !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        color: #1a1a1a !important;
        font-size: 0.875rem !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
        text-align: left !important;
        display: flex !important;
        align-items: center !important;
        gap: 0.75rem !important;
        min-height: 60px !important;
        width: 100% !important;
        justify-content: flex-start !important;
    }
    
    .stButton > button:hover {
        background: #f3f4f6 !important;
        border-color: #d1d5db !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1) !important;
    }
    
    .stButton > button:focus {
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
        border-color: #3b82f6 !important;
    }
    
    /* Chat messages area */
    .chat-messages {
        flex: 1;
        overflow-y: auto;
        padding: 1rem;
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }
    
    /* Message bubbles */
    .message-bubble {
        display: flex;
        align-items: flex-start;
        gap: 0.75rem;
        max-width: 80%;
    }
    
    .message-bubble.user {
        align-self: flex-end;
        flex-direction: row-reverse;
    }
    
    .message-bubble.assistant {
        align-self: flex-start;
    }
    
    .message-content {
        background: #f3f4f6;
        border-radius: 12px;
        padding: 0.75rem 1rem;
        font-size: 0.875rem;
        line-height: 1.5;
        color: #1a1a1a;
        word-wrap: break-word;
    }
    
    .message-bubble.user .message-content {
        background: #3b82f6;
        color: #ffffff;
    }
    
    .message-avatar {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        background: #e5e7eb;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.75rem;
        font-weight: 600;
        color: #6b7280;
        flex-shrink: 0;
    }
    
    .message-bubble.user .message-avatar {
        background: #3b82f6;
        color: #ffffff;
    }
    
    /* Modern input area */
    .chat-input-container {
        background: #ffffff;
        border-top: 1px solid #e5e7eb;
        padding: 1rem 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .chat-input {
        flex: 1;
        background: #f9fafb;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 0.75rem 1rem;
        font-size: 0.875rem;
        color: #1a1a1a;
        resize: none;
        min-height: 44px;
        max-height: 120px;
        font-family: inherit;
    }
    
    .chat-input:focus {
        outline: none;
        border-color: #3b82f6;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    }
    
    .chat-input::placeholder {
        color: #9ca3af;
    }
    
    .send-button {
        background: #3b82f6;
        color: #ffffff;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1rem;
        font-size: 0.875rem;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s ease;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .send-button:hover {
        background: #2563eb;
        transform: translateY(-1px);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    .send-button:disabled {
        background: #9ca3af;
        cursor: not-allowed;
        transform: none;
        box-shadow: none;
    }
    
    /* Mobile responsive */
    @media screen and (max-width: 768px) {
        .chat-header {
            padding: 0.75rem 1rem;
        }
        
        .shuru-logo {
            height: 28px;
        }
        
        .empty-state {
            padding: 1rem;
        }
        
        .greeting-title {
            font-size: 1.5rem;
        }
        
        .prompt-grid {
            grid-template-columns: 1fr;
            gap: 0.75rem;
        }
        
        .prompt-button {
            padding: 0.75rem;
            min-height: 50px;
        }
        
        .chat-input-container {
            padding: 0.75rem 1rem;
        }
        
        .message-bubble {
            max-width: 90%;
        }
    }
    
    /* Scrollbar styling */
    .chat-messages::-webkit-scrollbar {
        width: 4px;
    }
    
    .chat-messages::-webkit-scrollbar-track {
        background: transparent;
    }
    
    .chat-messages::-webkit-scrollbar-thumb {
        background: #d1d5db;
        border-radius: 2px;
    }
    
    .chat-messages::-webkit-scrollbar-thumb:hover {
        background: #9ca3af;
    }
    
    /* Fixed Contact Us Button */
    .contact-button-container {
        position: fixed;
        bottom: 80px;
        right: 1.5rem;
        z-index: 999;
    }
    
    .contact-button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: #ffffff;
        border: none;
        border-radius: 50px;
        padding: 0.875rem 1.5rem;
        font-size: 0.875rem;
        font-weight: 600;
        cursor: pointer;
        box-shadow: 0 4px 14px rgba(59, 130, 246, 0.4);
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        text-decoration: none;
    }
    
    .contact-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.5);
        color: #ffffff;
        text-decoration: none;
    }
    
    /* Mobile responsive contact button */
    @media screen and (max-width: 768px) {
        .contact-button-container {
            bottom: 70px;
            right: 1rem;
        }
        
        .contact-button {
            padding: 0.75rem 1.25rem;
            font-size: 0.8rem;
        }
    }
    
    /* Enhanced message content styling */
    .message-content ul {
        margin: 0.5rem 0;
        padding-left: 1.5rem;
    }
    
    .message-content li {
        margin: 0.25rem 0;
        line-height: 1.6;
    }
    
    .message-content strong {
        color: #1a1a1a;
        font-weight: 600;
        display: block;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }
    
    .message-content p {
        margin: 0.75rem 0;
        line-height: 1.6;
    }
    
    /* Streamlit markdown styling for chat */
    [data-testid="stChatMessage"] p {
        margin: 0.5rem 0;
    }
    
    [data-testid="stChatMessage"] ul {
        margin: 0.5rem 0;
        padding-left: 1.5rem;
    }
    
    [data-testid="stChatMessage"] strong {
        color: #1a1a1a;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)

def display_21st_header():
    """Display modern header with Shuru logo"""
    st.markdown("""
    <div class="chat-header">
        <img src="https://www.shurutech.com/images/logo-black-text.png" 
             alt="Shuru Tech" 
             class="shuru-logo" />
    </div>
    """, unsafe_allow_html=True)

def display_21st_empty_state():
    """Display modern empty state with greeting and prompts"""
    st.markdown("""
    <div class="empty-state">
        <h1 class="greeting-title">How can I help you today?</h1>
        <p class="greeting-subtitle">Ask me anything about Shuru Tech's services and capabilities</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display prompt buttons using Streamlit columns
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🚀 What services does Shuru Tech offer?", key="prompt_services", use_container_width=True):
            st.session_state.selected_prompt = "What services does Shuru Tech offer?"
            st.rerun()
        
        if st.button("🤖 How can AI transform my business operations?", key="prompt_ai", use_container_width=True):
            st.session_state.selected_prompt = "How can AI transform my business operations?"
            st.rerun()
    
    with col2:
        if st.button("💬 Tell me about your RAG chatbot capabilities", key="prompt_rag", use_container_width=True):
            st.session_state.selected_prompt = "Tell me about your RAG chatbot capabilities"
            st.rerun()
        
        if st.button("📊 Show me some successful case studies", key="prompt_cases", use_container_width=True):
            st.session_state.selected_prompt = "Show me some successful case studies"
            st.rerun()

def display_21st_chat_messages(messages: List[Dict[str, Any]]):
    """Display chat messages in modern bubble format"""
    if not messages:
        return
    
    st.markdown('<div class="chat-messages">', unsafe_allow_html=True)
    
    for message in messages:
        role = message["role"]
        content = message["content"]
        
        if role == "user":
            st.markdown(f"""
            <div class="message-bubble user">
                <div class="message-avatar">U</div>
                <div class="message-content">{content}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="message-bubble assistant">
                <div class="message-avatar">AI</div>
                <div class="message-content">{content}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def display_21st_chat_input():
    """Display modern chat input using Streamlit's chat_input"""
    # Use Streamlit's built-in chat input with custom styling
    st.markdown("""
    <style>
    [data-testid="stChatInput"] {
        background: #f9fafb !important;
        border: 1px solid #e5e7eb !important;
        border-radius: 12px !important;
        padding: 0.75rem 1rem !important;
    }
    
    [data-testid="stChatInput"] input {
        background: transparent !important;
        border: none !important;
        color: #1a1a1a !important;
        font-size: 0.875rem !important;
    }
    
    [data-testid="stChatInput"] input:focus {
        outline: none !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
    }
    
    [data-testid="stChatInput"] input::placeholder {
        color: #9ca3af !important;
    }
    </style>
    """, unsafe_allow_html=True)

def display_21st_sales_cta():
    """Display modern sales CTA"""
    st.markdown("""
    <div style="margin-top: 1rem; padding: 1rem; background: #f0f9ff; border: 1px solid #bae6fd; border-radius: 8px;">
        <h4 style="margin: 0 0 0.5rem 0; color: #0369a1; font-size: 0.875rem; font-weight: 600;">
            Ready to transform your business?
        </h4>
        <p style="margin: 0 0 1rem 0; color: #0c4a6e; font-size: 0.875rem; line-height: 1.4;">
            Let's discuss how Shuru Tech can help you achieve your goals with AI and modern technology.
        </p>
        <a href="https://www.shurutech.com/contact" 
           style="display: inline-block; background: #3b82f6; color: white; padding: 0.5rem 1rem; border-radius: 6px; text-decoration: none; font-size: 0.875rem; font-weight: 500;">
            Get in Touch →
        </a>
    </div>
    """, unsafe_allow_html=True)

def display_fixed_contact_button():
    """Display fixed Contact Us button"""
    st.markdown("""
    <div class="contact-button-container">
        <a href="https://www.shurutech.com/contact" 
           target="_blank" 
           class="contact-button">
            <span>💼</span>
            <span>Contact Us</span>
        </a>
    </div>
    """, unsafe_allow_html=True)
