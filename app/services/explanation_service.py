"""
Explanation service module.

Uses OpenAI API to generate a professional explanation
for why a candidate matches a given job based on metadata.
"""

from openai import OpenAI
from app.config import OPENAI_API_KEY
from app.db.chroma_client import job_collection, candidate_collection


# Validate API key at startup
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set in environment variables.")


# Initialize OpenAI client once
client = OpenAI(api_key=OPENAI_API_KEY)


def generate_explanation(job_id: str, candidate_id: str) -> str:
    """
    Generate an AI-based explanation describing why a
    specific candidate matches a given job.

    Args:
        job_id (str): Unique identifier of the job.
        candidate_id (str): Unique identifier of the candidate.

    Returns:
        str: AI-generated explanation text or error message.
    """

    # Retrieve job metadata
    job_result = job_collection.get(
        ids=[job_id],
        include=["metadatas"]
    )

    # Retrieve candidate metadata
    candidate_result = candidate_collection.get(
        ids=[candidate_id],
        include=["metadatas"]
    )

    # Validate existence
    if not job_result["metadatas"] or not candidate_result["metadatas"]:
        return "Invalid job or candidate."

    job = job_result["metadatas"][0]
    candidate = candidate_result["metadatas"][0]

    # Construct structured prompt
    prompt = f"""
    You are an expert HR recruiter.

    Provide a clear and professional explanation (3–4 sentences)
    for why this candidate is a good match for the job.

    Job Details:
    - Title: {job.get('title')}
    - Country: {job.get('country')}
    - Minimum Experience: {job.get('min_experience', 'Not specified')}

    Candidate Details:
    - Name: {candidate.get('name')}
    - Experience: {candidate.get('experience')} years
    - Location: {candidate.get('location')}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional recruitment assistant."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=200
        )

        explanation = response.choices[0].message.content.strip()
        return explanation

    except Exception as e:
        return f"Error generating explanation: {str(e)}"
