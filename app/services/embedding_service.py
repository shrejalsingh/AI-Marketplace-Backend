from sentence_transformers import SentenceTransformer
from app.config import EMBEDDING_MODEL_NAME

"""
Embedding service module.

Initializes the Sentence Transformer model and provides
a utility function to generate vector embeddings from text.
"""

# Load embedding model at startup
model = SentenceTransformer(EMBEDDING_MODEL_NAME)


def generate_embedding(text: str) -> list:
    """
    Generate a vector embedding for the given text input.

    Args:
        text (str): Input text to be converted into embedding.

    Returns:
        list: Embedding vector as a list of floats.
    """

    embedding = model.encode(text)
    return embedding.tolist()
