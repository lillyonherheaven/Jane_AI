"""
Jane-AI - Local Hybrid RAG Engine
Module: rag.py
Description: Ingests PDFs, research papers, notes, and code repositories using
Hybrid Retrieval (ChromaDB Dense Vectors + BM25 Sparse Keyword Ranking) for optimal accuracy.
"""

import os
from pathlib import Path
from typing import List, Dict, Any, Optional
import math


class DocumentChunk:
    def __init__(self, text: str, metadata: Dict[str, Any], chunk_id: str):
        self.text = text
        self.metadata = metadata
        self.chunk_id = chunk_id


class LocalHybridRAG:
    """
    100% Local RAG pipeline combining ChromaDB dense vector indexing
    with rank-bm25 lexical term matching and reciprocal rank fusion (RRF).
    """

    def __init__(self, collection_name: str = "jane_academic_vault"):
        self.collection_name = collection_name
        self.persist_dir = Path.home() / ".jane_ai" / "chroma_db"
        self.persist_dir.mkdir(parents=True, exist_ok=True)

        self.chroma_client = None
        self.collection = None
        self.bm25 = None
        self.corpus_chunks: List[DocumentChunk] = []

        self._init_vector_store()

    def _init_vector_store(self):
        """Initializes local ChromaDB client with sentence embeddings or Ollama embeddings."""
        try:
            import chromadb
            from chromadb.config import Settings

            self.chroma_client = chromadb.PersistentClient(
                path=str(self.persist_dir),
                settings=Settings(anonymized_telemetry=False)
            )
            self.collection = self.chroma_client.get_or_create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine"}
            )
            print(f"[RAG Engine] ChromaDB initialized at {self.persist_dir}")
        except Exception as e:
            print(f"[RAG Engine Warning] ChromaDB setup notice: {e}. Running in memory fallback.")

    def ingest_pdf(self, file_path: str, chunk_size: int = 600, overlap: int = 100) -> int:
        """
        Parses and chunks academic PDFs or text documents into vector and BM25 indices.
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Document '{file_path}' does not exist.")

        raw_text = ""
        if path.suffix.lower() == ".pdf":
            try:
                import pypdf
                reader = pypdf.PdfReader(str(path))
                for page_idx, page in enumerate(reader.pages):
                    page_text = page.extract_text() or ""
                    raw_text += f"\n--- Page {page_idx + 1} ---\n" + page_text
            except ImportError:
                with open(path, "rb") as f:
                    raw_text = f.read().decode("utf-8", errors="ignore")
        else:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                raw_text = f.read()

        # Sliding window chunking
        words = raw_text.split()
        added_count = 0

        for i in range(0, len(words), chunk_size - overlap):
            chunk_words = words[i:i + chunk_size]
            if not chunk_words:
                continue
            chunk_text = " ".join(chunk_words)
            chunk_id = f"{path.stem}_chunk_{added_count}"
            metadata = {"source": path.name, "index": added_count, "length": len(chunk_text)}

            doc_chunk = DocumentChunk(text=chunk_text, metadata=metadata, chunk_id=chunk_id)
            self.corpus_chunks.append(doc_chunk)

            # Insert into ChromaDB collection if available
            if self.collection:
                try:
                    self.collection.add(
                        documents=[chunk_text],
                        metadatas=[metadata],
                        ids=[chunk_id]
                    )
                except Exception as e:
                    print(f"[RAG] Vector insert note: {e}")

            added_count += 1

        # Re-index BM25
        self._rebuild_bm25()
        print(f"[RAG Engine] Successfully ingested '{path.name}' ({added_count} chunks).")
        return added_count

    def _rebuild_bm25(self):
        """Constructs rank-bm25 index over all memory chunks."""
        try:
            from rank_bm25 import BM25Okapi
            tokenized_corpus = [doc.text.lower().split() for doc in self.corpus_chunks]
            if tokenized_corpus:
                self.bm25 = BM25Okapi(tokenized_corpus)
        except ImportError:
            self.bm25 = None

    def hybrid_search(self, query: str, top_k: int = 3, vector_weight: float = 0.6) -> List[Dict[str, Any]]:
        """
        Executes hybrid retrieval combining Vector similarity + BM25 keyword matching with RRF.
        """
        if not self.corpus_chunks:
            return []

        # 1. BM25 Sparse Search
        bm25_scores = {}
        if self.bm25:
            tokenized_query = query.lower().split()
            scores = self.bm25.get_scores(tokenized_query)
            for idx, score in enumerate(scores):
                bm25_scores[idx] = float(score)
        else:
            # Fallback simple keyword counting
            q_terms = set(query.lower().split())
            for idx, doc in enumerate(self.corpus_chunks):
                doc_terms = set(doc.text.lower().split())
                overlap = len(q_terms.intersection(doc_terms))
                bm25_scores[idx] = float(overlap)

        # 2. ChromaDB Dense Search (if active)
        vector_ranked_ids = []
        if self.collection:
            try:
                results = self.collection.query(query_texts=[query], n_results=min(top_k * 2, len(self.corpus_chunks)))
                if results and "ids" in results and results["ids"]:
                    vector_ranked_ids = results["ids"][0]
            except Exception:
                pass

        # 3. Reciprocal Rank Fusion & Combined Scoring
        combined_scores: List[Dict[str, Any]] = []
        for idx, doc in enumerate(self.corpus_chunks):
            sparse_score = bm25_scores.get(idx, 0.0)
            dense_rank = vector_ranked_ids.index(doc.chunk_id) if doc.chunk_id in vector_ranked_ids else 999
            
            # Reciprocal rank score
            rrf_dense = 1.0 / (60 + dense_rank)
            normalized_sparse = math.log1p(max(0.0, sparse_score))

            final_score = (vector_weight * rrf_dense * 100) + ((1 - vector_weight) * normalized_sparse)
            combined_scores.append({
                "chunk_id": doc.chunk_id,
                "text": doc.text,
                "metadata": doc.metadata,
                "score": round(final_score, 4)
            })

        combined_scores.sort(key=lambda x: x["score"], reverse=True)
        return combined_scores[:top_k]

    def format_rag_context(self, retrieved_chunks: List[Dict[str, Any]]) -> str:
        """Formats RAG retrieved snippets for multi-agent prompt conditioning."""
        if not retrieved_chunks:
            return ""

        lines = ["[ACADEMIC & LOCAL KNOWLEDGE VAULT (ChromaDB + BM25 Hybrid)]:"]
        for idx, c in enumerate(retrieved_chunks, start=1):
            src = c.get("metadata", {}).get("source", "Document")
            lines.append(f"Document [{idx}] ({src}):\n{c.get('text')}\n")
        return "\n".join(lines)


# Global RAG Instance
rag_engine = LocalHybridRAG()
