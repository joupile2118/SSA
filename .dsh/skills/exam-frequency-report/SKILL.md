---
name: exam-frequency-report
description: Analyze how often each topic of a textbook chapter has been examined across past papers, then typeset an exam-frequency report (PDF) with per-question tagging, frequency tables, tier rankings, and a gap analysis against the current assignment. Use when the user asks for 考频 / 历年考频 / 真题考点分布 / "which topics are examined most", or wants a revision priority order derived from past papers. Also covers deriving a matched review problem set and answer key from the same analysis.
---

# Exam-frequency report

Turn a set of past exam papers plus one textbook chapter into an evidence-backed revision
priority: **which topics carried how many marks, how often, and what that implies for study
order.** Every mark in the report must be traceable to one sub-question of one paper.

Typical inputs: a textbook (scanned PDF or LaTeX source), N past papers as PDFs, and optionally
the current assignment. Keep source scripts, intermediate files, and final documents in the task
workspace.

For this SSA workspace, follow [WORKFLOW.md](../../../WORKFLOW.md): DSH builds and hands off the textbook; when homework is released, Codex delivers the homework booklet, homework solutions, frequency report, review problem set, and review solutions in that order, verifying each before the next. The review pair is already authorized by this standing workflow; an explicit narrower user request takes precedence.

## 0. Start here when a course inventory already exists

This skill ships with instance data for one course. **Read it before doing any discovery** — it
records the material paths, the textbook's per-chapter page and section map, the paper structure
with every sub-question mark (already sum-checked), the canonical tier rules, and which chapters
have reports already.

- `references/course-materials.md` — the inventory and the chapter register.

If that file matches the task, you can skip straight to §2 with the paper list and §3 with the
section codes in hand. If the task is a **different course**, copy the reference file, retarget the
paths and the chapter table, and keep the method sections unchanged.

When building chapter *n* of a course that already has chapter 1 done:

- **Reuse the shared sample.** The same papers serve every chapter; do not re-derive the paper
  structure or re-verify the per-paper mark totals.
- **Reuse the section codes and tier rules verbatim**, so the chapters stay comparable. Reports
  from different chapters must be directly stackable.
- **Draw exercise text from the re-typeset textbook source when one exists** rather than OCR-ing
  the scan, and reuse the existing translation's wording if there is one.
- **Register the finished report** in the chapter register, so the next agent sees the state.

Supporting files in this skill directory:

| File | Use |
|---|---|
| `references/course-materials.md` | instance data: paths, chapter map, paper marks, register |
| `assets/report-preamble.tex` | preamble with the known failure modes already fixed |
| `assets/report-template.tex` | compilable report skeleton — fill the CAPS placeholders |
| `scripts/check_tex_pdf.py` | overfull-box / page-count / aspect-ratio gate |

## 1. Fix the taxonomy from the textbook's own numbering

Read the textbook's table of contents and adopt **its** section codes verbatim (`§1.4.2`). Never
invent a taxonomy: the reader must be able to open the book and find the section.

- Scanned textbook → `pdftoppm -f <a> -l <b> -r 110 -png book.pdf toc` and read the TOC images.
- LaTeX textbook → `grep -n "\\\\section\|\\\\subsection" book.tex` gives the codes directly.
- Record section titles in the source language and in the language of the exam if they differ.
- Note which sections are marked optional/starred and whether they were ever examined; exclude
  them from statistics only if you say so explicitly.

## 2. Extract the papers, then verify against the rendered page

**`pdftotext -layout` is lossy for mathematics. Never tag marks from extracted text alone.**

Extract for speed, then render every page and actually look at it:

```sh
pdftotext -layout paper.pdf -            # fast pass, for structure and wording
pdftoppm -r 110 -png paper.pdf page     # then read the images to confirm
```

What extraction silently destroys — all observed in real papers:

| In the paper | Extracted as | Consequence |
|---|---|---|
| $t^2$, $n^2$ | `t`, `n` | wrong function, wrong density |
| $\frac{16}{\omega^2+16}$ | *(empty)* | missing data, unanswerable part |
| $\sigma^2 e^{-\alpha\lvert\tau\rvert}$ | `σ e ∣ ∣` | lost exponents and limits |
| band edges $144\pi \le \lvert\omega\rvert \le 156\pi$ | usually intact | but confirm against the figure |

Cross-check every formula, every mark value, and every figure-dependent number. Mark values are
the scoring basis; a misread mark invalidates the frequency table.

If a rendered page shows a figure the text lost (a spectrum, a block diagram), transcribe the
figure's numbers into your notes — downstream conclusions often depend on them (e.g. whether a
band is symmetric about the carrier).

## 3. Classify every sub-question with one auditable rule

