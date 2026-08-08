# Provenance of canonical papers

Established 2026-08-03 (WP0 version audit). Each canonical file was copied from the
newest-content source found anywhere in the repo (zip archives excluded), then normalized.
Superseded copies remain on disk untracked (`Draft II/`, `Finals/`, `The Crystal/`, repo root).

| Canonical file | Source copied | Why that source |
|---|---|---|
| `prime_sum_formula_paper.tex` (named `u_space_prime_formula_paper.tex` until 2026-08-08, renamed to match the paper's title and its verification script) | `Draft II/u_space_prime_formula_paper (1).tex` (2026-08-01 14:14) | Revision adding the McKenzie attribution (abstract, intro, related work) and the Companion/Code bibitems; the root copy (13:23) lacks both |
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

## Placeholders (all resolved 2026-08-03)

- Companion cross-citations: **filled** with the published Zenodo DOIs in all four papers —
  Paper 1 `10.5281/zenodo.21769103`, Paper 2 `10.5281/zenodo.21769105`,
  Paper 3 `10.5281/zenodo.21769107` (preprints, CC BY 4.0, ORCID 0009-0007-5500-9175).
  These replaced the arXiv-ID TODOs via the submission pack's Zenodo fallback route; arXiv
  proper can follow later as record versions if an endorsement materializes.
- Repository URL: **filled** with `https://github.com/carlgribble-caa/prime-moments`
  in all four Code bibitems.

No placeholders remain in any paper.

## Zenodo v1.0 releases (2026-08-09)

New versions of the trilogy records were published via `tools/zenodo_update.py` with the
literature-review revisions (v1.0, publication date 2026-08-08). Before rebuilding the PDFs,
each paper's Companion bibitems were switched from version DOIs to concept DOIs
("cite all versions"), so cross-citations always resolve to the latest version.

| Paper | Concept DOI (cited) | v1.0 version DOI |
|---|---|---|
| Paper 1 `prime_sum_formula_paper` | `10.5281/zenodo.21769102` | `10.5281/zenodo.21855605` |
| Paper 2 `prime_ladder_paper` | `10.5281/zenodo.21769104` | `10.5281/zenodo.21855606` |
| Paper 3 `prime_recovery_paper` | `10.5281/zenodo.21769106` | `10.5281/zenodo.21855607` |

The original v0.x version DOIs (`…21769103`, `…21769105`, `…21769107`) remain resolvable as
prior versions of the same concept records. Note: the v0.x records carried the `.tex` source
alongside the PDF; the v1.0 versions carry the PDF only (Paper 1's file also renamed from
`u_space_prime_formula_paper.pdf` to `prime_sum_formula_paper.pdf`).

## Audit note

Paper 1's abstract claim of "forty exact interval tests" was recounted against
`code/prime_sum_formula.py` and is **correct**: 20 dyadic + 5 edge + 8 random + 5 count + 2 span = 40.
