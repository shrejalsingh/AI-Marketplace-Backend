# AI Job-Candidate Matching Engine

This project is a backend system that matches candidates to jobs using
vector embeddings and semantic similarity. It also provides an
AI-powered explanation endpoint to describe why a candidate matches a
specific job.

The system is built using FastAPI, ChromaDB, Sentence Transformers, and
the OpenAI API.

------------------------------------------------------------------------

# Project Overview

The application allows:

-   Creating jobs
-   Creating candidates
-   Storing embeddings in ChromaDB
-   Performing semantic similarity matching
-   Generating AI-based explanations for matches

The system follows a clean layered architecture separating API routes,
business logic, and database configuration.

------------------------------------------------------------------------

# Project Structure

```
AI-Marketplace-Backend/
│
├── app/
│   │
│   ├── api/
│   │   ├── candidate_routes.py
│   │   └── job_routes.py
│   │
│   ├── services/
│   │   ├── embedding_service.py
|   |   ├── explanation_service.py
│   │   └── explanation_service.py
│   │
│   ├── db/
│   │   └── chroma_client.py
│   │
│   ├── schemas/
│   │   └── schemas.py
│   │
│   ├── config.py
│   └── main.py
│
├── .env
├── requirements.txt
└── README.md
```


------------------------------------------------------------------------

# Setup Instructions

## 1. Clone the Repository

```git clone <repository_url>```  
```cd kovon_ai_matching_engine```

## 2. Create Virtual Environment

Windows:

```python -m venv venv ```   
```venv\Scripts\activate```

macOS/Linux:

```python3 -m venv venv```  
```source venv/bin/activate```

## 3. Install Dependencies

```pip install -r requirements.txt```

If requirements.txt is not available:

pip install fastapi uvicorn chromadb sentence-transformers openai
python-dotenv

## 4. Configure Environment Variables

Create a .env file in the project root:

```OPENAI_API_KEY=your_openai_api_key```

Add .env to .gitignore to avoid committing secrets.

## 5. Run the Application

```uvicorn app.main:app --reload```

Open API documentation:

http://127.0.0.1:8000/docs

------------------------------------------------------------------------

# Architecture Explanation

The system follows a three-layer structure:

## API Layer (FastAPI)

Handles HTTP requests and returns responses.

Key endpoints:

-   POST /candidates
-   POST /jobs
-   GET /jobs/{job_id}/explain/{candidate_id}

## Service Layer

Contains business logic.

embedding_service.py\
Generates embeddings using Sentence Transformers.

explanation_service.py\
Fetches metadata from ChromaDB and calls the OpenAI API to generate
explanations.

## Database Layer (ChromaDB)

Stores:

-   Embeddings
-   UUIDs
-   Metadata (experience, country, etc.)

Each job and candidate is stored with a unique ID, vector embedding, and
associated metadata.

------------------------------------------------------------------------

# Embedding Model Used

Model: all-MiniLM-L6-v2\
Library: Sentence Transformers

This model converts text into 384-dimensional vectors representing
semantic meaning.

Reasons for selection:

-   Lightweight and fast
-   Strong semantic understanding
-   Suitable for production use
-   Widely adopted in NLP systems

------------------------------------------------------------------------

# Similarity Metric Explanation

ChromaDB uses cosine similarity to compare embeddings.

Cosine similarity measures the angle between two vectors rather than
their magnitude.

Formula:

cos(θ) = (A · B) / (\|\|A\|\| × \|\|B\|\|)

Where:

-   A = Job embedding
-   B = Candidate embedding
-   · = Dot product
-   \|\|A\|\| and \|\|B\|\| = Vector magnitudes

Cosine similarity is effective for text embeddings because it measures
semantic closeness and is independent of vector scale.

A higher cosine similarity score indicates stronger semantic similarity
between job and candidate descriptions.

------------------------------------------------------------------------

# Explanation Endpoint

Endpoint:

GET /jobs/{job_id}/explain/{candidate_id}

Process:

1.  Retrieve job metadata from ChromaDB.
2.  Retrieve candidate metadata from ChromaDB.
3.  Construct structured prompt.
4.  Send prompt to OpenAI API.
5.  Return generated explanation.

Model used for explanation:

gpt-4o-mini

Selected for cost efficiency, speed, and strong instruction-following
capability.

------------------------------------------------------------------------

# Matching Flow

1.  A job is created and stored with an embedding.
2.  A candidate is created and stored with an embedding.
3.  Embeddings are compared using cosine similarity.
4.  Most similar candidates are retrieved.
5.  Optional AI explanation can be generated for a job-candidate pair.

------------------------------------------------------------------------

# Design Decisions

-   Used ChromaDB for vector storage and similarity search.
-   Used Sentence Transformers for efficient embedding generation.
-   Used OpenAI API instead of hosting a local LLM.
-   Separated routes from business logic for maintainability.
-   Used environment variables for secure configuration.

------------------------------------------------------------------------

# Possible Improvements

-   Add caching for OpenAI responses.
-   Add match scoring endpoint.
-   Add authentication and authorization.
-   Add pagination for large datasets.
-   Add Docker support.
-   Deploy to a cloud platform.

------------------------------------------------------------------------

# Conclusion

This project demonstrates:

-   Vector-based semantic search
-   Cosine similarity matching
-   LLM-powered explanation generation
-   Clean FastAPI backend architecture
-   Secure environment-based configuration

It provides a scalable foundation for AI-powered recruitment matching
systems.
