"""
Shuru Tech RAG Chatbot - Streamlit Application
A conversational AI assistant powered by RAG for Shuru Tech
"""

import streamlit as st
import os
import json
import logging
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_anthropic import ChatAnthropic
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.schema import Document
from langchain.prompts import PromptTemplate

# Suppress tokenizer parallelism warnings
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Shuru Tech | AI Solutions Dashboard",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)


class ShuruTechRAGBot:
    def __init__(self):
        self.anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
        self.knowledge_base_path = 'knowledge_base.json'
        self.vectorstore = None
        self.chain = None
        # Debug tracking
        self.num_documents = 0
        self.num_case_studies = 0
        self.last_query = None
        self.last_retrieval_count = 0
        self.last_retrieved_clients = []
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
        print(f"📚 Loading {self.num_case_studies} case studies from knowledge_base.json")

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
                    "technologies": ', '.join(case_study.get('technologies', []))
                }
            )
            documents.append(doc)
            case_study_count += 1

        logger.info(f"✓ Created {case_study_count} case study documents for vector store")
        print(f"✓ Created {case_study_count} case study documents for vector store")

        # Process services
        for service in data.get('services', []):
            doc = Document(
                page_content=f"Service: {service.get('name', '')}\nDescription: {service.get('description', '')}",
                metadata={"source": "service", "type": "service"}
            )
            documents.append(doc)

        self.num_documents = len(documents)
        logger.info(f"✓ Total documents created: {self.num_documents}")
        print(f"✓ Total documents created: {self.num_documents}")
        return documents

    def create_vectorstore(self, documents):
        """Create FAISS vector store from documents"""
        if not documents:
            error_msg = "❌ No documents provided to create vector store"
            logger.error(error_msg)
            st.error(error_msg)
            return None

        try:
            logger.info(f"📊 Processing {len(documents)} documents for vector store...")
            print(f"📊 Processing {len(documents)} documents for vector store...")

            # Split documents into chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len
            )
            splits = text_splitter.split_documents(documents)
            logger.info(f"✓ Split into {len(splits)} chunks")
            print(f"✓ Split into {len(splits)} chunks")

            # Create embeddings (using free local HuggingFace embeddings)
            logger.info("🔧 Initializing embeddings model...")
            print("🔧 Initializing embeddings model...")
            embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2"
            )

            # Create FAISS vector store
            logger.info("🔨 Creating FAISS vector store...")
            print("🔨 Creating FAISS vector store...")
            vectorstore = FAISS.from_documents(
                documents=splits,
                embedding=embeddings
            )

            logger.info(f"✓ Vector store created with {len(splits)} documents")
            print(f"✓ Vector store created with {len(splits)} documents")
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
            max_tokens=int(os.getenv('MAX_TOKENS', 1024))
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

Provide a helpful, professional response that:
1. Acknowledges their specific problem with empathy (1-2 sentences)
2. References the most relevant case study from our portfolio
3. Explains the approach we took and technologies used
4. Highlights measurable results with specific metrics
5. Suggests how we can apply similar solutions to their situation
6. Ends with an engaging question or next step

