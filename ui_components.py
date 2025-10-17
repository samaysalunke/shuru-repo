"""
UI Components for Shuru Tech Dashboard
Modern, responsive components adapted from 21st.dev for Streamlit
"""

import streamlit as st


def inject_dashboard_styles():
    """Inject minimal dashboard styles into Streamlit"""
    st.markdown("""
    <style>
    /* Import Inter font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Global styles - Shuru Tech Brand */
    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        background: #FFFFFF;
        color: #291f3b;
    }
    
    /* Remove default Streamlit padding */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 120px !important;
        max-width: 100%;
    }
    
    /* Hide sidebar */
    [data-testid="stSidebar"] {
        display: none;
    }
    
    /* Removed metric card styles - no longer used */
    
    /* Case study list item */
    .case-study-item {
        background: white;
        border: 1px solid #E5E7EB;
        border-radius: 8px;
        padding: 0.875rem 1rem;
        margin-bottom: 0.5rem;
        cursor: pointer;
        transition: all 0.2s ease;
        display: flex;
        align-items: start;
        gap: 0.75rem;
    }
    
    .case-study-item:hover {
        border-color: #3B82F6;
        background: #F9FAFB;
        transform: translateX(4px);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
    }
    
    .case-study-icon {
        width: 2.25rem;
        height: 2.25rem;
        background: #F3F4F6;
        border-radius: 6px;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
        color: #6B7280;
        font-size: 1rem;
    }
    
    .case-study-item:hover .case-study-icon {
        background: #EFF6FF;
        color: #3B82F6;
    }
    
    .case-study-content {
        flex: 1;
        min-width: 0;
    }
    
    .case-study-client {
        font-size: 0.875rem;
        font-weight: 500;
        color: #1F2937;
        margin-bottom: 0.25rem;
        transition: color 0.2s ease;
    }
    
    .case-study-item:hover .case-study-client {
        color: #3B82F6;
    }
    
    .case-study-industry {
        font-size: 0.75rem;
        color: #6B7280;
    }
    
    /* Chat messages - better spacing */
    [data-testid="stChatMessage"] {
        background: white;
        border: 1px solid #E5E7EB;
        border-radius: 16px;
        padding: 1.25rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 8px rgba(41, 31, 59, 0.08);
        animation: fadeIn 0.4s ease-in;
    }

    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    /* User messages - Shuru Tech Purple */
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
        border-left: 4px solid #291f3b;
        background: #FAFAFA;
    }

    /* Assistant messages - Shuru Tech Purple Accent */
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
        border-left: 4px solid #6B4F9B;
        background: #FFFFFF;
    }

    /* Input placeholder text */
    [data-testid="stChatInput"] input::placeholder {
        color: #9CA3AF !important;
        font-style: italic;
    }

    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
    }

    ::-webkit-scrollbar-track {
        background: #F3F4F6;
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb {
        background: #D1D5DB;
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #9CA3AF;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: #F9FAFB;
        border: 1px solid #E5E7EB;
        border-radius: 8px;
        padding: 0.75rem 1rem;
        font-weight: 500;
        color: #1F2937;
        transition: all 0.2s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background: #F3F4F6;
        border-color: #D1D5DB;
    }
    
    /* Header styles - Shuru Tech Brand */
    .dashboard-header {
        background: linear-gradient(135deg, #FFFFFF 0%, #FAFAFA 100%);
        border-bottom: 3px solid #291f3b;
        padding: 2rem 2.5rem;
        margin: -2rem -2rem 2.5rem -2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 4px 20px rgba(41, 31, 59, 0.12);
        border-radius: 0 0 16px 16px;
    }
    
    .header-left {
        display: flex;
        align-items: center;
        gap: 1.5rem;
    }
    
    .dashboard-logo {
        height: 48px;
        vertical-align: middle;
        filter: drop-shadow(0 2px 4px rgba(41, 31, 59, 0.1));
    }
    
    .header-content {
        display: flex;
        flex-direction: column;
        gap: 0.25rem;
    }
    
    .dashboard-title {
        font-size: 2rem;
        font-weight: 800;
        color: #291f3b;
        margin: 0;
        letter-spacing: -0.5px;
        text-shadow: 0 1px 2px rgba(41, 31, 59, 0.1);
    }
    
    .dashboard-subtitle {
        font-size: 1rem;
        color: #64748B;
        margin: 0;
        font-weight: 500;
        line-height: 1.4;
    }
    
    /* Panel headers */
    .panel-header {
        font-size: 1.125rem;
        font-weight: 600;
        color: #1F2937;
        margin-bottom: 1rem;
        padding-bottom: 0.75rem;
        border-bottom: 2px solid #E5E7EB;
    }
    
    /* Removed status badge styles - no longer used */
    
    /* Chat container - full height with scroll */
    .chat-container {
        height: calc(100vh - 250px);
        overflow-y: auto;
        padding-bottom: 1rem;
    }
    
    /* Chat input - force to viewport bottom */
    [data-testid="stChatInput"] {
        position: fixed !important;
        bottom: 0 !important;
        left: 0 !important;
        right: 0 !important;
        background: white;
        padding: 1.5rem 2rem;
        z-index: 1000;
        border-top: 2px solid #E5E7EB;
        box-shadow: 0 -4px 12px rgba(0, 0, 0, 0.1);
    }
    
    /* Center the input field within the fixed container */
    [data-testid="stChatInput"] > div {
        max-width: 1200px;
        margin: 0 auto;
    }
    
    [data-testid="stChatInput"] input,
    [data-testid="stChatInput"] textarea {
        border: 2px solid #E2E8F0 !important;
        border-radius: 12px !important;
        padding: 0.875rem 1rem !important;
        font-size: 0.875rem !important;
        transition: all 0.2s ease !important;
        background: #FFFFFF !important;
        color: #291f3b !important;
    }
    
    [data-testid="stChatInput"] input:focus,
    [data-testid="stChatInput"] textarea:focus {
        border-color: #291f3b !important;
        box-shadow: 0 0 0 3px rgba(41, 31, 59, 0.1) !important;
        outline: none !important;
    }

    /* Clickable prompts styling */
    .prompt-section {
        text-align: center;
        padding: 3rem 2rem;
        background: linear-gradient(135deg, #FAFAFA 0%, #F8F9FA 100%);
        border-radius: 20px;
        margin: 2rem 0;
        border: 2px solid #F1F5F9;
    }

    .prompt-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #291f3b;
        margin-bottom: 0.5rem;
    }

    .prompt-subtitle {
        font-size: 1rem;
        color: #64748B;
        margin-bottom: 2rem;
        font-weight: 500;
    }

    .prompt-button {
        background: linear-gradient(135deg, #FFFFFF 0%, #FAFAFA 100%);
        border: 2px solid #E2E8F0;
        border-radius: 16px;
        padding: 1.25rem 1.5rem;
        margin: 0.5rem 0;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(41, 31, 59, 0.08);
        text-align: left;
        width: 100%;
        font-size: 0.95rem;
        font-weight: 600;
        color: #291f3b;
        line-height: 1.4;
    }

    .prompt-button:hover {
        border-color: #291f3b;
        background: linear-gradient(135deg, #291f3b 0%, #3d2f5a 100%);
        color: white;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(41, 31, 59, 0.2);
    }

    .prompt-icon {
        font-size: 1.25rem;
        margin-right: 0.75rem;
        vertical-align: middle;
    }
    </style>
    """, unsafe_allow_html=True)


