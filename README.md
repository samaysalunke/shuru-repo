# 🚀 Shuru Tech AI Solutions Finder

An intelligent RAG (Retrieval-Augmented Generation) chatbot that helps potential clients discover relevant case studies and solutions from Shuru Tech's portfolio. Built with Claude AI, LangChain, and Streamlit.

## ✨ Features

### Core Functionality
- **🤖 AI-Powered Conversations**: Claude 3.5 Sonnet provides consultative, sales-oriented responses
- **📚 RAG Architecture**: Retrieves relevant case studies from vector database before generating responses
- **💬 Conversational Memory**: Maintains context throughout the conversation
- **🎯 Smart Retrieval**: FAISS vector store with semantic search capabilities

### User Experience
- **💡 Example Questions**: Pre-built questions for common use cases
- **📋 Copy Responses**: One-click copying of AI responses
- **🕐 Timestamps**: Track conversation flow with message timestamps
- **💬 Message Counter**: Visual conversation progress tracking
- **👋 Welcoming Empty State**: Professional placeholder guiding new users

### Professional Features
- **📊 Real-time Stats**: View loaded case studies, technologies, and industries
- **🐛 Developer Mode**: Comprehensive debugging information
- **📈 Monitoring**: Detailed logging of all operations
- **🎨 Brand Styling**: Custom Shuru Tech blue theme (#1E3A8A)
- **⚡ Performance**: Local embeddings with HuggingFace models

## 🛠️ Tech Stack

**AI & ML:**
- Claude 3.5 Sonnet (Anthropic)
- LangChain for RAG orchestration
- HuggingFace Embeddings (sentence-transformers/all-MiniLM-L6-v2)
- FAISS for vector storage

**Frontend:**
- Streamlit for interactive UI
- Custom CSS for branding
- Responsive design

**Backend:**
- Python 3.8+
- BeautifulSoup4 for web scraping
- Python logging for monitoring

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- Anthropic API key

### Setup Steps

1. **Clone the repository**
```bash
git clone <repository-url>
cd shuru-chatbot
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
Create a `.env` file in the project root:
```env
ANTHROPIC_API_KEY=your_api_key_here
TEMPERATURE=0.7
MAX_TOKENS=1024
APP_TITLE=Shuru Tech AI Assistant
APP_ICON=🚀
```

5. **Prepare knowledge base**
Run the scraper to collect case studies (if available):
```bash
python scrape_website.py
```

Or manually create `knowledge_base.json` with your case studies.

## 🚀 Usage

### Starting the Application

```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

### Using the Chatbot

1. **Start a Conversation**
   - Type your question in the chat input
   - Or click one of the example questions in the sidebar

2. **View Responses**
   - AI provides consultative responses with case study references
   - Click on case study expanders to see full details
   - Use the "Copy Response" button to save responses

3. **Explore Features**
   - Toggle "Developer Mode" to see system status
   - View stats about loaded case studies
   - Check timestamps for conversation flow
   - Clear conversation to start fresh

### Demo Mode

For demonstrations:
1. Enable "Developer Mode" to show technical capabilities
2. Use example questions for consistent demos
3. Highlight case study retrieval in sources section
4. Show message counter and timestamps
5. Demonstrate copy functionality

## 📊 Knowledge Base Structure

The `knowledge_base.json` file should follow this structure:

```json
{
  "company_info": {
    "title": "Company Name",
    "description": "Company description"
  },
  "case_studies": [
    {
      "client_name": "Client Name",
      "industry": "Industry",
      "problem": "Description of the problem",
      "solution": "Description of the solution",
      "technologies": ["Tech1", "Tech2"],
      "results": "Measurable results achieved",
      "duration": "Project duration"
    }
  ],
  "services": [
    {
      "name": "Service Name",
      "description": "Service description"
    }
  ],
  "pages": [
    {
      "title": "Page Title",
      "url": "https://example.com",
      "content": "Page content"
    }
  ]
}
```

## 🎯 Key Components

### Vector Store (FAISS)
- Processes documents into 1000-character chunks
- 200-character overlap for context preservation
- Uses HuggingFace embeddings for semantic search
- Retrieves top 5 most relevant documents

### RAG Chain
- ConversationalRetrievalChain for context-aware responses
- Custom prompt engineering for consultative tone
- Memory buffer maintains conversation history
- Returns source documents for transparency

### UI Components
- **Sidebar**: Example questions, stats, developer mode
- **Main Chat**: Message history with timestamps
- **Empty State**: Welcoming placeholder
- **Sources**: Expandable case study details

## 🔧 Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `ANTHROPIC_API_KEY` | Required | Your Anthropic API key |
| `TEMPERATURE` | 0.7 | Model temperature (0-1) |
| `MAX_TOKENS` | 1024 | Maximum response length |
| `APP_TITLE` | Shuru Tech AI Assistant | Browser tab title |
| `APP_ICON` | 🚀 | Browser tab icon |

### Customization

**Branding:**
- Update color scheme in CSS section (line ~337)
- Modify header title and subtitle (line ~375)
- Change example questions (line ~397)

**Retrieval:**
- Adjust chunk size/overlap (line ~175-178)
- Modify retrieval count (line ~275: `search_kwargs={"k": 5}`)
- Change embedding model (line ~187)

**Prompts:**
- Edit system prompt (line ~244-269)
- Customize response guidelines
- Adjust tone and style instructions

## 🐛 Troubleshooting

### Common Issues

**Vector store not loading:**
- Verify `knowledge_base.json` exists and is valid JSON
- Check that case_studies array is not empty
- Enable Developer Mode to see detailed status

**API errors:**
- Confirm ANTHROPIC_API_KEY is set correctly in `.env`
- Check API key has sufficient credits
- Review error messages in console logs

**Slow responses:**
- First query initializes embeddings (takes ~10 seconds)
- Subsequent queries should be faster
- Consider using GPU for embeddings if available

**Empty responses:**
- Check knowledge base has relevant content
- Verify retrieval is finding documents (Developer Mode)
- Review console logs for errors

## 📈 Future Enhancements

- **User Authentication**: Multi-user support with personalized history
- **Feedback System**: Thumbs up/down ratings for responses
- **Export Conversations**: Download chat history as PDF/Markdown
- **Multi-language Support**: Internationalization for global reach
- **Advanced Analytics**: Track popular queries and user behavior
- **Integration**: Webhooks for CRM systems (Salesforce, HubSpot)
- **A/B Testing**: Compare different prompt strategies
- **Voice Input**: Speech-to-text for hands-free interaction

## 📸 Screenshots

_Add screenshots here showing:_
- Main chat interface
- Example questions sidebar
- Case study sources
- Developer mode
- Empty state

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:
1. Fork the repository
2. Create a feature branch
3. Make your changes with clear commit messages
4. Test thoroughly
5. Submit a pull request

## 📄 License

[Add your license here]

## 👥 Authors

- **Shuru Tech Team** - Initial development

## 🙏 Acknowledgments

- Anthropic for Claude API
- LangChain for RAG framework
- Streamlit for UI framework
- HuggingFace for embeddings

---

**Built with ❤️ by Shuru Tech**
