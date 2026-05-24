from typing import List, Dict, Any
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

from app.config import settings
from app.schemas import RagResult


# Load embedding model once
_model = SentenceTransformer("all-MiniLM-L6-v2")


def embed_text(text: str) -> List[float]:
    """Convert text into embedding vector."""
    return _model.encode(text).tolist()


def get_qdrant_client() -> QdrantClient:
    """Initialize Qdrant client with or without API key."""
    return QdrantClient(
        url=settings.QDRANT_URL,
        api_key=settings.QDRANT_API_KEY or None
    )


def retrieve_ats_constraints(job_description: str, top_k: int = 5) -> RagResult:
    """
    Retrieves ATS parser rules and resume‑writing constraints
    based on the job description text using modern Qdrant Query API.
    """

    client = get_qdrant_client()

    # Embed the job description
    query_vec = embed_text(job_description)

    # Perform vector search using modern query_points interface
    response = client.query_points(
        collection_name=settings.QDRANT_COLLECTION_NAME,
        query=query_vec,  # query accepts the raw embedding vector list
        limit=top_k,
        with_payload=True
    )

    rules: List[str] = []
    metadata: List[Dict[str, Any]] = []

    # Extract clean list from response container points
    for hit in response.points:
        payload = hit.payload or {}
        rule_text = payload.get("rule_text")
        if rule_text:
            rules.append(rule_text)
        metadata.append(payload)

    return RagResult(
        rules=rules,
        metadata={"hits": metadata}
    )