import math
from collections import Counter

from app.core.config import get_settings
from app.services.text_utils import tokenize


_model = None


def cosine_similarity(left: str, right: str) -> float:
    settings = get_settings()
    if settings.enable_local_embeddings:
        embedded = _embedding_similarity(left, right)
        if embedded is not None:
            return embedded
    return _token_cosine(left, right)


def _token_cosine(left: str, right: str) -> float:
    left_counts = Counter(tokenize(left))
    right_counts = Counter(tokenize(right))
    if not left_counts or not right_counts:
        return 0.0
    common = set(left_counts) & set(right_counts)
    numerator = sum(left_counts[token] * right_counts[token] for token in common)
    left_norm = math.sqrt(sum(value * value for value in left_counts.values()))
    right_norm = math.sqrt(sum(value * value for value in right_counts.values()))
    return round(numerator / (left_norm * right_norm), 4) if left_norm and right_norm else 0.0


def _embedding_similarity(left: str, right: str) -> float | None:
    global _model
    try:
        from sentence_transformers import SentenceTransformer
    except Exception:
        return None
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    vectors = _model.encode([left, right], normalize_embeddings=True)
    return float((vectors[0] * vectors[1]).sum())

