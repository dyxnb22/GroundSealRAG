import json
import tempfile
from pathlib import Path

import numpy as np
import pytest

from groundseal.index.fingerprint import chunk_fingerprint
from groundseal.models.chunk import ChunkRecord
from groundseal.retrieval.embeddings import EmbeddingModel, VectorIndex


def _make_chunk(cid: str) -> ChunkRecord:
    return ChunkRecord(
        chunk_id=cid,
        document_id="DOC-1",
        source_id="SRC-1",
        text=f"text for {cid}",
        start_offset=0,
        end_offset=10,
        heading_path=[],
        chunk_index=0,
        token_count=3,
        visibility="internal",
        allowed_roles=["engineer"],
    )


def test_vector_index_load_rejects_mismatched_chunk_ids():
    chunks = [_make_chunk("CHK-a"), _make_chunk("CHK-b")]
    embeddings = np.random.rand(2, 8).astype(np.float32)

    with tempfile.TemporaryDirectory() as tmp:
        index_dir = Path(tmp)
        np.save(index_dir / "embeddings.npy", embeddings)
        (index_dir / "chunk_ids.json").write_text(json.dumps(["CHK-a", "CHK-wrong"]))

        with pytest.raises(ValueError, match="chunk_ids do not match"):
            VectorIndex.load(chunks, index_dir)


def test_chunk_fingerprint_order_sensitive():
    a = [_make_chunk("CHK-1"), _make_chunk("CHK-2")]
    b = [_make_chunk("CHK-2"), _make_chunk("CHK-1")]
    assert chunk_fingerprint(a) != chunk_fingerprint(b)
