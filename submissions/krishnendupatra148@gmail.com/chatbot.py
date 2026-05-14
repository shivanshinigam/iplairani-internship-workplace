from langchain_classic.memory import ConversationBufferWindowMemory
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq

#Splitting documents into chunk
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
docs = splitter.create_documents([
    "Machine learning is a subset of artificial intelligence.",
    "RAG combines retrieval with LLM generation."
])

#Creating embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

#storing vector in ChromaDB
vectorstore = Chroma.from_documents(
    docs,
    embeddings
)

# Retrieve top 2 relevant documents from vector database
retriever = vectorstore.as_retriever(search_kwargs={'k': 2})

import os

os.environ["GROQ_API_KEY"] = "your api key"



llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)


# Prompt template combining retrieved context, conversation history, and user question

prompt = ChatPromptTemplate.from_template("""
You are a helpful AI assistant.

Use the following context to answer the question.

Context:
{context}

Previous Conversation:
{history}

Question:
{question}
""")

# Store last 3 conversations for contextual memory
memory = ConversationBufferWindowMemory(
    k=3,  
    return_messages=True
)


# Build RAG pipeline using retrieved context, memory history, prompt template, and LLM
rag_chain = (
    {
        "context": retriever,
        "question": RunnablePassthrough(),
        "history": lambda x: memory.load_memory_variables({})["history"]
    }
    | prompt
    | llm
)


# Continuous conversation loop with memory-aware response generation
while True:
    user_input = input("you:")
    if user_input.lower()== 'exit':
        break
    response = rag_chain.invoke(user_input)
    print("bot:",response.content)
    memory.save_context(
    {"input": user_input},
    {"output": response.content}
)
