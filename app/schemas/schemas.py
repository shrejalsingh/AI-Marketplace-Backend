from pydantic import BaseModel

"""
Pydantic schema definitions for request validation.

Defines data models for candidate and job creation.
"""


class CandidateCreate(BaseModel):
    """
    Schema for creating a new candidate.
    """

    name: str
    skill_description: str
    experience: int
    location: str


class JobCreate(BaseModel):
    """
    Schema for creating a new job.
    """

    title: str
    country: str
    description: str