# Removed: display_metric_card() - no longer used in two-column layout


def display_case_study_item(client_name, industry, icon="💼"):
    """Display a case study list item"""
    html = f"""
    <div class="case-study-item">
        <div class="case-study-icon">{icon}</div>
        <div class="case-study-content">
            <div class="case-study-client">{client_name}</div>
            <div class="case-study-industry">{industry}</div>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def display_panel_header(title):
    """Display a panel header"""
    st.markdown(f'<div class="panel-header">{title}</div>', unsafe_allow_html=True)


# Removed: display_status_badge() - no longer used in two-column layout


def display_dashboard_header(title, subtitle=""):
    """Display dashboard header with Shuru Tech branding"""
    html = f"""
    <div class="dashboard-header">
        <div class="header-left">
            <img src="https://www.shurutech.com/images/logo-black-text.png" 
                 alt="Shuru Tech" 
                 class="dashboard-logo" />
            <div class="header-content">
                <h1 class="dashboard-title">{title}</h1>
                {f'<p class="dashboard-subtitle">{subtitle}</p>' if subtitle else ''}
            </div>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def display_sales_cta():
    """Display a prominent CTA button for contacting Shuru Tech"""
    html = f"""
    <div style="margin: 1.5rem 0; padding: 1.25rem; background: linear-gradient(135deg, #FAFAFA 0%, #F8F9FA 100%); border: 2px solid #291f3b; border-radius: 16px; text-align: center; box-shadow: 0 4px 16px rgba(41, 31, 59, 0.12);">
        <p style="margin: 0 0 1rem 0; font-size: 1rem; color: #291f3b; font-weight: 600; line-height: 1.5;">
            💡 Ready to build smarter and scale faster?
        </p>
        <a href="https://www.shurutech.com/contact-us" target="_blank" style="text-decoration: none;">
            <button style="
                background: linear-gradient(135deg, #291f3b 0%, #3d2f5a 100%);
                color: white;
                border: none;
                padding: 0.875rem 2.5rem;
                border-radius: 12px;
                font-size: 1.05rem;
                font-weight: 700;
                cursor: pointer;
                box-shadow: 0 6px 20px rgba(41, 31, 59, 0.3);
                transition: all 0.3s ease;
                letter-spacing: 0.5px;
            "
            onmouseover="this.style.transform='translateY(-3px)'; this.style.boxShadow='0 8px 24px rgba(41, 31, 59, 0.4)';"
            onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 6px 20px rgba(41, 31, 59, 0.3)';">
                Contact Us
            </button>
        </a>
        <p style="margin: 1rem 0 0 0; font-size: 0.875rem; color: #64748B; font-weight: 500;">
            Let's discuss how we can help transform your business
        </p>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def display_chat_prompts():
    """Display clickable prompts when chat is empty"""
    html = f"""
    <div class="prompt-section">
        <h2 class="prompt-title">👋 How can I help you today?</h2>
        <p class="prompt-subtitle">Choose a prompt to get started with Shuru Tech's AI assistant</p>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
    
    # Create three columns for the prompts
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🚀 What services does Shuru Tech offer?", key="prompt1", use_container_width=True):
            st.session_state.selected_prompt = "What services does Shuru Tech offer?"
            st.rerun()
    
    with col2:
        if st.button("🤖 How can AI transform my business operations?", key="prompt2", use_container_width=True):
            st.session_state.selected_prompt = "How can AI transform my business operations?"
            st.rerun()
    
    with col3:
        if st.button("💬 Tell me about your RAG chatbot capabilities", key="prompt3", use_container_width=True):
            st.session_state.selected_prompt = "Tell me about your RAG chatbot capabilities"
            st.rerun()

