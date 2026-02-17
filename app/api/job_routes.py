from fastapi import APIRouter, HTTPException
from uuid import uuid4
from datetime import datetime
from app.schemas.schemas import JobCreate
from app.services.embedding_service import generate_embedding
from app.db.chroma_client import job_collection
from app.services.matching_service import match_candidates
from app.services.explanation_service import generate_explanation

router = APIRouter()
"""
Router for job-related API endpoints.
Handles job creation, candidate matching, and explanation generation.
"""


@router.post("/jobs")
def create_job_api(job: JobCreate):
    """
    Create a new job, generate its embedding,
    and store it in ChromaDB with metadata.
    """

    job_id = str(uuid4())

    embedding = generate_embedding(job.description)

    metadata = {
        "id": job_id,
        "title": job.title,
        "country": job.country,
        "created_at": str(datetime.utcnow())
    }

    job_collection.add(
        ids=[job_id],
        embeddings=[embedding],
        metadatas=[metadata]
    )

    return metadata


@router.get("/jobs/{job_id}/match")
def match_job(
    job_id: str,
    min_experience: int = None,
    country: str = None
):
    """
    Retrieve job embedding and return semantically
    similar candidates using vector similarity search.
    """

    result = job_collection.get(
        ids=[job_id],
        include=["embeddings"]
    )

    # Validate job existence
    if result is None:
        return {"error": "Job not found"}

    if "embeddings" not in result:
        return {"error": "Embedding not found"}

    if len(result["embeddings"]) == 0:
        return {"error": "Job not found"}

    job_embedding = result["embeddings"][0]

    matches = match_candidates(job_embedding)

    return matches


@router.get("/jobs/{job_id}/explain/{candidate_id}")
def explain_candidate_match(job_id: str, candidate_id: str):
    """
    Generate an AI-based explanation describing why
    a specific candidate matches the given job.
    """

    explanation = generate_explanation(job_id, candidate_id)

    if explanation.startswith("Invalid"):
        raise HTTPException(status_code=404, detail=explanation)

    if explanation.startswith("Error"):
        raise HTTPException(status_code=500, detail=explanation)

    return {
        "job_id": job_id,
        "candidate_id": candidate_id,
        "explanation": explanation
    }
