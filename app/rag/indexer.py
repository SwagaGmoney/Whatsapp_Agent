from typing import List, Dict
from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams
from app.config import get_settings

settings = get_settings()


def get_qdrant_client() -> QdrantClient:
    return QdrantClient(
        url=settings.QDRANT_URL,
        api_key=settings.QDRANT_API_KEY or None
    )


def create_collection_if_missing(vector_size: int = 1536):
    """Creates Qdrant collection for ATS rules if it doesn't exist."""
    client = get_qdrant_client()

    collections = client.get_collections().collections
    names = [c.name for c in collections]

    if settings.QDRANT_COLLECTION_NAME not in names:
        client.create_collection(
            collection_name=settings.QDRANT_COLLECTION_NAME,
            vectors_config=VectorParams(size=vector_size, distance="Cosine")
        )


def index_ats_rules(rules: List[Dict]):
    """
    Indexes ATS parser rules into Qdrant.
    Each rule dict must contain:
    - "rule_text": str
    - "embedding": List[float]
    - optional metadata
    """

    client = get_qdrant_client()

    points = []
    for i, rule in enumerate(rules):
        points.append({
            "id": i,
            "vector": rule["embedding"],
            "payload": rule
        })

    client.upsert(
        collection_name=settings.QDRANT_COLLECTION_NAME,
        points=points
    )
