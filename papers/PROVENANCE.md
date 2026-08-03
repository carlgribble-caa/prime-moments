# Provenance of canonical papers

Established 2026-08-03 (WP0 version audit). Each canonical file was copied from the
newest-content source found anywhere in the repo (zip archives excluded), then normalized.
Superseded copies remain on disk untracked (`Draft II/`, `Finals/`, `The Crystal/`, repo root).

| Canonical file | Source copied | Why that source |
|---|---|---|
| `u_space_prime_formula_paper.tex` | `Draft II/u_space_prime_formula_paper (1).tex` (2026-08-01 14:14) | Revision adding the McKenzie attribution (abstract, intro, related work) and the Companion/Code bibitems; the root copy (13:23) lacks both |
| `prime_ladder_paper.tex` | `Draft II/prime_ladder_paper (1).tex` (2026-08-01 14:15) | Same revision wave: adds McKenzie/Companion/Code references and completed bibitems; root copy (13:26) predates it |
| `prime_recovery_paper.tex` | `Finals/prime_recovery_paper.tex` (mtime 06:40 is a zip-extraction artifact) | Content superset of `Draft II/prime_recovery_paper.tex`: author name, the AI-disclosure section, the Section-2 self-containment sentence referenced by the cover letters; no mathematical differences between the two |
| `multiplication_crystal_paper.tex` | `The Crystal/multiplication_crystal_paper.tex` (2026-08-02 16:10) | Only copy |

## Normalizations applied to the canonical copies (2026-08-03)

1. Author `[Author Name]` → `Carl Gribble` (Papers 1–2; Papers 3–4 were already named).
2. `\thanks` placeholder ("AI assistance to be disclosed per the target venue's policy") →
   "A full disclosure of AI use appears at the end of the paper." (Papers 1–2).
3. Added `\section*{Disclosure of AI use}` to Papers 1–2, modeled on Paper 3's, with per-paper
   verification references (Section 6 / Section 5) and series position (first / second).
4. Fixed a doubled-dash typo in Paper 3's disclosure paragraph.
5. Bibliography self-references unified to `C. Gribble` across all four papers
   (matching Paper 4's existing style).

## Outstanding placeholders (deliberate; tracked under WP0 in PROGRAMME.md)

- `% TODO: replace with arXiv ID once posted` — companion cross-citations in all four papers.
- `https://github.com/USERNAME/REPO` — Code bibitems in all four papers; fill when the GitHub
  repository is created (the submission pack in `Finals/` suggests `carlgribble-caa/prime-moments`).

## Audit note

Paper 1's abstract claim of "forty exact interval tests" was recounted against
`code/prime_sum_formula.py` and is **correct**: 20 dyadic + 5 edge + 8 random + 5 count + 2 span = 40.
