"""
Shuru Tech RAG Chatbot - 21st.dev Modern Interface
Enhanced with modern UI components and Claude-powered RAG system
"""

import streamlit as st
import json
import os
import logging
from typing import List, Dict, Any
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_anthropic import ChatAnthropic
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.schema import Document
from langchain.prompts import PromptTemplate
from ui_components_21st import (
    inject_21st_styles,
    display_21st_header,
    display_21st_empty_state,
    display_21st_chat_messages,
    display_21st_chat_input,
    display_21st_sales_cta,
    display_fixed_contact_button
)

# Suppress tokenizer parallelism warnings
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configure Streamlit page
st.set_page_config(
    page_title="Shuru Tech AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

class ShuruTechRAGBot:
    """Claude-powered RAG Bot with 21st.dev modern interface"""
    
    def __init__(self):
        self.anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
        self.knowledge_base_path = 'knowledge_base.json'
        self.vectorstore = None
        self.chain = None
        self.num_documents = 0
        self.num_case_studies = 0
        logger.info("ShuruTechRAGBot initialized")
    
    def load_knowledge_base(self):
        """Load knowledge base from JSON file"""
        logger.info(f"Loading knowledge base from {self.knowledge_base_path}")

        # Validation checks
        if not os.path.exists(self.knowledge_base_path):
            error_msg = "❌ Knowledge base not found. Please run scrape_website.py first."
            logger.error(error_msg)
            st.error(error_msg)
            return []

        try:
            with open(self.knowledge_base_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            error_msg = f"❌ Invalid JSON in knowledge base: {str(e)}"
            logger.error(error_msg)
            st.error(error_msg)
            return []

        # Validate case_studies exists and is not empty
        if 'case_studies' not in data:
            error_msg = "❌ No 'case_studies' key found in knowledge_base.json"
            logger.error(error_msg)
            st.error(error_msg)
            return []

        if not data.get('case_studies'):
            error_msg = "❌ case_studies array is empty in knowledge_base.json"
            logger.error(error_msg)
            st.error(error_msg)
            return []

        self.num_case_studies = len(data.get('case_studies', []))
        logger.info(f"📚 Loaded {self.num_case_studies} case studies from knowledge_base.json")

        documents = []

        # Process company info
        if data.get('company_info'):
            info = data['company_info']
            doc = Document(
                page_content=f"{info.get('title', '')}\n{info.get('description', '')}",
                metadata={"source": "company_info", "type": "company"}
            )
            documents.append(doc)

        # Process pages
        for page in data.get('pages', []):
            doc = Document(
                page_content=f"Title: {page.get('title', '')}\nContent: {page.get('content', '')}",
                metadata={"source": page.get('url', ''), "type": "page"}
            )
            documents.append(doc)

        # Process case studies with RICH CONTENT
        case_study_count = 0
        for case_study in data.get('case_studies', []):
            # Create rich page_content combining all important fields
            page_content = f"""Case Study: {case_study.get('client_name', 'Unknown Client')}
Industry: {case_study.get('industry', 'N/A')}

Problem:
{case_study.get('problem', 'N/A')}

Solution:
{case_study.get('solution', 'N/A')}

Technologies Used: {', '.join(case_study.get('technologies', []))}

Results:
{case_study.get('results', 'N/A')}

Duration: {case_study.get('duration', 'N/A')}"""

            doc = Document(
                page_content=page_content,
                metadata={
                    "source": "case_study",
                    "type": "case_study",
                    "client_name": case_study.get('client_name', 'Unknown'),
                    "industry": case_study.get('industry', 'N/A'),
                    "technologies": ', '.join(case_study.get('technologies', [])),
                    "url": case_study.get('url', ''),
                    "results": case_study.get('results', 'N/A')
                }
            )
            documents.append(doc)
            case_study_count += 1

        self.num_documents = len(documents)
        logger.info(f"📄 Created {self.num_documents} documents ({case_study_count} case studies)")

        return documents

    def create_vectorstore(self, documents):
        """Create FAISS vector store from documents"""
        logger.info("Creating vector store...")
        
        try:
            # Initialize embeddings
            embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                model_kwargs={'device': 'cpu'}
            )
            
            # Create vector store
            vectorstore = FAISS.from_documents(documents, embeddings)
            
            logger.info("✓ Vector store created successfully")
            return vectorstore
        except Exception as e:
            error_msg = f"❌ Failed to create vector store: {str(e)}"
            logger.error(error_msg)
            st.error(error_msg)
            return None

    def initialize_chain(self):
        """Initialize the conversational retrieval chain"""
        logger.info("Initializing conversational chain...")

        if not self.anthropic_api_key:
            error_msg = "❌ Anthropic API key not found. Please set it in .env file."
            logger.error(error_msg)
            st.error(error_msg)
            return None

        # Load documents
        documents = self.load_knowledge_base()
        if not documents:
            return None

        # Create vector store
        self.vectorstore = self.create_vectorstore(documents)
        if not self.vectorstore:
            return None

        # Create LLM (using Claude)
        llm = ChatAnthropic(
            model="claude-3-5-sonnet-20241022",
            temperature=float(os.getenv('TEMPERATURE', 0.7)),
            anthropic_api_key=self.anthropic_api_key,
            max_tokens=int(os.getenv('MAX_TOKENS', 1500))  # Increased for structured responses
        )

        # Create memory
        memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="answer"
        )

        # Create custom prompt template for consultative responses
        qa_prompt = PromptTemplate(
            input_variables=["context", "question"],
            template="""You are a solutions consultant for Shuru Tech, a technology consulting company. A potential client has described their business challenge.

Based on these relevant case studies from our portfolio:
{context}

Client's challenge: {question}

Provide a helpful, professional response using this EXACT structure:

[Opening paragraph: Lead with the most relevant case study name in bold. Show empathy for their challenge. 1-2 sentences max.]

**The Challenge:**
• [Bullet point describing problem 1]
• [Bullet point describing problem 2]
• [Bullet point describing problem 3 if relevant]

**Our Solution:**
• [Solution component 1]
• [Solution component 2]
• [Solution component 3]
• [Solution component 4 if relevant]

**Results Achieved:**
• ✓ [Metric 1 with percentage/number]
• ✓ [Metric 2 with percentage/number]
• ✓ [Metric 3 with percentage/number]

**How We Can Help You:**
• [Specific action item 1 for their situation]
• [Specific action item 2 for their situation]
• [Specific action item 3 for their situation]

[Closing: One sentence inviting them to learn more. Keep it soft and consultative, not pushy.]

CRITICAL FORMATTING RULES:
- Use **bold** for section headers exactly as shown
- Use bullet points (•) for all lists
- Use ✓ checkmark for results
- Keep bullets concise (max 15 words each)
- Add blank line between each section
- Do not use numbered lists
- Do not ask for specific meeting times
- Do not make up metrics not in the context
- Cite exact client names from case studies in bold
- Keep opening and closing to 1-2 sentences each"""
        )

        # Create chain with k=5 for top 5 results and custom prompt
        chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=self.vectorstore.as_retriever(search_kwargs={"k": 5}),
            memory=memory,
            return_source_documents=True,
            verbose=False,
            combine_docs_chain_kwargs={"prompt": qa_prompt}
        )

        logger.info("✓ Conversational chain initialized successfully")
        return chain

    def get_response(self, question):
        """Get response from the chatbot"""
        logger.info(f"Processing query: {question[:100]}...")

        if not self.chain:
            self.chain = self.initialize_chain()

        if not self.chain:
            error_msg = "Sorry, I couldn't initialize the chatbot. Please check your configuration."
            logger.error(error_msg)
            return error_msg, []

        try:
            result = self.chain.invoke({"question": question})
            sources = result.get('source_documents', [])
            answer = result['answer']
            
            # Add clickable URLs to case studies mentioned in response
            answer = self.add_case_study_links(answer, sources)
            
            logger.info(f"✓ Generated response with {len(sources)} sources")
            return answer, sources
        except Exception as e:
            error_msg = f"❌ Error processing query: {str(e)}"
            logger.error(error_msg)
            return f"Sorry, an error occurred: {str(e)}", []

    def add_case_study_links(self, answer: str, sources: List) -> str:
        """Add clickable URLs for case studies mentioned in response"""
        # Extract case studies from sources
        case_study_links = {}
        for source in sources:
            if source.metadata.get('type') == 'case_study':
                client_name = source.metadata.get('client_name', '')
                url = source.metadata.get('url', '')
                if client_name and url and url != '#':
                    case_study_links[client_name] = url
        
        # Add URLs section at the end if case studies were referenced
        if case_study_links:
            answer += "\n\n---\n\n**📚 View Full Case Studies:**\n\n"
            for client, url in case_study_links.items():
                answer += f"• [{client}]({url})\n"
        
        return answer

    def generate_response(self, query: str) -> str:
        """Generate AI-powered response using Claude and RAG"""
        answer, sources = self.get_response(query)
        return answer
    

