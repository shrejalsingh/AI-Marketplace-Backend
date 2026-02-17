from uuid import uuid4
from datetime import datetime

"""
In-memory data store for candidates and jobs.

Used for temporary storage during development or testing.
Not intended for production persistence.
"""

candidates_store = {}
jobs_store = {}


def create_candidate(data: dict) -> dict:
    """
    Create a candidate entry with a unique ID and timestamp,
    and store it in the in-memory candidate store.
    """

    candidate_id = str(uuid4())
    data["id"] = candidate_id
    data["created_at"] = datetime.utcnow()

    candidates_store[candidate_id] = data
    return data


def create_job(data: dict) -> dict:
    """
    Create a job entry with a unique ID and timestamp,
    and store it in the in-memory job store.
    """

    job_id = str(uuid4())
    data["id"] = job_id
    data["created_at"] = datetime.utcnow()

    jobs_store[job_id] = data
    return data
