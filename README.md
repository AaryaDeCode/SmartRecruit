

---

````markdown
# 🤖 CareerYatra – AI-Powered Resume Filtering & Ranking System

CareerYatra is an intelligent resume filtering and ranking platform designed to help recruiters automatically score and shortlist resumes based on job descriptions. Powered by NLP, GCN, and Gemini AI, it ensures context-aware, multi-layered evaluation of resumes in real-time.

---

## 🚀 Features

✅ Upload multiple resumes  
✅ Extract semantic information using SBERT  
✅ Analyze structure using GCN (Graph Convolution Network)  
✅ Extract entities using RoBERTa-based NER  
✅ Rank resumes based on multi-channel scoring  
✅ Get keyword insights using Gemini API  
✅ Download/view resumes directly from the frontend  
✅ Store parsed resumes in MongoDB  
✅ Built with FastAPI (backend) + Streamlit (frontend)

---

## 🧠 Tech Stack

- **Frontend**: Streamlit  
- **Backend API**: FastAPI  
- **NLP Models**:  
  - `SentenceTransformer` (SBERT) for semantic similarity  
  - `dslim/bert-base-NER` for named entity recognition  
  - GCN (PyTorch Geometric) for graph embeddings  
- **Database**: MongoDB (via Motor Async)  
- **AI API**: Google Gemini for keyword extraction  
- **OCR**: `pdfplumber` & `pytesseract` for text extraction from resumes  

---

## 📁 Folder Structure

```bash
careeryatra/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── resumes.py         # Resume upload & scoring API
│   │   ├── services/
│   │   │   ├── parser.py          # OCR, NER, graph building
│   │   │   └── scorer.py          # Gemini, SBERT, GCN scoring
│   │   ├── models/
│   │   │   └── resume.py          # Resume document schema
│   │   ├── database.py            # MongoDB config
│   │   └── main.py                # FastAPI entry point
│
├── frontend/
│   ├── pages/
│   │   └── recruiter_dashboard.py # Streamlit recruiter interface
│   ├── utils/
│   │   └── api_client.py          # FastAPI call handler
│   └── app.py                     # Streamlit app entry
│
├── uploaded_resumes/             # Temp folder for uploaded PDFs
├── README.md                     # ← You're here!
````

---

## 🛠️ How to Run

### 1️⃣ Clone the repo

```bash
git clone https://github.com/your-username/careeryatra.git
cd careeryatra
```

### 2️⃣ Set up the backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # On Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 3️⃣ Set up the frontend

```bash
cd ../frontend
streamlit run app.py
```

Make sure MongoDB is running locally on `mongodb://localhost:27017`.

---

## 📊 Resume Scoring Breakdown

| Channel        | Description                                      | Weight |
| -------------- | ------------------------------------------------ | ------ |
| Semantic Match | SBERT-based similarity between JD & resume text  | 50%    |
| Graph Match    | GCN-based similarity of resume vs JD graph       | 20%    |
| Rule-based     | Keyword match (skills, tools) from Gemini output | 30%    |
| Cultural Fit   | Sentiment analysis of resume                     | 10%    |

---

## 📌 Sample Use Case

> Upload 10 resumes, paste a job description like *"Looking for a MERN Stack Developer with internship experience"*, and the system will:
>
> * Parse all resumes
> * Extract insights and rank them
> * Let you download or preview any resume immediately

---



