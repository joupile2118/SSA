#!/usr/bin/env python3
"""Compile and structurally check a self-contained English SSA homework/solution.
Requires XeLaTeX, pdftotext, and (with --render) pdftoppm on PATH.
Does not check mathematics or replace visual PDF review.
"""
import argparse
from pathlib import Path
import re
import shutil
import subprocess
import sys


def run(args):
    result = subprocess.run(args, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if result.returncode:
        raise RuntimeError(f'{args[0]} failed:\n{result.stdout[-6000:]}')
    return result.stdout


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--tex', type=Path, required=True)
    p.add_argument('--required', required=True, help='Comma-separated exercise IDs, in order; empty string allowed')
    p.add_argument('--optional', default='', help='Comma-separated exercise IDs, in order')
    p.add_argument('--build-dir', type=Path, required=True)
    p.add_argument('--issued')
    p.add_argument('--due')
    p.add_argument('--render', action='store_true')
    p.add_argument('--layout', choices=('auto','writing','reading'), default='auto', help='Writing: one exercise per page; reading: continuous solutions. Auto detects Solutions filename.')
    a = p.parse_args()
    src, build = a.tex.resolve(), a.build_dir.resolve()
    if build == src.parent or build.is_relative_to(src.parent):
        raise ValueError('Build into tmp/, not the deliverable directory.')
    if 'tmp' not in build.parts:
        raise ValueError('Choose a build directory under tmp/.')
    ids = lambda value: [v.strip() for v in value.split(',') if v.strip()]
    required, optional = ids(a.required), ids(a.optional)
    expected = required + optional
    if not expected or len(set(expected)) != len(expected):
        raise ValueError('Exercise list must be nonempty and have no duplicates.')
    if not all(re.fullmatch(r'\d+\.\d+', item) for item in expected):
        raise ValueError('Exercise IDs must have chapter.number form.')
    raw = src.read_text()
    text = re.sub(r'(?<!\\)%[^\n]*', '', raw)
    if re.search(r'\\(?:input|include|includegraphics|includepdf|externaldocument|bibliography|addbibresource)\b', text):
        raise ValueError('Final TeX must be self-contained: external content dependency found.')
    entries = re.findall(r'\\problem\{([^}]+)\}\{([^}]+)\}\{([^}]+)\}', text)
    if [e[0] for e in entries] != expected:
        raise ValueError(f'Source exercise order differs: {[e[0] for e in entries]} != {expected}')
    labels = ['Required'] * len(required) + ['Optional'] * len(optional)
    if [e[1] for e in entries] != labels:
        raise ValueError('Source Required/Optional labels differ from requested groups.')
    build.mkdir(parents=True, exist_ok=True)
    engine = shutil.which('xelatex')
    if not engine:
        engine = '/Library/TeX/texbin/xelatex'
    for _ in range(2):
        run([engine, '-interaction=nonstopmode', '-halt-on-error', f'-output-directory={build}', str(src)])
    log = (build / f'{src.stem}.log').read_text(errors='replace')
    bad = re.findall(r'^.*(?:Overfull \\[hv]box|Missing character|undefined|Rerun to|Label\(s\) may have changed).*$','\n'.join(log.splitlines()), re.M)
    if bad:
        raise ValueError('TeX checks failed:\n' + '\n'.join(bad))
    pdf = build / f'{src.stem}.pdf'
    extracted = run(['pdftotext', '-layout', str(pdf), '-'])
    pages = [page for page in extracted.split('\f') if page.strip()]
    layout = a.layout if a.layout != 'auto' else ('reading' if 'Solutions' in src.stem else 'writing')
    headings = re.findall(r'Exercise\s+(\d+\.\d+)', extracted)
    if headings != expected:
        raise ValueError(f'PDF exercise order differs: {headings} != {expected}')
    if layout == 'writing':
        if len(pages) != len(expected):
            raise ValueError(f'Expected {len(expected)} writing pages, found {len(pages)}.')
        for i, (page, exercise, label) in enumerate(zip(pages, expected, labels), 1):
            if re.findall(r'Exercise\s+(\d+\.\d+)', page) != [exercise]:
                raise ValueError(f'Page {i}: missing/extra exercise heading.')
            if not re.search(r'\b' + label + r'\b', page):
                raise ValueError(f'Page {i}: wrong group label.')
            for date in (a.issued, a.due):
                if date and date not in page:
                    raise ValueError(f'Page {i}: expected date {date!r}.')
    else:
        segments = re.split(r'Exercise\s+\d+\.\d+', extracted)[1:]
        for exercise, label, segment in zip(expected, labels, segments):
            if not re.search(r'\b' + label + r'\b', segment):
                raise ValueError(f'Exercise {exercise}: wrong group label.')
    info = run(['pdfinfo', str(pdf)])
    size = re.search(r'Page size:\s+([\d.]+) x ([\d.]+)', info)
    if not size or abs(float(size[1])/float(size[2])/(2048/2732)-1) > 1e-4:
        raise ValueError('Expected portrait 2048:2732 page ratio.')
    if a.render:
        run(['pdftoppm', '-scale-to', '1400', '-png', str(pdf), str(build / (src.stem + '-page'))])
    target = src.with_suffix('.pdf')
    shutil.copy2(pdf, target)
    print(f'PASS: {len(pages)} pages, {layout} layout, correct exercise order/groups, 2048:2732 ratio, self-contained source, no overfull/missing glyphs/unresolved references.')
    print(f'PDF: {target}')
    print('Mathematical verification and visual review are still required.')


if __name__ == '__main__':
    try:
        main()
    except (ValueError, RuntimeError, OSError) as e:
        print(f'FAIL: {e}', file=sys.stderr)
        sys.exit(1)