Two tiers, declared up front in the report:

- **Core (primary)** — the sub-question's principal assessed skill is chapter content; without
  that chapter it cannot be started. Its marks count **in full**, attributed to **exactly one**
  section code.
- **Incidental (support)** — the question's subject belongs to another chapter, but the solution
  requires a chapter result (a variance identity, an independence criterion, a distribution).
  Marks are **not** counted; only "also involves" is recorded.

Rules that keep the table defensible:

- One primary section per sub-question. This is what makes the per-section marks sum correctly.
- Still record secondary sections, so a reader can see a topic's true footprint.
- When torn between two sections, choose the one the student must know **to start** the problem,
  and say so in the methodology note.
- Zero-primary but repeatedly-incidental topics are a real category — call them out separately
  (they behave like preconditions; missing them blocks whole questions).

## 4. Verify the arithmetic before writing any prose

Three checks; state them in the report's methodology section, because they are what make the
numbers auditable:

1. Every paper's sub-question marks sum to that paper's stated total.
2. Sum of all primary marks == sum of the per-paper chapter totals.
3. Answer the "is the chapter important?" question with the per-paper series, not a single number.

Put the arithmetic in the report. A frequency table nobody can re-derive is not evidence.

## 5. Statistics and tiering

- **Headline**: chapter marks per paper, mean, share of the paper, and how many papers devoted a
  whole question to it.
- **Per section**: primary marks total, primary hit count (`k/N`), incidental count, hit rate.
- **Trend**: bar chart of per-paper chapter marks; horizontal bar chart of per-section marks.
  Watch for a jump in the most recent paper — that is the actionable signal.
- **Tiers**: S/A/B from marks and hit count; a separate row for precondition-type topics.
  Weight by marks, not by textbook page order.

## 6. Report structure

1. Cover: scope, sample size, one-paragraph bottom line.
2. Methodology: sources, the two-tier rule, the arithmetic checks, and the limits of the sample.
3. Chapter knowledge map: how the topics are actually examined (standalone question vs. embedded
   tool vs. precondition).
4. Per-paper, per-sub-question tagging table (the audit trail).
5. Frequency table + trend chart + ranking chart + tier table.
6. Gap analysis against the current assignment: what homework already covers, what it misses,
   and what it covers that is never examined.
7. Prioritised revision route + formula quick-reference for the top sections.
8. Appendix: data-source list, verification method, and an explicit statement of limitations.

Always include the limitations section — with a handful of papers, a zero-hit topic is "not yet
examined", not "will not be examined".

## 7. Compile and verify

Start from `assets/report-template.tex` (compilable skeleton) and `assets/report-preamble.tex`
(the same preamble with every known failure mode already fixed), rather than a blank file.

**Project conventions** — the report sources under a workspace convention like this one:

- The `.tex` must be **self-contained** (no `\input`, no external images) so any single file can
  be recompiled on its own.
- Keep deliverables out of the build directory: compile into a scratch directory and copy only
  the PDF back.
- CJK documents need **XeLaTeX**; only pure-ASCII documents can use `pdflatex`.

```sh
xelatex -interaction=nonstopmode -output-directory=tmp/report report.tex   # twice, for TOC/cross-refs
<python> <skill-directory>/scripts/check_tex_pdf.py \
         --log tmp/report/report.log --pdf output/<group>/report.pdf \
         --pages <expected> [--ratio 2048:2732]
cp tmp/report/report.pdf output/<group>/
```

**Require zero overfull `\hbox` and `\vbox`.** Then render pages and read the images to confirm
that tables fit, chart labels do not collide, and no display formula ran into the margin. A
compilation with no error can still be visually broken.

## 8. Downstream study materials

The frequency analysis is the input, not the output. Common follow-ups, all driven by the tiers:

- **Review problem set** — 3 questions/day for the number of days requested; mix exam questions,
  textbook exercises (draw the English wording from the assignment translation if one exists, to
  stay consistent), and formula-recall prompts ("write the definitions of … and derive …").
  Tag each question with its source in parentheses before the statement. One question per page
  with the remaining space left blank for handwriting — implement with tcolorbox `height fill`
  (never combine with `breakable`).
- **Answer key** — continuous computer-reading layout, marking the `§` code and source tag. Do not force one page per answer or reserve handwriting space. State which
  textbook identity each step uses so the reader can go back to the section.
- **Prioritise honestly**: put extra weight on topics the assignment *fails* to drill, and name
  the topics you deliberately omitted (zero marks, not set as homework).

## SSA pagination: writing sheets versus reading documents

All five SSA downstream documents retain portrait **2048:2732** geometry. Aspect ratio does not imply a handwriting layout.

