---
name: visual-diff
user-invocable: true
description: Automated visual regression testing with pixel-perfect comparison. Use when implementing or fixing CSS/SCSS to match a reference design (old project, Figma). Triggers on visual work, CSS fixes, "pixel-perfect", "visual match", "screenshot comparison", or any task where the goal is to make the new UI match a reference UI. Runs a loop: screenshot → pixelmatch diff → read diff image → fix CSS → repeat until diff < 1%.
---

# Visual Diff — Automated Pixel-Perfect Loop

## Workflow

```
1. Take REFERENCE screenshot (old project / production)
2. Take CURRENT screenshot (new project / localhost)
3. pixelmatch computes diff → diff image + diff %
4. Read diff image → red pixels = exact CSS problems
5. Fix CSS based on red zones
6. Repeat until diff < 1%
```

## Usage

```bash
# From project root:
python3 scripts/visual-diff.py <page>

# Available pages: login, dashboard, constructor, history
# Output: test-results/visual-diff/{page}_reference.png, {page}_current.png, {page}_diff.png
```

## Reading the Diff Image

The diff image highlights mismatched pixels in **red**. Use it to identify:
- **Large red blocks** = missing elements (OAuth buttons, icons, entire sections)
- **Red outlines** = wrong border-radius, padding, margin
- **Red text overlay** = font mismatch (size, weight, family, locale)
- **Thin red lines** = 1-2px shifts in positioning

## Iteration Protocol

1. Run `python3 scripts/visual-diff.py {page}`
2. Read the diff image with the Read tool
3. List each red zone and what CSS property causes it
4. Fix the CSS/SCSS
5. Run diff again
6. Compare diff % — it should decrease each iteration
7. Stop when diff < 1% OR when remaining diff is non-CSS (locale, data, CDN images)

## Key Rules

- **NEVER guess** what the problem is — always read the diff image first
- **Fix one category at a time** (layout → colors → typography → icons)
- **Log each iteration**: iteration number, diff %, what was fixed
- **Acceptable residual diff**: locale differences (logo language, switcher text), dynamic data, CDN images — these are NOT CSS problems

## Prerequisites

- `npm install -D pixelmatch pngjs` (in project)
- `pip install playwright` + `playwright install chromium`
- Dev server running on localhost:3000
- Reference site accessible (e.g. new-test.albato.ru)

## Adding New Pages

Edit `scripts/visual-diff.py` → `PAGES` dict:

```python
PAGES = {
    "my-page": {
        "path": "/my/path",
        "login_required": True,
        "viewport": {"width": 1440, "height": 900},
    },
}
```

## Proven Results

Login page: 5.12% → 2.72% → 2.75% (3 iterations). Remaining diff = locale text differences, not CSS.
