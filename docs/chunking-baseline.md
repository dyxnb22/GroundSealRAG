# Chunking Baseline

## Strategy

- **Chunk size**: 512 characters
- **Overlap**: 64 characters
- **Boundary**: Split on markdown `##` headings first; sub-split large sections by character window
- **chunk_id**: `CHK-{sha256(source_id:document_id:chunk_index)[:16]}`

## Traceability

Each chunk carries `source_id`, `document_id`, `heading_path`, `start_offset`, `end_offset`, and inherited permission fields from source.

## Tradeoffs

- 512 chars balances citation precision vs semantic completeness
- Heading-aware splits improve citation labels
- Overlap reduces boundary misses at cost of duplicate retrieval
