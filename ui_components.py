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
    
    /* Global styles */
    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        background: #F9FAFB;
    }
    
    /* Remove default Streamlit padding */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
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
    
    /* Chat area improvements */
    [data-testid="stChatMessage"] {
        background: white;
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }
    
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
        border-left: 3px solid #3B82F6;
    }
    
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
        border-left: 3px solid #10B981;
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
    
    /* Header styles */
    .dashboard-header {
        background: white;
        border-bottom: 1px solid #E5E7EB;
        padding: 1.5rem 2rem;
        margin: -2rem -2rem 2rem -2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .dashboard-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1F2937;
        margin: 0;
    }
    
    .dashboard-subtitle {
        font-size: 0.875rem;
        color: #6B7280;
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
    
    /* Chat input - sticky at bottom */
    [data-testid="stChatInput"] {
        position: sticky;
        bottom: 0;
        background: white;
        padding: 1rem 0;
        margin-top: 1rem;
        z-index: 100;
        border-top: 1px solid #E5E7EB;
    }
    
    [data-testid="stChatInput"] input,
    [data-testid="stChatInput"] textarea {
        border: 2px solid #E5E7EB !important;
        border-radius: 12px !important;
        padding: 0.875rem 1rem !important;
        font-size: 0.875rem !important;
        transition: all 0.2s ease !important;
    }
    
    [data-testid="stChatInput"] input:focus,
    [data-testid="stChatInput"] textarea:focus {
        border-color: #3B82F6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
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
    """Display dashboard header"""
    html = f"""
    <div class="dashboard-header">
        <div>
            <h1 class="dashboard-title">🚀 {title}</h1>
            {f'<p class="dashboard-subtitle">{subtitle}</p>' if subtitle else ''}
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

