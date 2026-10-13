#!/usr/bin/env python3
"""Verify a LaTeX->PDF deliverable the way the exam-frequency-report skill requires.

Checks, in order of what actually goes wrong:

  1. Overfull boxes in the LaTeX log.  The skill mandates zero.  A build can
     finish with exit code 0 and still have tables and formulas running into the
     margin, so this is a hard gate, not a warning.
  2. Page count, optionally asserted.
  3. Page size and aspect ratio, optionally asserted against a device screen.

Stdlib only: no PyPDF, no poppler required.  If `pdfinfo` happens to be on PATH
it is preferred for page size (authoritative); otherwise the MediaBox is read
straight out of the PDF bytes.

Usage
-----
  check_tex_pdf.py --log report.log --pdf report.pdf --pages 23
  check_tex_pdf.py --log report.log --pdf report.pdf --ratio 2048:2732
  check_tex_pdf.py --log report.log --json

Exit status: 0 if every requested check passes, 1 otherwise.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

# ---------------------------------------------------------------- log checks

OVERFULL_RE = re.compile(r"Overfull \\([hv])box \(([0-9.]+)pt too (?:wide|high)\)")
LOCATION_RE = re.compile(r"^(?:l\.(\d+)|.*?at line (\d+)|.*?lines (\d+)--(\d+))")
UNDERFULL_RE = re.compile(r"Underfull \\([hv])box")
LATEX_ERROR_RE = re.compile(r"^! (.+)$", re.MULTILINE)


def check_log(path: Path) -> dict:
    text = path.read_text(errors="replace")
    lines = text.splitlines()

    overfull = []
    for idx, line in enumerate(lines):
        m = OVERFULL_RE.search(line)
        if not m:
            continue
        where = ""
        # the offending source location is usually on the same or next line
        for probe in (line, lines[idx + 1] if idx + 1 < len(lines) else ""):
            loc = LOCATION_RE.search(probe.strip())
            if loc:
                where = next((g for g in loc.groups() if g), "")
                break
        overfull.append(
            {
                "kind": m.group(1),          # 'h' or 'v'
                "pt": float(m.group(2)),
                "line": where,
            }
        )

    underfull = len(UNDERFULL_RE.findall(text))
    errors = LATEX_ERROR_RE.findall(text)

    return {
        "overfull": overfull,
        "overfull_hbox": sum(1 for o in overfull if o["kind"] == "h"),
        "overfull_vbox": sum(1 for o in overfull if o["kind"] == "v"),
        "underfull": underfull,
        "errors": errors,
    }


# ---------------------------------------------------------------- pdf checks

MEDIABOX_RE = re.compile(
    rb"/MediaBox\s*\[\s*([0-9.+-]+)\s+([0-9.+-]+)\s+([0-9.+-]+)\s+([0-9.+-]+)\s*\]"
)
COUNT_RE = re.compile(rb"/Type\s*/Pages\b[^>]*?/Count\s+(\d+)", re.DOTALL)
PAGE_RE = re.compile(rb"/Type\s*/Page(?![s/\w])")


def check_pdf(path: Path) -> dict:
    info: dict = {"source": None, "pages": None, "width_pt": None, "height_pt": None}

    if shutil.which("pdfinfo"):
        try:
            out = subprocess.run(
                ["pdfinfo", str(path)], capture_output=True, text=True, timeout=30
            ).stdout
            pages = re.search(r"^Pages:\s+(\d+)", out, re.MULTILINE)
            size = re.search(
                r"^Page size:\s+([0-9.]+)\s+x\s+([0-9.]+)\s+pts", out, re.MULTILINE
            )
            if pages:
                info["pages"] = int(pages.group(1))
                info["source"] = "pdfinfo"
            if size:
                info["width_pt"] = float(size.group(1))
                info["height_pt"] = float(size.group(2))
                info["source"] = "pdfinfo"
            if info["pages"] and info["width_pt"]:
                return info
        except (OSError, subprocess.SubprocessError):
            pass  # fall through to byte parsing

    data = path.read_bytes()
    box = MEDIABOX_RE.search(data)
    if box:
        x0, y0, x1, y1 = (float(v) for v in box.groups())
        info["width_pt"] = abs(x1 - x0)
        info["height_pt"] = abs(y1 - y0)
    if info["pages"] is None:
        count = COUNT_RE.search(data)
        info["pages"] = int(count.group(1)) if count else len(PAGE_RE.findall(data))
    info["source"] = info["source"] or "pdf-bytes"
    return info


# ---------------------------------------------------------------- main

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--log", type=Path, help="LaTeX .log file to scan for overfull boxes")
    ap.add_argument("--pdf", type=Path, help="compiled PDF to measure")
    ap.add_argument("--pages", type=int, help="assert this exact page count")
    ap.add_argument(
        "--ratio",
        metavar="W:H",
        help="assert the page aspect ratio matches a screen, e.g. 2048:2732 "
        "(13-inch iPad Air M2 portrait). The pixel error at width W is reported.",
    )
    ap.add_argument("--allow-overfull", type=int, default=0,
                    help="tolerated overfull box count (default 0)")
    ap.add_argument("--json", action="store_true", help="emit machine-readable output")
    args = ap.parse_args()

    if not args.log and not args.pdf:
        ap.error("pass at least one of --log or --pdf")

    result: dict = {"ok": True, "failures": []}

    # ---- log
    if args.log:
        if not args.log.is_file():
            print(f"error: log not found: {args.log}", file=sys.stderr)
            return 1
        lg = check_log(args.log)
        result["log"] = lg
        total = lg["overfull_hbox"] + lg["overfull_vbox"]
        if total > args.allow_overfull:
            result["ok"] = False
            result["failures"].append(
                f"{total} overfull box(es): "
                f"{lg['overfull_hbox']} hbox, {lg['overfull_vbox']} vbox"
            )
        if lg["errors"]:
            result["ok"] = False
            result["failures"].append(f"{len(lg['errors'])} LaTeX error(s)")

    # ---- pdf
    if args.pdf:
        if not args.pdf.is_file():
            print(f"error: pdf not found: {args.pdf}", file=sys.stderr)
            return 1
        pdf = check_pdf(args.pdf)
        result["pdf"] = pdf

        if pdf["pages"] is None:
            result["ok"] = False
            result["failures"].append("could not determine page count")
        elif args.pages is not None and pdf["pages"] != args.pages:
            result["ok"] = False
            result["failures"].append(
                f"page count {pdf['pages']} != expected {args.pages}"
            )

        if args.ratio:
            if not (pdf["width_pt"] and pdf["height_pt"]):
                result["ok"] = False
                result["failures"].append("could not determine page size for --ratio")
            else:
                m = re.fullmatch(r"\s*(\d+)\s*:\s*(\d+)\s*", args.ratio)
                if not m:
                    ap.error("--ratio must look like W:H, e.g. 2048:2732")
                want_w, want_h = int(m.group(1)), int(m.group(2))
                got = pdf["width_pt"] / pdf["height_pt"]
                want = want_w / want_h
                rel = abs(got - want) / want
                px_err = want_w * rel
                result["ratio"] = {
                    "target": f"{want_w}:{want_h}",
                    "page_ratio": round(got, 8),
                    "target_ratio": round(want, 8),
                    "relative_error": rel,
                    "pixel_error_at_target_width": px_err,
                }
                # half a pixel is exact enough for any screen
                if px_err > 0.5:
                    result["ok"] = False
                    result["failures"].append(
                        f"aspect ratio off by {px_err:.2f} px at width {want_w}"
                    )

    # ---- report
    if args.json:
        print(json.dumps(result, indent=2))
        return 0 if result["ok"] else 1

    def line(label: str, value: str) -> None:
        print(f"  {label:<26} {value}")

    print("check_tex_pdf")
    if "log" in result:
        lg = result["log"]
        print(f"\nLOG  {args.log}")
        line("overfull hbox", str(lg["overfull_hbox"]))
        line("overfull vbox", str(lg["overfull_vbox"]))
        line("underfull (informational)", str(lg["underfull"]))
        line("latex errors", str(len(lg["errors"])))
        for o in lg["overfull"][:15]:
            where = f" (line {o['line']})" if o["line"] else ""
            print(f"      - {o['pt']:.1f}pt too wide [{o['kind']}box]{where}")
        if len(lg["overfull"]) > 15:
            print(f"      ... and {len(lg['overfull']) - 15} more")
        for e in lg["errors"][:5]:
            print(f"      ! {e}")

    if "pdf" in result:
        pdf = result["pdf"]
        print(f"\nPDF  {args.pdf}")
        line("page count", str(pdf["pages"]))
        if pdf["width_pt"]:
            line("page size", f"{pdf['width_pt']:.3f} x {pdf['height_pt']:.3f} pt")
            line("aspect ratio", f"{pdf['width_pt'] / pdf['height_pt']:.8f}")
        line("measured via", str(pdf["source"]))

    if "ratio" in result:
        r = result["ratio"]
        print("\nRATIO")
        line("target", r["target"])
        line("page ratio", f"{r['page_ratio']:.8f}")
        line("target ratio", f"{r['target_ratio']:.8f}")
        line("pixel error", f"{r['pixel_error_at_target_width']:.4f} px")

    print()
    if result["ok"]:
        print("PASS")
        return 0
    print("FAIL")
    for f in result["failures"]:
        print(f"  - {f}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
