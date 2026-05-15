"""
llm/translator.py — LegalEasier NLP Pipeline
Terjemahan klausul hukum ke bahasa sederhana Indonesia (Sprint 3).

Tugasnya:
    Terima satu klausul hukum → kembalikan penjelasan dalam bahasa
    Indonesia yang mudah dipahami oleh masyarakat umum (bukan pengacara).

Rules:
- Output harus dalam bahasa Indonesia.
- Jangan tambahkan opini hukum — hanya parafrase/penjelasan.
- Wajib sertakan disclaimer pada setiap output.
- Primary LLM: Claude API. Fallback: GPT-4.

Aturan kode:
- Tidak ada hardcoded API key.
- Semua fungsi harus punya type hints.
- Tidak ada bare except.
"""

# TODO Sprint 3: Implementasi fungsi-fungsi berikut:
#
# def translate_clause(clause_text: str, context: str = "") -> str:
#     """Terjemahkan satu klausul hukum ke bahasa sederhana Indonesia."""
#     ...
#
# def translate_clauses_batch(
#     clauses: list[str], context: str = ""
# ) -> list[str]:
#     """Terjemahkan banyak klausul sekaligus — lebih efisien dari satu per satu."""
#     ...
