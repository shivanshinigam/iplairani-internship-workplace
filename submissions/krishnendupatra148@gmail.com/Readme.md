# Conversational Intelligence Engine

## Overview

This project is a context-aware conversational AI system built using Python, LangChain, Groq LLM, and ChromaDB.

The chatbot can:
- Answer user questions naturally
- Maintain conversation memory
- Use previous interactions for contextual responses
- Retrieve relevant information using RAG (Retrieval-Augmented Generation)

The system avoids behaving like a stateless chatbot by storing recent conversation history.

---

# Features

- Context-aware conversation
- Retrieval-Augmented Generation (RAG)
- Conversation memory using LangChain
- Vector database using ChromaDB
- Sentence-transformer embeddings
- Edge case handling:
  - Empty input
  - Repeated queries
  - Invalid input

---

# Technologies Used

- Python
- LangChain
- Groq API
- ChromaDB
- HuggingFace Embeddings
- Sentence Transformers

---

# System Design

1. User enters a query
2. Query is converted into embeddings
3. Relevant documents are retrieved from ChromaDB
4. Previous conversation history is loaded
5. Prompt is constructed using:
   - Retrieved context
   - Conversation history
   - Current user question
6. LLM generates a contextual response
7. Conversation memory is updated

---

# Project Structure

```text
krishnendupatra148@gmail.com/
│
├── chatbot.py
├── requirements.txt
└── README.md
```

---

# How to Run

## Step 1: Install dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Add your Groq API key

Replace:

```python
YOUR_GROQ_API_KEY
```

with your actual Groq API key in `chatbot.py`.

---

## Step 3: Run the project

```bash
python chatbot.py

```
Or open and run `chatbot.ipynb` in Jupyter Notebook

---

# Example

User:
```text
How do I proceed to the next stage?
```

Bot:
```text
you: How do I proceed to the next stage?
bot: To proceed to the next stage, I would need more information about the current stage you are referring to. The context provided seems to be related to artificial intelligence and machine learning, but it doesn't give me enough details to provide a specific answer.

Could you please provide more context or clarify what you mean by "the next stage"? Are you referring to a specific process, project, or task? I'll do my best to assist you once I have a better understanding of your question.

```

---

# Approach and Decisions

- Used RAG architecture for contextual retrieval
- Used ChromaDB as vector database
- Used conversation memory to maintain context
- Limited memory window to last 3 interactions for efficiency
- Added edge-case handling for robustness

---

# Assumptions

- Internet connection is available for LLM API access
- Groq API key is valid
- The chatbot uses a small sample knowledge base for demonstration

