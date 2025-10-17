"""
UI Components for Shuru Tech Dashboard
Modern, responsive components adapted from 21st.dev for Streamlit
"""

import streamlit as st


def inject_dashboard_styles():
    """Inject dark ChatGPT-style dashboard styles into Streamlit"""
    st.markdown("""
    <style>
    /* Import Inter font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Global styles - Clean Light Theme */
    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        background: #ffffff !important;
        color: #1a1a1a !important;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        height: 100vh;
        overflow: hidden;
    }
    
    /* Ensure no scrolling on main container */
    .main {
        height: 100vh;
        overflow: hidden;
    }
    
    /* Force dark text on all elements */
    .stApp * {
        color: #1a1a1a !important;
    }
    
    /* Override Streamlit default text colors */
    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6 {
        color: #1a1a1a !important;
    }
    
    .stApp p, .stApp div, .stApp span {
        color: #1a1a1a !important;
    }
    
    .stApp button {
        color: #1a1a1a !important;
    }
    
    /* Ensure no scrolling in empty state */
    .main {
        height: 100vh;
        overflow: hidden;
    }
    
    /* Touch-friendly interactions */
    * {
        -webkit-tap-highlight-color: rgba(41, 31, 59, 0.1);
    }
    
    /* Better text rendering on mobile */
    body {
        -webkit-text-size-adjust: 100%;
        -ms-text-size-adjust: 100%;
    }
    
    /* Remove default Streamlit padding */
    .main .block-container {
        padding: 0;
        max-width: 100%;
        background: #ffffff;
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
    
    /* Clean light header */
    .dashboard-header {
        background: #ffffff;
        border-bottom: 1px solid #e5e7eb;
        padding: 1rem 1.5rem;
        margin: 0;
        display: flex;
        justify-content: center;
        align-items: center;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        border-radius: 0;
        height: 60px;
    }
    
    .shuru-logo {
        height: 32px;
        filter: none;
        display: block;
        margin: 0 auto;
    }
    
    /* Main content area - prevent scrolling */
    .main-content {
        background: #ffffff;
        height: calc(100vh - 180px);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: flex-start;
        padding: 2rem;
        overflow: hidden;
    }
    
    /* Chat messages container - scrollable within main content */
    .chat-messages-container {
        width: 100%;
        max-width: 800px;
        flex: 1;
        overflow-y: auto;
        padding-bottom: 1rem;
        max-height: calc(100vh - 300px);
    }
    
    /* Hide greeting when chat messages exist */
    .main-content:has(.chat-messages-container) .greeting-text {
        display: none;
    }
    
    /* Chat message styling */
    [data-testid="stChatMessage"] {
        background: #ffffff !important;
        border: 1px solid #e5e7eb !important;
        color: #1a1a1a !important;
        margin-bottom: 1rem !important;
    }
    
    /* Hide greeting and prompts when chat is active */
    .main-content:has([data-testid="stChatMessage"]) .greeting-text,
    .main-content:has([data-testid="stChatMessage"]) .prompt-buttons-container {
        display: none;
    }
    
    /* Override Streamlit button styles for light theme */
    .stApp button[kind="primary"],
    .stApp button[kind="secondary"],
    .stApp .stButton > button {
        background: #f9fafb !important;
        color: #1a1a1a !important;
        border: 1px solid #d1d5db !important;
    }
    
    .stApp button:hover {
        background: #f3f4f6 !important;
        color: #1a1a1a !important;
        border-color: #9ca3af !important;
    }
    
    .greeting-text {
        font-size: 2rem;
        font-weight: 600;
        color: #1a1a1a !important;
        text-align: center;
        margin: 0;
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
    
    /* Light input bar */
    [data-testid="stChatInput"] {
        position: fixed !important;
        bottom: 0 !important;
        left: 0 !important;
        right: 0 !important;
        background: #ffffff !important;
        padding: 1rem 1.5rem !important;
        z-index: 1000 !important;
        border-top: 1px solid #e5e7eb !important;
        box-shadow: 0 -1px 3px rgba(0, 0, 0, 0.1) !important;
        display: block !important;
    }
    
    /* Center the input field within the fixed container */
    [data-testid="stChatInput"] > div {
        max-width: 800px;
        margin: 0 auto;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    /* Hide Streamlit input buttons we don't want */
    [data-testid="stChatInput"] button[title="Attach files"] {
        display: none !important;
    }
    
    [data-testid="stChatInput"] button[title="Voice input"] {
        display: none !important;
    }
    
    [data-testid="stChatInput"] input,
    [data-testid="stChatInput"] textarea {
        background: #f9fafb !important;
        border: 1px solid #d1d5db !important;
        border-radius: 12px !important;
        padding: 0.875rem 1rem !important;
        font-size: 0.875rem !important;
        color: #1a1a1a !important;
        flex: 1;
    }
    
    [data-testid="stChatInput"] input::placeholder,
    [data-testid="stChatInput"] textarea::placeholder {
        color: #6b7280 !important;
    }
    
    [data-testid="stChatInput"] input:focus,
    [data-testid="stChatInput"] textarea:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2) !important;
        outline: none !important;
    }
    
    /* Prompt buttons below input */
    .prompt-buttons-container {
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
        margin-top: 2rem;
        max-width: 600px;
        width: 100%;
    }
    
    .prompt-button-row {
        display: flex;
        gap: 0.75rem;
        justify-content: center;
    }
    
    .prompt-button {
        background: #f9fafb !important;
        border: 1px solid #d1d5db !important;
        border-radius: 12px;
        padding: 0.75rem 1rem;
        color: #1a1a1a !important;
        cursor: pointer;
        font-size: 0.875rem;
        font-weight: 500;
        transition: all 0.2s ease;
        flex: 1;
        text-align: center;
    }
    
    .prompt-button:hover {
        background: #f3f4f6 !important;
        border-color: #9ca3af !important;
        color: #1a1a1a !important;
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
    
    /* ============================================ */
    /* MOBILE RESPONSIVE STYLES */
    /* ============================================ */
    
    /* Tablets and smaller (max-width: 768px) */
    @media screen and (max-width: 768px) {
        /* Reduce padding on mobile */
        .main .block-container {
            padding-top: 1rem;
            padding-left: 1rem;
            padding-right: 1rem;
            padding-bottom: 100px !important;
        }
        
        /* Stack Streamlit columns on mobile */
        [data-testid="column"] {
            width: 100% !important;
            flex: 0 0 100% !important;
        }
        
        /* Remove column gaps on mobile */
        [data-testid="stHorizontalBlock"] {
            gap: 0 !important;
            flex-direction: column !important;
        }
        
        /* Mobile header adjustments */
        .dashboard-header {
            padding: 1rem;
            background: #ffffff;
            border-bottom: 1px solid #e5e7eb;
        }
        
        .greeting-text {
            font-size: 1.5rem;
            color: #1a1a1a !important;
        }
        
        .main-content {
            padding: 1rem;
            height: calc(100vh - 100px);
            background: #ffffff;
        }
        
        /* Mobile prompt buttons */
        .prompt-buttons-container {
            margin-top: 1.5rem;
        }
        
        .prompt-button {
            font-size: 0.8125rem;
            padding: 0.625rem 0.875rem;
        }
        
        .header-left {
            flex-direction: column;
            align-items: flex-start;
            gap: 0.5rem;
            width: 100%;
        }
        
        .dashboard-logo {
            height: 32px;
        }
        
        .dashboard-title {
            font-size: 1.25rem;
            letter-spacing: -0.3px;
        }
        
        .dashboard-subtitle {
            font-size: 0.8125rem;
            line-height: 1.3;
        }
        
        /* Mobile chat messages */
        [data-testid="stChatMessage"] {
            padding: 1rem;
            margin-bottom: 1rem;
            border-radius: 12px;
        }
        
        /* Mobile chat input */
        [data-testid="stChatInput"] {
            padding: 1rem;
        }
        
        [data-testid="stChatInput"] input,
        [data-testid="stChatInput"] textarea {
            padding: 0.75rem !important;
            font-size: 0.875rem !important;
        }
        
        /* Mobile prompt section */
        .prompt-section {
            padding: 2rem 1rem;
            margin: 1rem 0;
            border-radius: 16px;
        }
        
        .prompt-title {
            font-size: 1.25rem;
        }
        
        .prompt-subtitle {
            font-size: 0.875rem;
            margin-bottom: 1.5rem;
        }
        
        .prompt-button {
            padding: 1rem 1.25rem;
            font-size: 0.875rem;
            border-radius: 12px;
        }
        
        /* Mobile case study items */
        .case-study-item {
            padding: 0.75rem;
            gap: 0.5rem;
        }
        
        .case-study-icon {
            width: 1.75rem;
            height: 1.75rem;
            font-size: 0.875rem;
        }
        
        .case-study-client {
            font-size: 0.8125rem;
        }
        
        .case-study-industry {
            font-size: 0.6875rem;
        }
        
        /* Mobile CTA */
        .sales-cta-container {
            padding: 1rem !important;
            margin: 1rem 0 !important;
            border-radius: 12px !important;
        }
        
        .cta-button {
            padding: 0.75rem 2rem !important;
            font-size: 0.95rem !important;
            min-height: 44px !important;
        }
        
        .cta-message, .cta-subtitle {
            font-size: 0.8125rem !important;
        }
        
        /* Touch-friendly button sizes */
        button {
            min-height: 44px !important;
            touch-action: manipulation;
        }
        
        /* Better touch targets for prompts */
        .prompt-button {
            min-height: 48px !important;
        }
    }
    
    /* Small mobile phones (max-width: 480px) */
    @media screen and (max-width: 480px) {
        .main .block-container {
            padding-left: 0.75rem;
            padding-right: 0.75rem;
        }
        
        .dashboard-header {
            padding: 0.75rem;
            margin: -1rem -0.75rem 1rem -0.75rem;
        }
        
        .dashboard-logo {
            height: 28px;
        }
        
        .dashboard-title {
            font-size: 1.125rem;
        }
        
        .dashboard-subtitle {
            font-size: 0.8125rem;
        }
        
        [data-testid="stChatMessage"] {
            padding: 0.875rem;
        }
        
        [data-testid="stChatInput"] {
            padding: 0.75rem;
        }
        
        .prompt-section {
            padding: 1.5rem 0.75rem;
        }
        
        .prompt-title {
            font-size: 1.125rem;
        }
        
        .prompt-subtitle {
            font-size: 0.8125rem;
        }
        
        .prompt-button {
            padding: 0.875rem 1rem;
            font-size: 0.8125rem;
        }
    }
    
    /* Large desktops (min-width: 1400px) */
    @media screen and (min-width: 1400px) {
        .main .block-container {
            max-width: 1400px;
            margin: 0 auto;
        }
        
        [data-testid="stChatInput"] > div {
            max-width: 1400px;
        }
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
    html = """
    <div class="sales-cta-container" style="
        margin: 1.5rem 0; 
        padding: 1.25rem; 
        background: linear-gradient(135deg, #FAFAFA 0%, #F8F9FA 100%); 
        border: 2px solid #291f3b; 
        border-radius: 16px; 
        text-align: center; 
        box-shadow: 0 4px 16px rgba(41, 31, 59, 0.12);
    ">
        <p class="cta-message" style="
            margin: 0 0 1rem 0; 
            font-size: 1rem; 
            color: #291f3b; 
            font-weight: 600; 
            line-height: 1.5;
        ">
            💡 Ready to build smarter and scale faster?
        </p>
        <a href="https://www.shurutech.com/contact-us" target="_blank" style="text-decoration: none;">
            <button class="cta-button" style="
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
                width: auto;
                min-width: 200px;
            "
            onmouseover="this.style.transform='translateY(-3px)'; this.style.boxShadow='0 8px 24px rgba(41, 31, 59, 0.4)';"
            onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 6px 20px rgba(41, 31, 59, 0.3)';">
                Contact Us
            </button>
        </a>
        <p class="cta-subtitle" style="
            margin: 1rem 0 0 0; 
            font-size: 0.875rem; 
            color: #64748B; 
            font-weight: 500;
        ">
            Let's discuss how we can help transform your business
        </p>
    </div>
    
    <style>
    /* Mobile CTA responsiveness */
    @media screen and (max-width: 768px) {
        .sales-cta-container {
            padding: 1rem !important;
            margin: 1rem 0 !important;
            border-radius: 12px !important;
        }
        
        .cta-message {
            font-size: 0.9375rem !important;
        }
        
        .cta-button {
            padding: 0.75rem 1.75rem !important;
            font-size: 0.9375rem !important;
            width: 100% !important;
            max-width: 300px;
        }
        
        .cta-subtitle {
            font-size: 0.8125rem !important;
        }
    }
    
    @media screen and (max-width: 480px) {
        .cta-button {
            padding: 0.75rem 1.5rem !important;
            font-size: 0.875rem !important;
        }
    }
    </style>
    """
    st.markdown(html, unsafe_allow_html=True)


# Removed display_chat_prompts() - replaced with display_dark_prompts()


def display_dark_header():
    """Display simplified header with Shuru logo only"""
    html = """
    <div class="dashboard-header">
        <img src="https://www.shurutech.com/images/logo-black-text.png" 
             alt="Shuru Tech" 
             class="shuru-logo" />
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def display_dark_greeting():
    """Display centered greeting in dark theme"""
    html = """
    <div class="main-content">
        <h1 class="greeting-text">How can I help you today?</h1>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def display_dark_prompts():
    """Display prompt buttons below the greeting"""
    # Create prompt buttons using Streamlit
    st.markdown("""
    <div style="margin-top: 2rem; display: flex; flex-direction: column; gap: 0.75rem; max-width: 600px; margin-left: auto; margin-right: auto;">
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🚀 What services does Shuru Tech offer?", key="dark_prompt1", use_container_width=True):
            st.session_state.selected_prompt = "What services does Shuru Tech offer?"
            st.rerun()
    
    with col2:
        if st.button("🤖 How can AI transform my business operations?", key="dark_prompt2", use_container_width=True):
            st.session_state.selected_prompt = "How can AI transform my business operations?"
            st.rerun()
    
    # Third button centered
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("💬 Tell me about your RAG chatbot capabilities", key="dark_prompt3", use_container_width=True):
            st.session_state.selected_prompt = "Tell me about your RAG chatbot capabilities"
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)