- **Homework booklet and review problem set:** used in Notability on iPad; one question per page with sufficient blank working space. Preserve these pages when fixing a report or answer key.
- **Homework solutions, frequency report and Chinese review solutions:** read on a computer; use continuous content with natural pagination. No per-answer `\clearpage`, `height fill`, or empty working area. Use `\Needspace{8\baselineskip}` before an answer heading so the heading and start of its explanation stay together; allow the rest of a long answer to continue.
- A cover and a deliberate contents/body boundary may start a new page. Do not insert `\clearpage` before every report section or every paper's audit table.
- A source index must be one table, not chunks of 15 rows. Use `xltabular` or `longtable` to break according to actual available space and repeat headers. Short indexes should fit on one page at a readable font size; do not shrink text merely to force a fit. Long audit tables must also be breakable, outside `center`, `minipage`, floats or nonbreakable boxes.
- After compiling, inspect page transitions and bottom whitespace as well as overflow. Zero overfull does not detect unnecessary page breaks. A half-empty reading page followed by more of the same table/section requires inspection of forced breaks, indivisible `tabularx`, box settings and heading spacing. Keep justified cover/contents and unavoidable diagram space distinct from accidental gaps.
- Verify unchanged question counts, sources and mathematics, repeated table headers, complete rows, heading/body attachment, and the 2048:2732 ratio after the fix. Update page counts in the chapter register.

## 9. Matching page geometry to a reading device

When the deliverable is meant to be read or written on a tablet, match the **screen** aspect
ratio, not the device body (bezels would make it wrong by a couple of percent).

1. Get the display resolution (e.g. 13-inch iPad Air M2: 2732×2048 px → portrait 2048:2732).
2. Keep the long edge at a comfortable physical size — A4's 297 mm preserves the vertical layout
   you already verified, so only the width changes.
3. `width = height × Wpx/Hpx`. Example: `297 × 512/683 = 222.6413 mm`.
4. Verify numerically, in pixels: `2048 × height/width` must equal `Hpx`.

A page whose ratio equals the screen fills it with no letterboxing; a mismatched page is scaled
to fit and leaves bars on two sides anyway, so matching costs nothing and gains usable width.

## Pitfalls (all encountered, all reproducible)

| Symptom | Cause | Fix |
|---|---|---|
| Formula or exponent missing from notes | `pdftotext` drops math | render pages, read images |
| `Overfull \hbox (17.0pt too wide)` | `\rule{\textwidth}` or `tabularx` starting a paragraph picks up `\parindent` (17pt at 11pt) | `\noindent` before it |
| pgfplots: "input coordinate … has not been defined" | numeric reference line on a `symbolic x coords` axis | draw with `axis description cs` |
| `! LaTeX Error: Command \Bbbk already defined` | `newtxmath` together with `amssymb` | load `amsmath` only, before `newtxmath` |
| `! Undefined control sequence \rowcolor` | `xcolor` without the `table` option | `\usepackage[table]{xcolor}` |
| `Package enumitem Error: Undefined label` | `\newlist{x}{itemize}{1}` with no `label=` | pass `label=\textbullet` |
| Long display formula in the margin | single unbreakable line | break it in `aligned`/`multline` |
| Chinese renders as blank/absent | document class is not CJK-aware | `ctexart` + `xelatex` |
| `Font TU/STFangsong ... not loadable`; Chinese inside `\texttt` turns to mojibake | in a **ctex** document `newtxtext` breaks ctex's CJK-monospace mapping, so ctex falls back to the `macold` fontset whose 仿宋/STFangsong font current macOS no longer ships | **drop `newtxtext`** in CJK documents and keep `newtxmath` (verified harmless). `\setCJKmonofont` does *not* fix it. Pure-ASCII documents may keep `newtxtext` |
| Page ratio still slightly off | rounding in mm | compute the width from the full-precision ratio and re-check in pixels |

## Regression checklist

- [ ] Taxonomy codes come from the textbook's TOC, not invented.
- [ ] Every formula and mark value confirmed against a rendered page image.
- [ ] Each sub-question has exactly one primary section.
- [ ] Per-paper marks sum to each paper's total; primary totals cross-check.
- [ ] Tiers assigned by marks and hit count; preconditions called out separately.
- [ ] Gap analysis names both directions (missed by homework / covered but never examined).
- [ ] `check_tex_pdf.py` reports 0 overfull boxes and the expected page count.
- [ ] Pages rendered and visually inspected (tables, charts, formulas, page transitions and unexplained blank space).
- [ ] SSA writing sheets retain one question per page; reading documents paginate naturally; indexes are not split by a fixed row count.
- [ ] Limitations section present and specific.
