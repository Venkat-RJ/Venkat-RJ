# Research notebook visual assets

This folder contains the editable source for the GitHub profile animation and its research figure.

## The experiment that fought back

A 32-second original SVG animation, featuring a small curious research agent and a stubborn replication checker. The story uses a fictional illustrative test. It does not represent an actual scientific run.

**Beats:**

| Time (seconds) | Beat |
| --- | --- |
| 0–4.8 | A hypothesis appears; investigator arrives |
| 4.8–7.4 | An early promising result prompts premature celebration |
| 7.4–11 | The checker rejects replication and knocks the investigator over |
| 11–13.3 | Investigator discovers an unexamined control |
| 13.3–21 | A controlled three-run replay replaces the first result |
| 21–27.2 | Result is written with scope and evidence; checker accepts the record |
| 27.2–32 | The notebook resets for the next experiment |

The only runtime dependency is SVG with native SMIL animation. There is no JavaScript, network content, hosted SVG service, external font, script, or tracking. GitHub embeds the SVG as an image. The first frame acts as a clear fallback, and the static files are available separately for reduced-motion use.

## Generate

Python 3.10 or later and the standard library:

```sh
python media/generate.py
python media/figure.py
python -m unittest discover -s media -p 'test_*.py'
```

Optional local screenshot testing uses Playwright and Chromium:

```sh
python media/preview.py
```

The generator emits `experiment-{dark,light}.svg` and `experiment-{dark,light}-static.svg`. The figure builder reads `frontieror-instances.csv` and emits `frontieror-{dark,light}.svg`.

## Sources and interpretation

- **FrontierOR data:** [`openresearch/frontieror/scheduling-study/assets/final-instance-data.csv`](https://github.com/Venkat-RJ/openresearch/blob/main/frontieror/scheduling-study/assets/final-instance-data.csv), copied here as an explicit pinned input. The chart plots `normalized_advantage` for all 30 final comparisons, grouped by the six published strata. Positive differences favor the frozen solver's mean weighted tardiness; the red dot is the single exception.
- **FACET illustration:** linked directly to the project's published figure. It is not recreated here.
- **Dexter's Laboratory:** built on and credited to Lattice. No inherited Lattice screenshot is presented as original UI work.

Animation art, layout and characters are newly authored for this profile, not extracted from the ClashLex animation or its assets.
