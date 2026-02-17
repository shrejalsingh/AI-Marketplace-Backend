import math
from app.db.chroma_client import candidate_collection

"""
Matching service module.

Provides cosine similarity computation and candidate
matching logic based on embedding similarity and filters.
"""


def cosine_similarity(vec1: list, vec2: list) -> float:
    """
    Compute cosine similarity between two vectors.

    Args:
        vec1 (list): First embedding vector.
        vec2 (list): Second embedding vector.

    Returns:
        float: Cosine similarity score.
    """

    dot_product = 0.0
    norm_a = 0.0
    norm_b = 0.0

    for i in range(len(vec1)):
        dot_product += vec1[i] * vec2[i]
        norm_a += vec1[i] * vec1[i]
        norm_b += vec2[i] * vec2[i]

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return dot_product / (math.sqrt(norm_a) * math.sqrt(norm_b))


def match_candidates(
    job_embedding: list,
    min_experience: int = None,
    country: str = None
) -> list:
    """
    Match candidates against a job embedding using cosine similarity.

    Optional filters:
        - Minimum experience
        - Country (location)

    Args:
        job_embedding (list): Embedding vector of the job.
        min_experience (int, optional): Minimum required experience.
        country (str, optional): Required candidate location.

    Returns:
        list: Top 5 matched candidates sorted by similarity and experience.
    """

    # Retrieve all candidate embeddings and metadata
    results = candidate_collection.get(
        include=["embeddings", "metadatas"]
    )

    ids = results.get("ids", [])
    embeddings = results.get("embeddings", [])
    metadatas = results.get("metadatas", [])

    matches = []

    for i in range(len(ids)):
        candidate_id = ids[i]
        candidate_embedding = embeddings[i]
        metadata = metadatas[i]

        # Apply minimum experience filter
        if min_experience is not None:
            if metadata["experience"] < min_experience:
                continue

        # Apply location filter
        if country is not None:
            if metadata["location"].lower() != country.lower():
                continue

        similarity = cosine_similarity(job_embedding, candidate_embedding)

        matches.append({
            "candidateId": candidate_id,
            "similarityScore": round(similarity, 4),
            "experience": metadata["experience"]
        })

    # Sort by similarity score and experience (descending)
    matches.sort(
        key=lambda x: (x["similarityScore"], x["experience"]),
        reverse=True
    )

    return matches[:5]
