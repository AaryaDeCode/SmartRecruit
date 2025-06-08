from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
import os
import uuid
import torch

from app.services.parser import extract_text_from_resume, extract_entities, build_knowledge_graph
from app.services.scorer import final_score, get_keywords_from_gemini, GCN, sbert_model
from app.models.resume import create_resume_document
from app.database import mongodb

router = APIRouter()
device = 'cuda' if torch.cuda.is_available() else 'cpu'
gcn_model = GCN(input_dim=384, hidden_dim=128, output_dim=64).to(device)

UPLOAD_FOLDER = "uploaded_resumes"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@router.post("/upload-resume/")
async def upload_resume(file: UploadFile = File(...), job_description: str = Form(...)):
    # 1. Save file to disk temporarily
    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_FOLDER, unique_filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    # 2. JD parsing
    jd_keywords = get_keywords_from_gemini(job_description)
    jd_entities = extract_entities(job_description)
    jd_graph = build_knowledge_graph(jd_entities)

    # 3. Resume parsing
    resume_text = extract_text_from_resume(file_path)
    resume_entities = extract_entities(resume_text)
    resume_graph = build_knowledge_graph(resume_entities)

    # 4. Score calculation
    scores = final_score(resume_text, job_description, resume_graph, jd_graph, gcn_model, jd_keywords)
    scores = [float(s) for s in scores]  # Convert np.float32 to float
    # 5. Save to MongoDB
    document = create_resume_document(file.filename, resume_text, scores, jd_keywords, resume_entities)
    await mongodb.db.resumes.insert_one(document)
    # Optional: Delete temp file after processing
    os.remove(file_path)

    return {
        "filename": file.filename,
        "scores": {
            "semantic": scores[0],
            "graph": scores[1],
            "rule_based": scores[2],
            "cultural_fit": scores[3],
            "final": scores[4],
        },
        "keywords": jd_keywords
    }
