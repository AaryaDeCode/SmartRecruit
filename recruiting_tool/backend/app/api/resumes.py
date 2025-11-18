from fastapi import APIRouter, UploadFile, File, Form
import os
import uuid
from app.services.parser import extract_text_from_resume, extract_entities, build_knowledge_graph
from app.services.scorer import final_score, get_keywords_from_gemini, GCN, sbert_model
from app.database import mongodb
from app.models.resume import create_resume_document
import torch

router = APIRouter()
device = 'cuda' if torch.cuda.is_available() else 'cpu'
gcn_model = GCN(input_dim=384, hidden_dim=128, output_dim=64).to(device)

UPLOAD_FOLDER = "uploaded_resumes"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@router.post("/upload-resume/")
async def upload_resume(file: UploadFile = File(...), job_description: str = Form(...)):
    # 1. Save File
    file_path = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4()}_{file.filename}")
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # 2. JD Parsing
    jd_keywords = get_keywords_from_gemini(job_description)
    jd_entities = extract_entities(job_description)
    jd_graph = build_knowledge_graph(jd_entities)

    # 3. Resume Parsing
    resume_text = extract_text_from_resume(file_path)
    resume_entities = extract_entities(resume_text)
    resume_graph = build_knowledge_graph(resume_entities)

    # 4. Score Calculation
    scores = final_score(resume_text, job_description, resume_graph, jd_graph, gcn_model, jd_keywords)

# ✅ Convert all NumPy float32 to native Python float
    scores = [float(s) for s in scores]

    # 5. Save to MongoDB
    document = create_resume_document(file.filename, resume_text, scores, jd_keywords, resume_entities)
    await mongodb.db.resumes.insert_one(document)


    return {
        "filename": file.filename,
        "scores": document["scores"],

        "keywords": jd_keywords
    }
