"""
llm/risk_scorer.py — LegalEasier NLP Pipeline
Hitung skor risiko dokumen 0–100 berbasis analisis LLM (Sprint 3).

Skor risiko:
    0–20   : Aman — tidak ada klausul yang merugikan
    21–40  : Rendah — ada beberapa catatan minor
    41–70  : Sedang — ada klausul yang perlu diperhatikan
    71–100 : Tinggi — ada klausul yang berpotensi sangat merugikan

Rules (CLAUDE.md §9):
- risk_score harus integer antara 0–100.
- Skor dihitung dari kombinasi: jumlah klausul berisiko, level,
  dan confidence score masing-masing klausul.
- Tidak boleh null — default ke 0 jika analisis gagal.

Aturan kode:
- Tidak ada hardcoded API key.
- Semua fungsi harus punya type hints.
- Tidak ada bare except.
"""

# TODO Sprint 3: Implementasi fungsi-fungsi berikut:
#
# def compute_risk_score(risk_clauses: list["RiskClause"]) -> int:
#     """Hitung skor risiko agregat 0–100 dari daftar klausul berisiko.
#
#     Args:
#         risk_clauses: Hasil dari analyzer.analyze_document().
#
#     Returns:
#         Integer 0–100. 0 = tidak ada risiko, 100 = risiko tertinggi.
#     """
#     ...
