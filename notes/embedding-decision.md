# Embedding Decision

## Choice

`sentence-transformers/all-MiniLM-L6-v2`

## Rationale

- Local-first, no API key required
- Small model (~80MB), fast on CPU
- 384-dim embeddings, sufficient for small enterprise corpus
- normalize_embeddings=True for cosine via dot product

## Fallback

`BAAI/bge-small-en-v1.5` if recall on paraphrase cases is insufficient.
