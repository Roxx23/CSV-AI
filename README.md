# 🧠 CSV AI - Intelligent Data Analysis Platform

> A powerful Retrieval-Augmented Generation (RAG) application that enables natural language interactions with CSV data using LangChain and Streamlit.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![LangChain](https://img.shields.io/badge/LangChain-Latest-green.svg)](https://langchain.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Latest-red.svg)](https://streamlit.io/)

## ✨ Features

### 💬 Chat with CSV
- **Natural Language Queries**: Ask questions about your CSV data in plain English
- **Context-Aware Responses**: RAG pipeline retrieves relevant data chunks for accurate answers
- **Conversation Memory**: Maintains chat history for contextual follow-up questions
- **Semantic Search**: FAISS vector store with HuggingFace embeddings for intelligent retrieval

### 📝 Summarize CSV
- **Automated Summarization**: Generate concise summaries of large CSV datasets
- **Map-Reduce Strategy**: Handles documents exceeding context limits efficiently
- **Key Insights Extraction**: Identifies important patterns and information automatically

### 📊 Analyze CSV
- **Autonomous Data Analysis**: AI agent performs complex data operations
- **Python Code Execution**: Dynamic pandas operations via natural language commands
- **Statistical Insights**: Calculate means, correlations, distributions, and more
- **Interactive Q&A**: Ask analytical questions and get computed results instantly

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Frontend** | Streamlit |
| **LLM Provider** | Groq (Llama 3.1-8B-Instant) |
| **Framework** | LangChain |
| **Embeddings** | HuggingFace (sentence-transformers/all-MiniLM-L6-v2) |
| **Vector Store** | FAISS |
| **Data Processing** | Pandas |
| **Agent Framework** | LangChain Experimental Agents |

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Groq API key (get free at [console.groq.com](https://console.groq.com/keys))

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/Roxx23/CSVChatter.git
cd CSVChatter
```

2. **Create virtual environment**
```bash
python -m venv vnv
# Windows
vnv\Scripts\activate
# macOS/Linux
source vnv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**

Create a `.env` file in the project root:
```env
GROQ_API_KEY=your_groq_api_key_here
```

5. **Run the application**
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 📖 Usage

### 1. Chat with CSV
1. Select "Chat with CSV" from the sidebar
2. Upload your CSV file
3. Ask questions like:
   - "What are the top 5 products by sales?"
   - "Show me customers from New York"
   - "What's the average order value?"

### 2. Summarize CSV
1. Select "Summarize CSV" from the sidebar
2. Upload your CSV file
3. Click "Generate Summary"
4. Get a comprehensive overview of your data

### 3. Analyze CSV
1. Select "Analyze CSV" from the sidebar
2. Upload your CSV file
3. Ask analytical questions:
   - "What is the correlation between price and quantity?"
   - "Show me statistics for the revenue column"
   - "How many unique categories are there?"

## 📂 Project Structure

```
CSVChatter/
│
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── .env                   # Environment variables (not tracked)
├── .gitignore            # Git ignore rules
├── README.md             # Project documentation
│
└── vnv/                  # Virtual environment (not tracked)
```

## 🏗️ Architecture

```
User Query
    ↓
CSV Upload → Document Loader → Text Splitter
    ↓
Embeddings (HuggingFace) → Vector Store (FAISS)
    ↓
Retriever ← User Question
    ↓
Retrieved Context + Chat History → Prompt Template
    ↓
LLM (Groq/Llama) → Generated Response
    ↓
User Interface (Streamlit)
```

## 🔑 Key Components

### RAG Pipeline
- **Document Loading**: CSVLoader with encoding fallback (UTF-8/CP1252)
- **Text Splitting**: RecursiveCharacterTextSplitter (1000 chars, 200 overlap)
- **Embeddings**: sentence-transformers/all-MiniLM-L6-v2 (384 dimensions)
- **Vector Store**: FAISS with similarity search (top-6 retrieval)
- **Memory**: Session-based conversation history

### LLM Configuration
```python
model: llama-3.1-8b-instant
temperature: 0.5
max_tokens: 512
provider: Groq (30K RPM free tier)
```

## 🎯 Use Cases

- **Business Analytics**: Quick insights from sales, customer, or inventory data
- **Data Exploration**: Understand new datasets through conversational queries
- **Report Generation**: Automated summaries for stakeholders
- **Data Quality Checks**: Ask questions to identify anomalies or patterns
- **Educational**: Learn data analysis through natural language interaction

## 🚧 Limitations

- In-memory processing (suitable for small to medium CSV files < 100MB)
- Code execution requires `allow_dangerous_code=True` (use in trusted environments)
- Rate limits apply based on Groq free tier (30,000 requests/minute)
- Session memory is not persistent (clears on app restart)

## 🔮 Future Enhancements

- [ ] Support for multiple file formats (Excel, JSON, Parquet)
- [ ] Persistent conversation history with database storage
- [ ] Data visualization generation (charts, graphs)
- [ ] Multi-file comparison and joins
- [ ] Export analysis results to PDF/Excel
- [ ] User authentication and file management
- [ ] Advanced filtering and data transformation
- [ ] Caching for faster repeated queries
- [ ] Support for larger datasets with streaming
- [ ] Custom prompt templates for domain-specific analysis

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


## 🙏 Acknowledgments

- [LangChain](https://langchain.com/) - Framework for LLM applications
- [Streamlit](https://streamlit.io/) - Web framework for data apps
- [Groq](https://groq.com/) - Ultra-fast LLM inference
- [HuggingFace](https://huggingface.co/) - Embedding models
- [FAISS](https://github.com/facebookresearch/faiss) - Vector similarity search

## 📧 Contact

**Ayush Bora** - [thisisayu0912@gmail.com](mailto:thisisayu0912@gmail.com)

Project Link: [https://github.com/Roxx23/CSVChatter](https://github.com/Roxx23/CSVChatter)

---

<div align="center">
  <p>⭐ Star this repo if you find it helpful!</p>
  <p>Made with ❤️ using LangChain & Streamlit</p>
</div>