Guidelines:
- Be conversational yet professional
- Use **bold** for key metrics and results (e.g., **50% increase**, **$100K savings**)
- Use **bold** for company names and case study names
- Structure with clear paragraphs (not bullet points in main response)
- Always cite specific case study names
- Focus on business value, not just technical details
- Be confident and solution-focused
- Add line breaks between sections for readability"""
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
        print("✓ Conversational chain initialized successfully")

        return chain

    def get_response(self, question):
        """Get response from the chatbot"""
        logger.info(f"Processing query: {question[:100]}...")  # Log first 100 chars
        self.last_query = question

        if not self.chain:
            self.chain = self.initialize_chain()

        if not self.chain:
            error_msg = "Sorry, I couldn't initialize the chatbot. Please check your configuration."
            logger.error(error_msg)
            return error_msg, []

        try:
            result = self.chain.invoke({"question": question})
            sources = result.get('source_documents', [])

            # Track retrieval metrics
            self.last_retrieval_count = len(sources)
            self.last_retrieved_clients = []

            for source in sources:
                if source.metadata.get('type') == 'case_study':
                    client_name = source.metadata.get('client_name', 'Unknown')
                    if client_name not in self.last_retrieved_clients:
                        self.last_retrieved_clients.append(client_name)

            logger.info(f"✓ Retrieved {self.last_retrieval_count} documents, {len(self.last_retrieved_clients)} unique case studies")

            return result['answer'], sources
        except Exception as e:
            error_msg = f"❌ Error processing query: {str(e)}"
            logger.error(error_msg)
            return f"Sorry, an error occurred: {str(e)}", []


def main():
    """Main application function"""
    from ui_components import (
        inject_dashboard_styles,
        display_case_study_item,
        display_panel_header,
        display_dashboard_header,
        display_sales_cta
    )
    
    # Inject modern dashboard styles
    inject_dashboard_styles()
    
    # Display dashboard header
    display_dashboard_header(
        "🤖 ShuruMan",
        "Have business questions? We already have answers"
    )

    # Initialize bot in session state
    if 'bot' not in st.session_state:
        with st.spinner("Initializing chatbot..."):
            st.session_state.bot = ShuruTechRAGBot()

    # Initialize chat history
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # ==========================================
    # CHAT AREA (Full Width)
    # ==========================================
    # Display all messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # Show sources if assistant message
            if message["role"] == "assistant" and message.get("sources"):
                st.markdown('<hr style="margin: 2rem 0; border-top: 2px solid #E5E7EB;">', unsafe_allow_html=True)
                st.markdown("### 📚 Related Case Studies")
                
                # Display case studies (existing code)
                sources = message["sources"]
                case_studies = []
                
                for source in sources:
                    if source.metadata.get('type') == 'case_study':
                        client_name = source.metadata.get('client_name', 'Unknown')
                        if not any(cs.metadata.get('client_name') == client_name for cs in case_studies):
                            case_studies.append(source)
                
                if case_studies:
                    for source in case_studies:
                        client_name = source.metadata.get('client_name', 'Unknown')
                        industry = source.metadata.get('industry', 'N/A')
                        
                        with st.expander(f"🔹 **{client_name}** - {industry}"):
                            content = source.page_content
                            
                            # Parse sections (existing code)
                            sections = {}
                            current_section = None
                            current_content = []
                            
                            for line in content.split('\n'):
                                line = line.strip()
                                if line.endswith(':') and line[:-1] in ['Problem', 'Solution', 'Results', 'Technologies Used', 'Duration']:
                                    if current_section:
                                        sections[current_section] = '\n'.join(current_content).strip()
                                    current_section = line[:-1]
                                    current_content = []
                                elif line and current_section:
                                    current_content.append(line)
                            
                            if current_section:
                                sections[current_section] = '\n'.join(current_content).strip()
                            
                            # Display sections
                            if 'Problem' in sections:
                                st.markdown(f"**Problem:**")
                                st.markdown(sections['Problem'])
                                st.markdown("")
                            
                            if 'Solution' in sections:
                                st.markdown(f"**Solution:**")
                                st.markdown(sections['Solution'])
                                st.markdown("")
                            
                            if 'Technologies Used' in sections:
                                st.markdown(f"**Technologies Used:**")
                                st.markdown(sections['Technologies Used'])
                                st.markdown("")
                            
                            if 'Results' in sections:
                                st.markdown(f"**Results:**")
                                st.markdown(sections['Results'])
                                st.markdown("")
                            
                            if 'Duration' in sections:
                                st.markdown(f"**Duration:** {sections['Duration']}")
                
                # Add CTA after sources
                display_sales_cta()
    
    # Chat input at bottom (full width, outside any columns)
    prompt = st.chat_input("Type your business question...")
    
    # ==========================================
    # MESSAGE PROCESSING (Simplified)
    # ==========================================
    if prompt:
        # Add user message (no timestamps)
        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })

        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get bot response
        with st.chat_message("assistant"):
            with st.spinner("✨ Finding relevant solutions..."):
                response, sources = st.session_state.bot.get_response(prompt)
                st.markdown(response)

                # Display sources
                if sources:
                    st.markdown('<hr style="margin: 2rem 0; border-top: 2px solid #E5E7EB;">', unsafe_allow_html=True)
                    st.markdown("### 📚 Related Case Studies")

                    # Extract case studies
                    case_studies = []
                    for source in sources:
                        if source.metadata.get('type') == 'case_study':
                            client_name = source.metadata.get('client_name', 'Unknown')
                            if not any(cs.metadata.get('client_name') == client_name for cs in case_studies):
                                case_studies.append(source)

                    # Display case studies in expandable sections
                    if case_studies:
                        for source in case_studies:
                            client_name = source.metadata.get('client_name', 'Unknown')
                            industry = source.metadata.get('industry', 'N/A')

                            with st.expander(f"🔹 **{client_name}** - {industry}"):
                                content = source.page_content

                                # Parse content
                                sections = {}
                                current_section = None
                                current_content = []

                                for line in content.split('\n'):
                                    line = line.strip()
                                    if line.endswith(':') and line[:-1] in ['Problem', 'Solution', 'Results', 'Technologies Used', 'Duration']:
                                        if current_section:
                                            sections[current_section] = '\n'.join(current_content).strip()
                                        current_section = line[:-1]
                                        current_content = []
                                    elif line and current_section:
                                        current_content.append(line)

                                if current_section:
                                    sections[current_section] = '\n'.join(current_content).strip()

                                # Display sections
                                if 'Problem' in sections:
                                    st.markdown(f"**Problem:**")
                                    st.markdown(sections['Problem'])
                                    st.markdown("")

                                if 'Solution' in sections:
                                    st.markdown(f"**Solution:**")
                                    st.markdown(sections['Solution'])
                                    st.markdown("")

                                if 'Technologies Used' in sections:
                                    st.markdown(f"**Technologies Used:**")
                                    st.markdown(sections['Technologies Used'])
                                    st.markdown("")

                                if 'Results' in sections:
                                    st.markdown(f"**Results:**")
                                    st.markdown(sections['Results'])
                                    st.markdown("")

                                if 'Duration' in sections:
                                    st.markdown(f"**Duration:** {sections['Duration']}")

        # Add assistant response (store sources for later display)
        st.session_state.messages.append({
            "role": "assistant",
            "content": response,
            "sources": sources
        })


if __name__ == "__main__":
    main()
