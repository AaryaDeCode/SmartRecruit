from fastapi import FastAPI
from app.api import resumes

app = FastAPI(
    title="CareerYatra Resume Ranking API",
    version="1.0.0"
)

app.include_router(resumes.router, prefix="/api/resumes", tags=["Resumes"])

@app.get("/")
async def root():
    return {"message": "Welcome to the CareerYatra Resume API"}
