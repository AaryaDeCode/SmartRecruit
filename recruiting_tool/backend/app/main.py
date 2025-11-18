from fastapi import FastAPI
from app.api import resumes
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or set your specific Streamlit URL for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app = FastAPI(
    title="CareerYatra Resume Ranking API",
    version="1.0.0"
)

app.include_router(resumes.router, prefix="/api/resumes", tags=["Resumes"])

@app.get("/")
async def root():
    return {"message": "Welcome to the CareerYatra Resume API"}
