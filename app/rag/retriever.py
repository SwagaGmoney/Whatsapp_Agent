from typing import List
from qdrant_client import QdrantClient
from qdrant_client.http.models import Filter, FieldCondition, MatchValue
from app.config import get_settings
from app.schemas import RagResult

settings = get_settings()


def get_qdrant_client() -> QdrantClient:
    """Initialize Qdrant client with or without API key."""
    return QdrantClient(
        url=settings.QDRANT_URL,
        api_key=settings.QDRANT_API_KEY or None
    )


def retrieve_ats_constraints(job_description: str, top_k: int = 5) -> RagResult:
    """
    Retrieves ATS parser rules and resume‑writing constraints
    based on the job description text.
    """

    client = get_qdrant_client()

    # Perform vector search
    search_results = client.search(
        collection_name=settings.QDRANT_COLLECTION_NAME,
        query_vector=job_description,
        limit=top_k
    )

    rules: List[str] = []
    metadata = []

    for hit in search_results:
        payload = hit.payload or {}
        rule_text = payload.get("rule_text")
        if rule_text:
            rules.append(rule_text)
        metadata.append(payload)

    return RagResult(
        rules=rules,
        metadata={"hits": metadata}
    )
