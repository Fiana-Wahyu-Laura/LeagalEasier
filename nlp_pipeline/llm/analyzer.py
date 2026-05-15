"""
llm/analyzer.py — LegalEasier NLP Pipeline
Deteksi dan klasifikasi klausul berisiko menggunakan LLM (Sprint 3).

Tugasnya (sesuai CLAUDE.md §9):
    Langkah 7 dari pipeline — LLM analysis:
    - Deteksi klausul yang berpotensi merugikan user
    - Klasifikasikan ke level: "Tinggi", "Sedang", "Rendah", "Aman"
    - Sertakan penjelasan dalam bahasa Indonesia sederhana

Rules (CLAUDE.md §9 LLM Calls):
- SELALU gunakan RAG context dari retriever — JANGAN tanya LLM tanpa dokumen.
- Validasi JSON output LLM sebelum disimpan — retry sekali jika parse error.
- Risk levels HANYA boleh: "Tinggi", "Sedang", "Rendah", "Aman".
- Setiap output wajib sertakan confidence score (float 0.0–1.0).
- Primary LLM: Claude API. Fallback: GPT-4.
- Semua LLM error harus di-catch — jangan crash pipeline.

Aturan kode:
- Tidak ada hardcoded API key.
- Semua fungsi harus punya type hints.
- Tidak ada bare except.
"""

# TODO Sprint 3: Implementasi fungsi-fungsi berikut:
#
# from dataclasses import dataclass, field
# from typing import Literal
#
# RiskLevel = Literal["Tinggi", "Sedang", "Rendah", "Aman"]
#
# @dataclass
# class RiskClause:
#     clause_text: str
#     plain_language: str
#     risk_level: RiskLevel
#     confidence: float  # 0.0–1.0
#
# @dataclass
# class AnalysisResult:
#     risk_clauses: list[RiskClause]
#     summary: str
#     disclaimer: str = (
#         "Hasil ini bersifat informatif dan bukan pengganti "
#         "konsultasi hukum profesional."
#     )
#
# def analyze_document(document_id: str, context_chunks: list[str]) -> AnalysisResult:
#     """Analisis dokumen hukum menggunakan LLM dengan RAG context."""
#     ...
