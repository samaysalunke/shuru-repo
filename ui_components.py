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
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        animation: fadeIn 0.3s ease-in;
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
        background: #FFFFFF;
        border-bottom: 2px solid #F1F5F9;
        padding: 1.5rem 2rem;
        margin: -2rem -2rem 2rem -2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 2px 8px rgba(41, 31, 59, 0.08);
    }
    
    .dashboard-logo {
        height: 40px;
        margin-right: 1rem;
        vertical-align: middle;
    }
    
    .dashboard-title {
        font-size: 1.75rem;
        font-weight: 700;
        color: #291f3b;
        margin: 0;
        display: inline-flex;
        align-items: center;
        gap: 1rem;
    }
    
    .dashboard-subtitle {
        font-size: 0.95rem;
        color: #64748B;
        margin: 0.5rem 0 0 0;
        font-weight: 400;
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
        <div>
            <h1 class="dashboard-title">
                <img src="https://www.shurutech.com/images/logo-black-text.png" 
                     alt="Shuru Tech" 
                     class="dashboard-logo" />
                {title}
            </h1>
            {f'<p class="dashboard-subtitle">{subtitle}</p>' if subtitle else ''}
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def display_sales_cta():
    """Display a prominent CTA button for booking sales calls - Shuru Tech Branded"""
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
                📞 Book a Sales Call
            </button>
        </a>
        <p style="margin: 1rem 0 0 0; font-size: 0.875rem; color: #64748B; font-weight: 500;">
            Let's discuss how we can help transform your business
        </p>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