def main():
    """Main application function with 21st.dev modern interface"""
    
    # Inject modern styles
    inject_21st_styles()
    
    # Display header
    display_21st_header()
    
    # Initialize bot with loading feedback
    if 'bot' not in st.session_state:
        with st.spinner("🔄 Initializing AI-powered RAG system..."):
            try:
                st.session_state.bot = ShuruTechRAGBot()
                # Eagerly initialize the chain
                st.session_state.bot.chain = st.session_state.bot.initialize_chain()
                if not st.session_state.bot.chain:
                    st.error("Failed to initialize RAG system. Please check ANTHROPIC_API_KEY.")
                else:
                    st.success(f"✓ RAG system ready with {st.session_state.bot.num_case_studies} case studies")
            except Exception as e:
                st.error(f"Error initializing bot: {str(e)}")
                return
    
    # Initialize chat history
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # Show empty state or chat interface
    if not st.session_state.messages:
        display_21st_empty_state()
    else:
        display_21st_chat_messages(st.session_state.messages)
    
    # Handle selected prompt
    if "selected_prompt" in st.session_state:
        prompt = st.session_state.selected_prompt
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Generate response
        with st.spinner("Thinking..."):
            response = st.session_state.bot.generate_response(prompt)
            st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Clear the selected prompt
        del st.session_state.selected_prompt
        st.rerun()
    
    # Always show chat input (both empty state and chat state)
    display_21st_chat_input()
    prompt = st.chat_input("Type your message here...")
    
    if prompt:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Generate and add assistant response
        with st.spinner("Thinking..."):
            response = st.session_state.bot.generate_response(prompt)
            st.session_state.messages.append({"role": "assistant", "content": response})
        
        st.rerun()
    
    # Add fixed contact button (always visible)
    display_fixed_contact_button()

if __name__ == "__main__":
    main()
