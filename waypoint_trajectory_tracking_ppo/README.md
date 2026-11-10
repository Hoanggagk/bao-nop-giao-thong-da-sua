# Waypoint Trajectory Tracking with PPO — Markdown source

This directory is the editable Markdown conversion of the Word article **“WAYPOINT TRAJECTORY TRACKING CONTROL OF A QUADCOPTER USING PROXIMAL POLICY OPTIMIZATION.”** The Word source remains unchanged outside this directory.

## Project structure

- `frontmatter/`: title/authors, Abstract, and Keywords.
- `sections/`: the six main article sections in source order.
- `references/references.md`: all 21 references.
- `assets/figures/`: seven numbered figures represented by ten panel image files, plus two front-matter logos.
- `assets/tables/`: standalone copies of the two scientific data tables. The same tables remain inline in their article sections so `paper.md` is self-contained.
- `metadata.md`: conversion and article metadata.
- `CONVERSION_REPORT.md`: completeness checks and source issues requiring manual review.
- `scripts/build_paper.py`: deterministic builder for the combined article.
- `paper.md`: combined article generated from the component files.

## Build the combined article

From this directory, run:

```powershell
python .\scripts\build_paper.py
```

The script reads the component files in article order and rewrites `paper.md`. Edit the component files rather than editing `paper.md` directly, then rebuild.

## Asset links

Component files use paths such as `../assets/figures/figure_01.png`. During the build, these become `assets/figures/figure_01.png`, which is correct relative to the project-root `paper.md`.

Figures 5–7 each contain two source panels (`a` and `b`). Their HTML table layout and captions are retained in `sections/05_results_discussion.md`.
