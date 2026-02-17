from fastapi import APIRouter
from uuid import uuid4
from datetime import datetime
from app.schemas.schemas import CandidateCreate
from app.services.embedding_service import generate_embedding
from app.db.chroma_client import candidate_collection

router = APIRouter()
"""
Router for candidate-related API endpoints.
Handles candidate creation and vector storage.
"""


@router.post("/candidates")
def create_candidate_api(candidate: CandidateCreate):
    """
    Create a new candidate, generate embedding for skill description,
    and store it in ChromaDB with metadata.
    """

    candidate_id = str(uuid4())

    embedding = generate_embedding(candidate.skill_description)

    metadata = {
        "id": candidate_id,
        "name": candidate.name,
        "experience": candidate.experience,
        "location": candidate.location,
        "created_at": str(datetime.utcnow())
    }

    candidate_collection.add(
        ids=[candidate_id],
        embeddings=[embedding],
        metadatas=[metadata]
    )

    return metadata
