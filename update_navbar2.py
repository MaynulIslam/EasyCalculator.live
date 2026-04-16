"""
update_navbar2.py
For every AllCalculate HTML page:
  1. Remove the nav-center div (tagline + stats) from the navbar
  2. Wrap nav-logo text in .nav-logo-content + add .nav-logo-tagline below it
  3. Add .footer-stats block inside .footer-brand (after the <p> tag)
"""

import os, re

HTML_DIR = r"C:\Projects\AllCalculate"

# ── Snippets ──────────────────────────────────────────────────
NEW_LOGO = '''\
<a href="index.html" class="nav-logo">
        <div class="nav-logo-content">
          <span class="nav-logo-text">All<span>Calculate</span></span>
          <div class="nav-logo-tagline">Free Online Calculators for Every Need</div>
        </div>
      </a>'''

FOOTER_STATS = '''\
        <div class="footer-stats">
          <span class="footer-stat"><strong>20+</strong> Calculators</span>
          <span class="footer-stat"><strong>100%</strong> Free Forever</span>
          <span class="footer-stat"><strong>Fast</strong> Instant Results</span>
        </div>'''

files = sorted(f for f in os.listdir(HTML_DIR) if f.endswith(".html"))
changed = []

for fname in files:
    path = os.path.join(HTML_DIR, fname)
    with open(path, "r", encoding="utf-8") as fh:
        html = fh.read()

    original = html

    # ── 1. Remove nav-center block ──────────────────────────────
    html = re.sub(
        r'\s*<div class="nav-center">[\s\S]*?</div>\s*</div>\s*\n',
        '\n',
        html
    )

    # ── 2. Replace plain nav-logo anchor with tagline version ──
    # Only do this if tagline not already present
    if 'nav-logo-tagline' not in html:
        html = re.sub(
            r'<a href="index\.html" class="nav-logo">'
            r'<span class="nav-logo-text">All<span>Calculate</span></span>'
            r'</a>',
            NEW_LOGO,
            html
        )

    # ── 3. Add footer-stats after footer-brand <p> if missing ──
    if 'footer-stats' not in html:
        # Find the closing </p> inside footer-brand and insert after it
        html = re.sub(
            r'(<div class="footer-brand">[\s\S]*?<p>[^<]*</p>)',
            r'\1\n' + FOOTER_STATS,
            html,
            count=1
        )

    if html != original:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(html)
        changed.append(fname)
        print(f"  updated: {fname}")
    else:
        print(f"  no change: {fname}")

print(f"\nDone. Updated {len(changed)} files.")
