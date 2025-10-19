# 🚀 Quick Start Guide - New Dashboard

## Run the Dashboard in 3 Steps

### 1. Activate Virtual Environment
```bash
cd /Users/samaysalunke/Documents/everything-hobby/shuru-chatbot
source venv/bin/activate
```

### 2. Verify Setup (Optional)
```bash
python test_chatbot.py
```
Expected output:
```
✅ All systems operational! Ready for demo.
```

### 3. Launch the Application
```bash
streamlit run app.py
```

The dashboard will open automatically in your browser at `http://localhost:8501`

---

## 📊 What You'll See

### Dashboard Layout
```
┌─────────────────────────────────────────────────┐
│  🚀 Shuru Tech Solutions Finder                 │
└─────────────────────────────────────────────────┘
┌──────────┬──────────────┬─────────────────────┐
│  STATS   │    CHAT      │  CASE STUDIES       │
│          │              │                     │
│ 📁 10    │  Messages    │  [Filter...]        │
│ ⚙️ 25    │              │  • Client 1         │
│ 🏢 8     │  [Input]     │  • Client 2         │
└──────────┴──────────────┴─────────────────────┘
```

---

## 🎯 Key Features

### Left Panel: Statistics
- **Case Studies Count** - Number of case studies in knowledge base
- **Technologies Count** - Unique technologies across all projects
- **Industries Count** - Industries served
- **System Status** - Model info and API connection status
- **Clear Chat Button** - Reset conversation

### Center Panel: Chat
- **Chat Messages** - User and AI responses
- **Case Study Sources** - Expandable sections with full details
- **Chat Input** - Type your business challenge

### Right Panel: Case Study Browser
- **Filter Box** - Search by client name or industry
- **Case Study List** - Browse all available case studies
- **Hover Effects** - Visual feedback on interaction

---

## 💡 Usage Tips

### Ask a Question
1. Type your business challenge in the chat input
2. Example: "We're experiencing slow payment processing"
3. Hit Enter to submit

### View Sources
1. AI response will include case study references
2. Click the expander to see full case study details
3. Includes: Problem, Solution, Technologies, Results

### Browse Case Studies
1. Use the filter box to search by name
2. Scroll through the list on the right panel
3. All case studies are visible at a glance

### Clear Chat
1. Click "🗑️ Clear Chat" button in left panel
2. Resets conversation and memory
3. Start fresh conversation

---

## 🔧 Troubleshooting

### Issue: Module not found
**Solution:** Make sure virtual environment is activated
```bash
source venv/bin/activate
```

### Issue: Knowledge base not found
**Solution:** Verify `knowledge_base.json` exists
```bash
ls -la knowledge_base.json
```

### Issue: API key missing
**Solution:** Check `.env` file has `ANTHROPIC_API_KEY`
```bash
cat .env | grep ANTHROPIC_API_KEY
```

### Issue: Port already in use
**Solution:** Run on a different port
```bash
streamlit run app.py --server.port 8502
```

---

## 📁 Project Structure

```
shuru-chatbot/
├── app.py                          # Main Streamlit application
├── ui_components.py                # UI component library
├── knowledge_base.json             # Case studies data
├── test_chatbot.py                 # RAG system validation tests
├── scrape_website.py               # Advanced web scraper
├── scrape_with_playwright.py       # JS-rendered content scraper
├── merge_knowledge.py              # Knowledge base merger
├── requirements.txt                # Dependencies
├── .env                            # Environment variables
├── setup.sh / setup.bat            # Setup scripts
└── README.md                       # Full documentation
```

---

## 🎨 Customization

### Change Colors
Edit `ui_components.py` → `inject_dashboard_styles()`:
```python
# Change primary color (blue)
border-color: #3B82F6;  # Change this hex color

# Change hover effects
background: #F9FAFB;    # Change this hex color
```

### Adjust Panel Widths
Edit `app.py` → line 353:
```python
# Current: [1, 2, 1] - equal left/right, double center
col1, col2, col3 = st.columns([1, 2, 1])

# Make center wider: [1, 3, 1]
col1, col2, col3 = st.columns([1, 3, 1])

# Make all equal: [1, 1, 1]
col1, col2, col3 = st.columns([1, 1, 1])
```

### Change Number of Case Studies Shown
Edit `app.py` → line 526:
```python
# Current: shows 15 case studies
for cs in case_studies_list[:15]:

# Show more: 25 case studies
for cs in case_studies_list[:25]:
```

---

## 🔗 Related Documentation

- **`README.md`** - Full project documentation
- **`STREAMLIT_DEPLOYMENT.md`** - Deployment guide
- **`DASHBOARD_REBUILD_SUMMARY.md`** - UI evolution notes
- **`MOBILE_RESPONSIVE_GUIDE.md`** - Mobile optimization guide

---

## 🆘 Support

If you encounter issues:
1. Run `python test_chatbot.py` for RAG system diagnostics
2. Check all files are present: `app.py`, `ui_components.py`, `knowledge_base.json`
3. Verify virtual environment is activated
4. Check Streamlit version: `streamlit --version` (should be ≥1.31.0)

---

## ✅ Checklist

Before running:
- [ ] Virtual environment activated
- [ ] `knowledge_base.json` exists
- [ ] `.env` file with API key present
- [ ] Dependencies installed (`pip install -r requirements.txt`)

After running:
- [ ] Dashboard loads without errors
- [ ] Three panels visible
- [ ] Stats display correctly
- [ ] Chat input works
- [ ] Case studies appear in browser
- [ ] Filter functionality works

---

**Enjoy your new dashboard! 🎉**

Built with ❤️ using 21st.dev components + Streamlit

