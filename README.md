# 🚀 Shuru Tech AI Chatbot - RAG-Powered Solutions Assistant

An intelligent **Retrieval-Augmented Generation (RAG)** chatbot that helps potential clients discover relevant case studies and solutions from Shuru Tech's portfolio. Built with Claude 3.5 Sonnet, LangChain, FAISS vector database, and Streamlit.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.31+-red.svg)](https://streamlit.io/)
[![LangChain](https://img.shields.io/badge/langchain-0.2+-green.svg)](https://www.langchain.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

---

## 📖 **Table of Contents**

- [What is This?](#-what-is-this)
- [Key Features](#-key-features)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [How It Works](#-how-it-works)
- [Installation](#-installation)
- [Usage](#-usage)
- [Configuration](#-configuration)
- [Knowledge Base](#-knowledge-base)
- [Deployment](#-deployment)
- [Troubleshooting](#-troubleshooting)
- [Performance](#-performance)
- [Contributing](#-contributing)

---

## 🎯 **What is This?**

**ShuruMan** is an AI-powered chatbot that acts as a **virtual solutions consultant** for Shuru Tech. It uses **Retrieval-Augmented Generation (RAG)** to:

1. **Understand** client business challenges
2. **Retrieve** relevant case studies from Shuru Tech's portfolio
3. **Generate** consultative responses with specific examples and metrics
4. **Recommend** tailored solutions based on proven success stories

### **Why RAG?**

Instead of just relying on the LLM's general knowledge, RAG retrieves **specific, factual information** from Shuru Tech's case studies before generating responses. This ensures:

- ✅ **Accurate information** - No hallucinations, only real case studies
- ✅ **Relevant recommendations** - Matches client needs with proven solutions
- ✅ **Transparent sources** - Shows which case studies informed the response
- ✅ **Up-to-date content** - Easy to update knowledge base without retraining

---

## ✨ **Key Features**

### **🤖 Intelligent Conversations**
- **Claude 3.5 Sonnet** provides human-like, consultative responses
- **Conversational memory** maintains context throughout the chat
- **Professional tone** balances technical expertise with accessibility

### **📚 RAG Architecture**
- **FAISS vector database** for fast semantic search
- **50+ case studies** covering diverse industries and technologies
- **Top-5 retrieval** ensures comprehensive yet focused responses
- **Source attribution** shows which case studies informed the answer

### **💬 Modern UI/UX**
- **Shuru Tech branding** with official logo and purple color scheme (#291f3b)
- **Clickable prompts** - 3 starter questions when chat is empty
- **Contact Us CTA** - Prominent button linking to Shuru Tech's contact page
- **ChatGPT-style interface** - Input at bottom, messages above
- **Responsive design** - Works on desktop, tablet, and mobile

### **⚡ Performance**
- **Free embeddings** - Uses local HuggingFace models (no API costs)
- **Fast search** - FAISS vector similarity in milliseconds
- **Efficient chunking** - 1000-character chunks with 200 overlap
- **Cached vectors** - First load slower, subsequent queries instant

---

## 🏗️ **Architecture**

```
┌─────────────────────────────────────────────────────────────────────┐
│                     SHURU TECH RAG CHATBOT                          │
└─────────────────────────────────────────────────────────────────────┘

┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│  DATA INGESTION  │───▶│  VECTOR STORE    │───▶│   RAG CHAIN      │
└──────────────────┘    └──────────────────┘    └──────────────────┘
        │                        │                        │
        │                        │                        │
   ┌────▼────┐          ┌────────▼────────┐     ┌────────▼────────┐
   │ Web     │          │ Embeddings      │     │ Claude 3.5      │
   │ Scraper │          │ (HuggingFace)   │     │ Sonnet          │
   │         │          │                 │     │                 │
   │ • Case  │          │ • Text Chunking │     │ • Retrieval     │
   │   Studies│         │ • Vector Index  │     │ • Generation    │
   │ • Services│        │ • FAISS Store   │     │ • Memory        │
   └─────────┘          └─────────────────┘     └─────────────────┘
        │                        │                        │
        ▼                        ▼                        ▼
knowledge_base.json      Vector Database           AI Response
```

### **Data Flow:**

1. **Ingestion**: Web scraper extracts case studies → `knowledge_base.json`
2. **Processing**: Documents chunked → Embeddings generated → FAISS index created
3. **Query**: User question → Semantic search → Top 5 relevant chunks retrieved
4. **Generation**: Context + Question → Claude 3.5 → Consultative response
5. **Response**: Answer + Source documents + Contact CTA

---

## 🛠️ **Tech Stack**

### **AI & ML**
| Technology | Purpose | Version |
|-----------|---------|---------|
| **Claude 3.5 Sonnet** | Large Language Model for response generation | Latest |
| **LangChain** | RAG orchestration framework | 0.2+ |
| **HuggingFace Transformers** | Embeddings model | 2.5+ |
| **sentence-transformers** | Semantic text embeddings | all-MiniLM-L6-v2 |
| **FAISS** | Vector similarity search | 1.7.4+ |

### **Frontend**
| Technology | Purpose | Version |
|-----------|---------|---------|
| **Streamlit** | Web interface framework | 1.31+ |
| **Custom CSS** | Shuru Tech branding | N/A |
| **HTML/JavaScript** | Interactive elements | N/A |

### **Backend**
| Technology | Purpose | Version |
|-----------|---------|---------|
| **Python** | Core language | 3.8+ |
| **BeautifulSoup4** | Web scraping | 4.12+ |
| **Requests** | HTTP requests | 2.31+ |
| **python-dotenv** | Environment management | 1.0+ |

### **Development & Deployment**
| Technology | Purpose |
|-----------|---------|
| **Git/GitHub** | Version control |
| **Streamlit Cloud** | Hosting platform |
| **Virtual Environment** | Dependency isolation |

---

## 🔍 **How It Works**

### **Step 1: Data Collection (Web Scraping)**

**File: `scrape_website.py`**

```python
class AdvancedShuruTechScraper:
    # Extracts case studies from Shuru Tech website
    # - Multi-strategy content extraction
    # - NLP pattern matching
    # - Technology & industry detection
```

**Output**: `knowledge_base.json` with structured case studies:

```json
{
  "case_studies": [
    {
      "client_name": "SwiftCart E-commerce Platform",
      "industry": "E-commerce",
      "problem": "72% cart abandonment rate...",
      "solution": "Implemented one-click checkout...",
      "technologies": ["React", "Redux", "Node.js", "MongoDB"],
      "results": "Reduced cart abandonment from 72% to 28%...",
      "duration": "3 months"
    }
  ]
}
```

### **Step 2: Vector Database Creation**

**File: `app.py` - `create_vectorstore()`**

```python
# 1. Text Chunking
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,      # Characters per chunk
    chunk_overlap=200     # Context preservation
)

# 2. Embeddings Generation (FREE - Local Model)
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# 3. FAISS Vector Store
vectorstore = FAISS.from_documents(
    documents=splits,
    embedding=embeddings
)
```

**Why this approach?**
- **1000 character chunks**: Optimal size for case studies
- **200 character overlap**: Preserves context between chunks
- **Free embeddings**: No API costs for vector generation
- **FAISS**: Fast, efficient similarity search

### **Step 3: RAG Chain Setup**

**File: `app.py` - `initialize_chain()`**

```python
# LLM Configuration
llm = ChatAnthropic(
    model="claude-3-5-sonnet-20241022",
    temperature=0.7,
    max_tokens=1024
)

# Conversational Memory
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

# RAG Chain with Custom Prompt
chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=vectorstore.as_retriever(search_kwargs={"k": 5}),
    memory=memory,
    return_source_documents=True
)
```

### **Step 4: Query Processing**

```
User: "How can I reduce cart abandonment in my e-commerce store?"
                            ↓
┌─────────────────────────────────────────────────────────┐
│ 1. SEMANTIC SEARCH (FAISS)                             │
│    - Converts question to vector embedding             │
│    - Searches vector database for similar chunks       │
│    - Returns top 5 most relevant case studies          │
└─────────────────────────────────────────────────────────┘
                            ↓
        [Found: SwiftCart case study - 72% → 28% cart abandonment]
                            ↓
┌─────────────────────────────────────────────────────────┐
│ 2. CONTEXT INJECTION                                    │
│    - Packages retrieved case studies                    │
│    - Combines with user question                        │
│    - Sends to Claude 3.5 Sonnet                        │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│ 3. RESPONSE GENERATION (Claude)                         │
│    - Analyzes case study context                        │
│    - Understands user's specific challenge              │
│    - Generates consultative response with:              │
│      ✓ Empathy for the problem                         │
│      ✓ Relevant case study reference                   │
│      ✓ Technical solution details                       │
│      ✓ Measurable business results                      │
│      ✓ Recommendation for their situation               │
└─────────────────────────────────────────────────────────┘
                            ↓
        "Based on our work with SwiftCart, where we reduced 
         cart abandonment from 72% to 28% using one-click 
         checkout and optimized payment flows..."
                            ↓
                    [Contact Us CTA]
```

---

## 📦 **Installation**

### **Prerequisites**

- **Python 3.8+** ([Download](https://www.python.org/downloads/))
- **Anthropic API Key** ([Get one](https://console.anthropic.com/))
- **Git** ([Download](https://git-scm.com/downloads))

### **Setup Steps**

#### **1. Clone the Repository**

```bash
git clone https://github.com/samaysalunke/shuru-repo.git
cd shuru-chatbot
```

#### **2. Create Virtual Environment**

```bash
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

#### **3. Install Dependencies**

```bash
pip install -r requirements.txt
```

**Dependencies installed:**
- `anthropic` - Claude API client
- `langchain` - RAG framework
- `langchain-anthropic` - Anthropic integration
- `faiss-cpu` - Vector similarity search
- `streamlit` - Web UI framework
- `sentence-transformers` - Embeddings model
- `beautifulsoup4` - Web scraping
- `python-dotenv` - Environment variables

#### **4. Configure Environment Variables**

Create a `.env` file in the project root:

```env
# Required
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Optional (with defaults)
TEMPERATURE=0.7
MAX_TOKENS=1024
APP_TITLE=ShuruMan
APP_ICON=🤖
```

**Get your Anthropic API key:**
1. Go to [console.anthropic.com](https://console.anthropic.com/)
2. Sign up or log in
3. Navigate to API Keys
4. Create a new key and copy it

#### **5. Prepare Knowledge Base**

**Option A: Use existing knowledge base**
- The repo includes `knowledge_base.json` with 50+ case studies
- Ready to use out of the box

**Option B: Scrape fresh data**
```bash
python scrape_website.py
```

**Option C: Create custom knowledge base**
- Edit `knowledge_base.json` manually
- Follow the structure in [Knowledge Base](#-knowledge-base) section

---

## 🚀 **Usage**

### **Starting the Application**

```bash
streamlit run app.py
```

The chatbot will open in your browser at **`http://localhost:8501`**

### **First-Time Setup**

When you first run the app:
1. **Embeddings download** (~30 seconds) - Downloads HuggingFace model
2. **Vector store creation** (~10 seconds) - Processes case studies
3. **Ready to chat!** - Subsequent loads are instant

### **Using the Chatbot**

#### **Option 1: Clickable Prompts (Recommended)**

When the chat is empty, you'll see 3 clickable prompts:

- 🚀 **"What services does Shuru Tech offer?"**
- 🤖 **"How can AI transform my business operations?"**
- 💬 **"Tell me about your RAG chatbot capabilities"**

**Click any prompt** to start a conversation instantly.

#### **Option 2: Type Your Own Question**

Click the input box at the bottom and ask anything:

**Example questions:**
- "I need help reducing cart abandonment on my e-commerce site"
- "How can I improve my mobile app's performance?"
- "What's your experience with cloud migration projects?"
- "Tell me about AI solutions for fintech companies"
- "I need to build a real-time data pipeline"

### **Understanding Responses**

Each AI response includes:

1. **Empathetic acknowledgment** of your challenge
2. **Relevant case study** from Shuru Tech's portfolio
3. **Technical approach** with specific technologies
4. **Measurable results** with real metrics
5. **Tailored recommendation** for your situation
6. **Contact Us CTA** to discuss further

**Example response:**
```
I understand that cart abandonment is a critical challenge for 
e-commerce businesses - it directly impacts revenue and growth.

Based on our work with **SwiftCart E-commerce Platform**, where 
we tackled a similar 72% cart abandonment rate...

[Detailed technical solution]

The results were impressive:
• Reduced cart abandonment from **72% to 28%**
• Increased conversion rate by **53%**
• Generated **$2.3M in additional annual revenue**

For your specific situation...

[Contact Us CTA Button]
```

### **Conversation Features**

- **Conversational memory**: The chatbot remembers the entire conversation
- **Context-aware**: Follow-up questions reference previous messages
- **Source transparency**: Know which case studies informed the response
- **Professional tone**: Consultative yet friendly communication

---

## ⚙️ **Configuration**

### **Environment Variables**

| Variable | Default | Description | Required |
|----------|---------|-------------|----------|
| `ANTHROPIC_API_KEY` | - | Your Anthropic API key | ✅ Yes |
| `TEMPERATURE` | `0.7` | Response creativity (0-1) | ❌ No |
| `MAX_TOKENS` | `1024` | Maximum response length | ❌ No |
| `APP_TITLE` | `ShuruMan` | Browser tab title | ❌ No |
| `APP_ICON` | `🤖` | Browser tab icon | ❌ No |

### **Customizing the Chatbot**

#### **1. Modify Branding**

**File: `ui_components.py`**

```python
# Change primary color
.dashboard-header {
    background: #FFFFFF;
    border-bottom: 3px solid #291f3b;  # ← Your brand color
}

# Update logo
.dashboard-logo {
    height: 48px;
    src: "your-logo-url.png"  # ← Your logo
}
```

#### **2. Adjust Retrieval Settings**

**File: `app.py`**

```python
# Change number of retrieved case studies
retriever=self.vectorstore.as_retriever(search_kwargs={"k": 5})
# ↑ Change k to 3, 7, or 10

# Adjust chunk size
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,      # ← Increase for longer chunks
    chunk_overlap=200     # ← Adjust overlap
)
```

#### **3. Customize System Prompt**

**File: `app.py` - Line 243**

```python
qa_prompt = PromptTemplate(
    template="""You are a solutions consultant for Shuru Tech...
    
    # Modify this prompt to change:
    # - Tone and style
    # - Response structure
    # - Emphasis on certain aspects
    # - Industry-specific language
    """
)
```

#### **4. Update Clickable Prompts**

**File: `ui_components.py`**

```python
def display_chat_prompts():
    # Modify the 3 starter prompts here
    st.button("🚀 Your custom prompt 1", key="prompt1")
    st.button("🤖 Your custom prompt 2", key="prompt2")
    st.button("💬 Your custom prompt 3", key="prompt3")
```

#### **5. Change LLM Model**

**File: `app.py`**

```python
llm = ChatAnthropic(
    model="claude-3-5-sonnet-20241022",  # ← Change model
    temperature=0.7,                      # ← Adjust creativity
    max_tokens=1024                       # ← Adjust length
)

# Available models:
# - claude-3-5-sonnet-20241022 (recommended)
# - claude-3-opus-20240229 (most capable)
# - claude-3-sonnet-20240229 (balanced)
# - claude-3-haiku-20240307 (fastest)
```

---

## 📚 **Knowledge Base**

### **Structure**

The `knowledge_base.json` file contains all the data the chatbot uses:

```json
{
  "company_info": {
    "title": "Shuru Tech",
    "description": "AI-native engineers powering innovation worldwide"
  },
  "case_studies": [
    {
      "id": 1,
      "client_name": "SwiftCart E-commerce Platform",
      "industry": "E-commerce",
      "problem": "Detailed problem description...",
      "solution": "Detailed solution description...",
      "technologies": ["React", "Node.js", "MongoDB"],
      "results": "Measurable results with metrics...",
      "duration": "3 months",
      "url": "https://www.shurutech.com/work"
    }
  ],
  "services": [
    {
      "name": "AI & Automation",
      "description": "Build AI applications that drive innovation..."
    }
  ],
  "pages": [
    {
      "title": "About Us",
      "url": "https://www.shurutech.com/about",
      "content": "Page content..."
    }
  ]
}
```

### **Adding New Case Studies**

1. Open `knowledge_base.json`
2. Add a new object to the `case_studies` array:

```json
{
  "id": 51,
  "client_name": "Your Client Name",
  "industry": "Your Industry",
  "problem": "Detailed problem (2-3 sentences)",
  "solution": "Detailed solution (3-4 sentences)",
  "technologies": ["Tech1", "Tech2", "Tech3"],
  "results": "Measurable results with specific metrics",
  "duration": "Project duration",
  "url": "https://www.shurutech.com/work"
}
```

3. **Restart the app** - Vector store will rebuild automatically

### **Best Practices for Case Studies**

✅ **DO:**
- Include specific metrics and numbers in results
- Use clear problem-solution structure
- List all relevant technologies
- Keep industry classification consistent
- Add duration for project scope context

❌ **DON'T:**
- Use vague language like "improved performance"
- Omit technologies or tools used
- Make results too generic
- Include client-sensitive information
- Mix multiple projects into one case study

### **Case Study Quality Checklist**

- [ ] Client name is professional and descriptive
- [ ] Industry matches standard categories
- [ ] Problem is specific and relatable
- [ ] Solution includes technical details
- [ ] Technologies list is comprehensive
- [ ] Results include at least 2-3 metrics
- [ ] Duration is realistic and specific

---

## 🌐 **Deployment**

### **Streamlit Cloud (Recommended)**

**Streamlit Cloud** offers free hosting for Streamlit apps.

#### **Step 1: Prepare Your Repository**

Ensure you have:
- ✅ `app.py` - Main application file
- ✅ `ui_components.py` - UI components
- ✅ `requirements.txt` - Dependencies
- ✅ `knowledge_base.json` - Case studies data
- ✅ `.streamlit/config.toml` - Streamlit configuration
- ✅ `.gitignore` - Excludes `.env`, `venv/`, etc.

#### **Step 2: Push to GitHub**

```bash
git add .
git commit -m "Prepare for deployment"
git push origin main
```

#### **Step 3: Deploy on Streamlit Cloud**

1. Go to [share.streamlit.io](https://share.streamlit.io/)
2. Click **"New app"**
3. Select your repository: `samaysalunke/shuru-repo`
4. Set **Main file path**: `app.py`
5. Click **"Advanced settings"**
6. Add **Secrets**:
   ```toml
   ANTHROPIC_API_KEY = "your_key_here"
   TEMPERATURE = 0.7
   MAX_TOKENS = 1024
   ```
7. Click **"Deploy"**

#### **Step 4: Configure Domain (Optional)**

1. In Streamlit Cloud dashboard, click your app
2. Go to **Settings** → **General**
3. Set custom **App URL**: `shuru-ai.streamlit.app`

### **Alternative Deployment Options**

#### **Docker**

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
```

```bash
docker build -t shuru-chatbot .
docker run -p 8501:8501 -e ANTHROPIC_API_KEY=your_key shuru-chatbot
```

#### **Heroku**

```bash
heroku create shuru-chatbot
heroku config:set ANTHROPIC_API_KEY=your_key
git push heroku main
```

#### **AWS EC2**

```bash
# SSH into EC2 instance
ssh -i key.pem ubuntu@ec2-instance

# Install dependencies
sudo apt update
sudo apt install python3-pip
pip3 install -r requirements.txt

# Run with nohup
nohup streamlit run app.py &
```

---

## 🐛 **Troubleshooting**

### **Common Issues & Solutions**

#### **1. "Knowledge base not found" Error**

**Problem**: `knowledge_base.json` is missing or corrupted

**Solution**:
```bash
# Check if file exists
ls knowledge_base.json

# Validate JSON syntax
python -c "import json; json.load(open('knowledge_base.json'))"

# If corrupted, re-run scraper
python scrape_website.py
```

#### **2. "Anthropic API key not found" Error**

**Problem**: Environment variable not set

**Solution**:
```bash
# Check .env file exists
cat .env

# Verify key is set
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('ANTHROPIC_API_KEY'))"

# If empty, add key to .env file
echo "ANTHROPIC_API_KEY=your_key_here" >> .env
```

#### **3. Slow Initial Load**

**Problem**: First run downloads embeddings model (~100MB)

**Solution**: This is normal! 
- First load: ~30 seconds
- Subsequent loads: <5 seconds
- Model is cached in `~/.cache/huggingface/`

#### **4. "No module named 'sentence_transformers'" Error**

**Problem**: Dependencies not fully installed

**Solution**:
```bash
pip install --upgrade -r requirements.txt

# If still failing, install individually
pip install sentence-transformers
pip install faiss-cpu
```

#### **5. Empty or Generic Responses**

**Problem**: Vector store not finding relevant chunks

**Solution**:
```bash
# Check case studies loaded
python -c "import json; data = json.load(open('knowledge_base.json')); print(len(data['case_studies']))"

# Verify retrieval
# Enable developer mode in app and check retrieval count
```

#### **6. Memory Errors**

**Problem**: FAISS index too large for available RAM

**Solution**:
```python
# Reduce chunk size in app.py
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,  # Reduce from 1000
    chunk_overlap=100  # Reduce from 200
)
```

#### **7. Streamlit Port Already in Use**

**Problem**: Port 8501 is occupied

**Solution**:
```bash
# Kill process on port 8501
lsof -ti:8501 | xargs kill -9

# Or run on different port
streamlit run app.py --server.port 8502
```

### **Debugging Tips**

#### **Enable Verbose Logging**

**File: `app.py`**
```python
# Set verbose=True for detailed logs
chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=self.vectorstore.as_retriever(search_kwargs={"k": 5}),
    memory=memory,
    verbose=True  # ← Enable this
)
```

#### **Check Console Output**

Watch terminal for:
```
📚 Loaded 50 case studies from knowledge_base.json
✓ Created 50 case study documents for vector store
✓ Split into 127 chunks
🔧 Initializing embeddings model...
🔨 Creating FAISS vector store...
✓ Vector store created with 127 documents
✓ Conversational chain initialized successfully
```

#### **Test Vector Store**

```python
# Run in Python shell
from app import ShuruTechRAGBot

bot = ShuruTechRAGBot()
bot.initialize_chain()

# Test query
response, sources = bot.get_response("Tell me about e-commerce projects")
print(response)
print(f"Found {len(sources)} sources")
```

---

## 📈 **Performance**

### **Current Metrics**

| Metric | Value | Notes |
|--------|-------|-------|
| **First Load** | ~30 seconds | Downloads embeddings model |
| **Subsequent Loads** | <5 seconds | Uses cached model |
| **Query Response** | 2-4 seconds | Includes retrieval + generation |
| **Retrieval Speed** | <100ms | FAISS vector similarity |
| **Memory Usage** | ~500MB | With 50 case studies |
| **Token Usage** | 300-800 tokens/query | Claude API cost |

### **Optimization Tips**

#### **1. Reduce Chunk Size**

Smaller chunks = Faster processing

```python
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,  # Reduce from 1000
    chunk_overlap=100  # Reduce from 200
)
```

#### **2. Adjust Retrieval Count**

Fewer chunks = Faster generation

```python
retriever=self.vectorstore.as_retriever(search_kwargs={"k": 3})
# Reduce from k=5 to k=3
```

#### **3. Cache Vector Store**

Save FAISS index to disk:

```python
# After creating vectorstore
vectorstore.save_local("faiss_index")

# Load on subsequent runs
vectorstore = FAISS.load_local("faiss_index", embeddings)
```

#### **4. Use Smaller LLM**

Faster responses with Claude Haiku:

```python
llm = ChatAnthropic(
    model="claude-3-haiku-20240307",  # Fastest model
    temperature=0.7
)
```

#### **5. Implement Streaming**

Stream responses for better UX:

```python
# In get_response()
for chunk in chain.stream({"question": question}):
    yield chunk
```

### **Cost Optimization**

#### **Claude API Pricing** (as of 2024)

| Model | Input (per 1M tokens) | Output (per 1M tokens) |
|-------|---------------------|----------------------|
| Claude 3.5 Sonnet | $3.00 | $15.00 |
| Claude 3 Opus | $15.00 | $75.00 |
| Claude 3 Haiku | $0.25 | $1.25 |

**Estimated costs for 1000 queries:**
- Average query: 500 input + 300 output tokens
- Sonnet: ~$6.00 per 1000 queries
- Haiku: ~$0.50 per 1000 queries (recommended for high volume)

#### **Free Components:**
- ✅ HuggingFace embeddings (local)
- ✅ FAISS vector search (local)
- ✅ Streamlit hosting (free tier)
- ✅ Storage (GitHub)

**Only cost**: Claude API usage

---

## 🤝 **Contributing**

We welcome contributions! Here's how to get involved:

### **Ways to Contribute**

1. **Add case studies** - Expand the knowledge base
2. **Improve UI/UX** - Enhance the interface
3. **Optimize performance** - Speed improvements
4. **Fix bugs** - Report or fix issues
5. **Documentation** - Improve guides and examples
6. **Features** - Propose new capabilities

### **Contribution Workflow**

1. **Fork the repository**
   ```bash
   # Click "Fork" on GitHub
   git clone https://github.com/YOUR_USERNAME/shuru-repo.git
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Write clean, documented code
   - Follow existing code style
   - Test thoroughly

4. **Commit with clear messages**
   ```bash
   git add .
   git commit -m "feat: Add new feature description"
   ```

5. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   # Go to GitHub and create Pull Request
   ```

### **Code Style Guidelines**

- **Python**: Follow PEP 8
- **Docstrings**: Use clear function descriptions
- **Comments**: Explain complex logic
- **Variables**: Use descriptive names
- **Functions**: Keep focused and modular

### **Testing Checklist**

Before submitting PR:
- [ ] Code runs without errors
- [ ] All features work as expected
- [ ] No breaking changes to existing features
- [ ] Documentation updated if needed
- [ ] Commits are clear and descriptive

---

## 📄 **License**

This project is licensed under the **MIT License**.

Copyright © 2025 Shuru Technologies PTE Ltd

---

## 👥 **Authors & Credits**

### **Core Team**
- **Shuru Tech Engineering Team** - Initial development and architecture
- **AI Integration** - RAG system design and implementation
- **UI/UX Design** - Branding and interface development

### **Technologies & Acknowledgments**

Special thanks to:
- [**Anthropic**](https://www.anthropic.com/) - Claude 3.5 Sonnet API
- [**LangChain**](https://www.langchain.com/) - RAG framework
- [**Streamlit**](https://streamlit.io/) - Web UI framework
- [**HuggingFace**](https://huggingface.co/) - Embeddings models
- [**FAISS**](https://github.com/facebookresearch/faiss) - Vector similarity search
- [**Beautiful Soup**](https://www.crummy.com/software/BeautifulSoup/) - Web scraping

---

## 📞 **Contact & Support**

### **Get in Touch**

- **Website**: [https://www.shurutech.com](https://www.shurutech.com)
- **Email**: hello@shurutech.com
- **Sales**: sales@shurutech.com
- **LinkedIn**: [Shuru Tech](https://www.linkedin.com/company/shurutech)

### **Global Presence**

🇦🇪 **Dubai** | 🇸🇬 **Singapore** | 🇮🇳 **India** | 🇨🇦 **Canada**

### **Services**

- AI & Automation
- Custom Software Development
- Cloud & DevOps
- Data Engineering
- Product Engineering
- Technology Consulting
- Engineering Team Extension

---

## 🚀 **Quick Start Summary**

```bash
# 1. Clone repository
git clone https://github.com/samaysalunke/shuru-repo.git
cd shuru-chatbot

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set API key
echo "ANTHROPIC_API_KEY=your_key_here" > .env

# 5. Run application
streamlit run app.py

# 6. Open browser
# Navigate to http://localhost:8501
```

---

## 📚 **Additional Resources**

- **[QUICKSTART.md](QUICKSTART.md)** - 5-minute setup guide
- **[STREAMLIT_DEPLOYMENT.md](STREAMLIT_DEPLOYMENT.md)** - Deployment guide
- **[DASHBOARD_REBUILD_SUMMARY.md](DASHBOARD_REBUILD_SUMMARY.md)** - UI evolution
- **[Knowledge Base Structure](#-knowledge-base)** - Data format guide

---

**Built with ❤️ by Shuru Tech | Empowering businesses through AI-driven solutions**

---

## ⭐ **Star This Repository**

If you find this project useful, please consider giving it a star on GitHub! It helps others discover the project and motivates us to keep improving it.

[⭐ Star on GitHub](https://github.com/samaysalunke/shuru-repo)

---

*Last updated: October 2025*
