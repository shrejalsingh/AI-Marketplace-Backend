from fastapi import FastAPI
from app.api import candidate_routes, job_routes

"""
Application entry point.

Initializes the FastAPI application and
registers API route modules.
"""

# Create FastAPI app instance
app = FastAPI(
    title="AI Job-Candidate Matching Engine",
    description="Backend system for semantic job-candidate matching using vector embeddings.",
    version="0.0.1"
)

# Register API routers
app.include_router(candidate_routes.router)
app.include_router(job_routes.router)
