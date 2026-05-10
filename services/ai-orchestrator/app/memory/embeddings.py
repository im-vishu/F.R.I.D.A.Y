import hashlib
import math


VECTOR_SIZE = 384


def create_mock_embedding(text: str) -> list[float]:
    """
    Deterministic local mock embedding.
    Good for development/testing.
    Replace later with OpenAI/Gemini embeddings.
    """
    vector = [0.0] * VECTOR_SIZE

    words = text.lower().split()

    for word in words:
        digest = hashlib.sha256(word.encode("utf-8")).hexdigest()
        index = int(digest[:8], 16) % VECTOR_SIZE
        value = (int(digest[8:16], 16) % 1000) / 1000.0
        vector[index] += value

    norm = math.sqrt(sum(x * x for x in vector))

    if norm == 0:
        return vector

    return [x / norm for x in vector]