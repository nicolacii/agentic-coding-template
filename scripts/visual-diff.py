"""
Visual Regression Diff — automated pixel-perfect comparison.

Usage:
  python3 scripts/visual-diff.py [page]

Configure REFERENCE_BASE, CURRENT_BASE, and PAGES below for your project.
Output: test-results/visual-diff/{page}_reference.png, {page}_current.png, {page}_diff.png

Requires:
  pip install playwright && playwright install chromium
  npm install -D pixelmatch pngjs
"""

import sys
import os
import subprocess
import json
from playwright.sync_api import sync_playwright

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
OUTPUT_DIR = os.path.join(PROJECT_DIR, "test-results", "visual-diff")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ═══════════════════════════════════════════════════════
# CONFIGURE FOR YOUR PROJECT
# ═══════════════════════════════════════════════════════

REFERENCE_BASE = "https://your-production-site.com"  # Old/reference project
CURRENT_BASE = "http://localhost:3000"                 # New/dev project

# Credentials for login (if needed)
CREDENTIALS = [
    ("user@example.com", "password"),
]

# Pages to compare
PAGES = {
    "login": {
        "path": "/login",
        "login_required": False,
        "viewport": {"width": 1440, "height": 900},
    },
    "dashboard": {
        "path": "/dashboard",
        "login_required": True,
        "viewport": {"width": 1440, "height": 900},
    },
    # Add more pages:
    # "profile": { "path": "/profile", "login_required": True, "viewport": {"width": 1440, "height": 900} },
}

# ═══════════════════════════════════════════════════════

def login(page, base_url):
    """Try to login with configured credentials."""
    page.goto(base_url, wait_until="networkidle")
    page.wait_for_timeout(2000)

    for email, password in CREDENTIALS:
        if "login" not in page.url.lower() and "auth" not in page.url.lower():
            return True

        email_input = page.locator('input[type="text"], input[type="email"], input[placeholder*="mail"]').first
        if email_input.is_visible():
            email_input.fill("")
            page.keyboard.type(email, delay=30)

        pass_input = page.locator('input[type="password"]').first
        if pass_input.is_visible():
            pass_input.click()
            page.keyboard.type(password, delay=30)

        submit = page.locator('button[type="submit"], button:has-text("Sign in"), button:has-text("Log in")').first
        if submit.is_visible():
            submit.click()

        page.wait_for_timeout(5000)
        page.wait_for_load_state("networkidle")

        if "login" not in page.url.lower() and "auth" not in page.url.lower():
            print(f"  Logged in as {email}")
            return True

        page.goto(base_url, wait_until="networkidle")
        page.wait_for_timeout(2000)

    print("  WARNING: Login failed")
    return False


def take_screenshot(page, base_url, config, output_path, label):
    """Navigate and screenshot."""
    if config["login_required"]:
        if not login(page, base_url):
            print(f"  Skipping {label} — login failed")
            return False

    url = base_url + config["path"]
    print(f"  Navigating to {url}")
    page.goto(url, wait_until="networkidle")
    page.wait_for_timeout(3000)
    page.screenshot(path=output_path, full_page=True)
    print(f"  Saved: {output_path}")
    return True


def pixel_diff(ref_path, cur_path, diff_path):
    """Compute pixel diff via Node.js + pixelmatch."""
    node_script = f"""
const fs = require('fs');
const {{ PNG }} = require('pngjs');
async function main() {{
const pixelmatch = (await import('pixelmatch')).default;
const img1 = PNG.sync.read(fs.readFileSync('{ref_path}'));
const img2 = PNG.sync.read(fs.readFileSync('{cur_path}'));
const width = Math.min(img1.width, img2.width);
const height = Math.min(img1.height, img2.height);
function crop(img, w, h) {{
    const out = new Uint8Array(w * h * 4);
    for (let y = 0; y < h; y++)
        for (let x = 0; x < w; x++) {{
            const si = (y * img.width + x) * 4, di = (y * w + x) * 4;
            out[di]=img.data[si]; out[di+1]=img.data[si+1]; out[di+2]=img.data[si+2]; out[di+3]=img.data[si+3];
        }}
    return out;
}}
const d1 = crop(img1, width, height), d2 = crop(img2, width, height);
const diff = new PNG({{width, height}});
const n = pixelmatch(d1, d2, diff.data, width, height, {{ threshold: 0.1, includeAA: false }});
fs.writeFileSync('{diff_path}', PNG.sync.write(diff));
console.log(JSON.stringify({{ width, height, diffPixels: n, totalPixels: width*height, diffPercent: parseFloat(((n/(width*height))*100).toFixed(2)), sizeMismatch: img1.width!==img2.width||img1.height!==img2.height, refSize:[img1.width,img1.height], curSize:[img2.width,img2.height] }}));
}}
main();
"""
    result = subprocess.run(["node", "-e", node_script], capture_output=True, text=True, cwd=PROJECT_DIR, timeout=30)
    if result.returncode != 0:
        print(f"  pixelmatch error: {result.stderr[:200]}")
        return None
    return json.loads(result.stdout.strip())


def run_diff(page_name):
    config = PAGES.get(page_name)
    if not config:
        print(f"Unknown page: {page_name}. Available: {', '.join(PAGES.keys())}")
        return

    ref_path = os.path.join(OUTPUT_DIR, f"{page_name}_reference.png")
    cur_path = os.path.join(OUTPUT_DIR, f"{page_name}_current.png")
    diff_path = os.path.join(OUTPUT_DIR, f"{page_name}_diff.png")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        print(f"\n[1/3] Reference ({REFERENCE_BASE})...")
        pg = browser.new_page(viewport=config["viewport"], device_scale_factor=2)
        ref_ok = take_screenshot(pg, REFERENCE_BASE, config, ref_path, "reference")
        pg.close()

        if not ref_ok:
            browser.close()
            return

        print(f"\n[2/3] Current ({CURRENT_BASE})...")
        pg = browser.new_page(viewport=config["viewport"], device_scale_factor=2)
        cur_ok = take_screenshot(pg, CURRENT_BASE, config, cur_path, "current")
        pg.close()
        browser.close()

        if not cur_ok:
            return

    print(f"\n[3/3] Pixel diff...")
    result = pixel_diff(ref_path, cur_path, diff_path)

    if result:
        status = "✅ PASS" if result["diffPercent"] < 1 else "❌ FAIL"
        print(f"\n{'='*50}")
        print(f"  Page: {page_name}")
        print(f"  Ref: {result['refSize'][0]}×{result['refSize'][1]}")
        print(f"  Cur: {result['curSize'][0]}×{result['curSize'][1]}")
        print(f"  Diff: {result['diffPercent']}% ({result['diffPixels']:,} px)")
        print(f"  {status} (threshold: 1%)")
        print(f"  Diff image: {diff_path}")
        print(f"{'='*50}")


if __name__ == "__main__":
    page = sys.argv[1] if len(sys.argv) > 1 else "login"
    run_diff(page)
