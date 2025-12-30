
# 📄 RAG-Based Personal Documents Chatbot

A **Retrieval-Augmented Generation (RAG)** chatbot that allows users to upload personal documents and ask questions based **strictly on the document content**.

Built using:

* FastAPI (backend)
* LangChain
* FAISS
* HuggingFace / OpenAI LLM
* Streamlit (UI)

⚠️ This project is for educational purposes only.

---

## 🚀 Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## 🧠 How It Works

* Documents are split into chunks
* Chunks are embedded and stored in FAISS
* User queries retrieve relevant chunks
* LLM generates answers only from retrieved context

---

## 📌 Features

* Document-based Q&A
* RAG-based architecture
* Reduced hallucinations
* Local vector search
