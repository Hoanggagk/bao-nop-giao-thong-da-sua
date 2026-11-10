# Conversion report

## Source and scope

- Source used: `TRAJECTORY TRACKING CONTROL OF A QUADCOPTER USING PROXIMAL POLICY OPTIMIZATION.docx` (the file present in the workspace; no separate filename ending in `(1).docx` was present).
- Source SHA-256: `17fb5feb06a122b810aa9aa900e21ec81323c232cc3c61ad47e31e3de25fa96a`.
- The source Word file was read only and was not overwritten.
- Conversion date: 2026-11-09.

## Successfully converted and verified

- The title, authors, affiliation, article information, Abstract, Keywords, six main sections, Conclusion, and References were separated into the requested component files.
- `paper.md` was rebuilt from those components and successfully parsed back through Pandoc as Markdown and HTML without a conversion error.
- All **21 references** are present in `references/references.md` and in the combined paper.
- All **79 mathematical objects** detected by Pandoc in the Word source are present in the combined Markdown. A normalized multiset comparison of the LaTeX expressions (ignoring the added `\tag{...}` commands) matched exactly.
- The document contains **13 numbered display-equation occurrences**, with source labels `1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 11, 12`. This source numbering was preserved rather than corrected.
- All **7 numbered figure captions** (Fig. 1 through Fig. 7) are present.
- The Word package contains **12 embedded media files**: 2 front-matter logos and 10 scientific figure-panel files. Figures 1–4 each use one file; Figures 5–7 each use two files (`a` and `b`). SHA-256 comparisons confirm that all 12 extracted assets are byte-for-byte identical to the media in the Word package.
- All image references in `paper.md` resolve to existing relative paths.
- Both scientific data tables were converted to editable Markdown tables and retained inline in the relevant sections. Standalone copies are also stored in `assets/tables/`:
  - Table I: 17 parameter rows.
  - Table 2: 24 result rows (10 trials × 2 methods, two mean rows, and two standard-deviation rows).
- The generated article contains exactly two parsed Markdown data tables. Word also uses layout tables for the journal header, numbered equations, and multi-panel figures; these are not additional scientific data tables.

## Items requiring manual review

The following points already exist in the Word source. They were deliberately preserved and not scientifically corrected:

1. Equation numbering is duplicated: the CF velocity equation and the RMSE equation are both numbered `(11)`; the next equation is numbered `(12)`.
2. The sentence introducing equation `(12)` says that MAE is calculated, but equation `(12)` repeats the RMSE expression from equation `(11)`.
3. In the waypoint-completion reward, equation `(6)` uses the threshold `\epsilon`, while the following prose defines and uses `r_w = 0.2 m` as the waypoint-completion radius.
4. The source includes wording/typographic anomalies such as `trajectory tracking..`, `Dicussion`, `. Let`, and missing spaces in `architecture.The`, `updates.Both`, and several math-to-text boundaries.
5. The second table caption is written as `Table 2. Comparison of ppo and carrot-following results`, whereas nearby prose refers to `Table II`.
6. The source heading text for Sections 3–6 does not include explicit leading section numbers, while Sections 1 and 2 do. The heading text was retained as supplied.
7. The Article Info block contains editor placeholders and a DOI marked “edited by editors”; these values were retained unchanged.

These items should be checked by the authors in the Word source or corrected deliberately in the Markdown components only after scientific review.

## Rebuild verification

Run:

```powershell
python .\scripts\build_paper.py
```

The builder concatenates the component files in source order and adjusts component-relative asset paths for the project-root `paper.md`.
