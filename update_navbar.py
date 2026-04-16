"""
update_navbar.py
Adds consistent navbar elements to all AllCalculate pages:
  1. nav-center (tagline + stats) on every page that lacks it
  2. nav-auth div (Sign In button) on every page that lacks it
  3. firebase-auth.js script tag before </body> on every page that lacks it

Skips: simple-calculator.html (has its own inline Firebase auth)
"""

import os, re

HTML_DIR = r"C:\Projects\AllCalculate"

# Pages with inline Firebase — do NOT add firebase-auth.js to these
SKIP_FIREBASE_SCRIPT = {"simple-calculator.html"}

NAV_CENTER = """\
      <div class="nav-center">
        <div class="nav-center-title">Free Online Calculators for Every Need</div>
        <div class="nav-center-stats">
          <span class="nav-center-stat"><strong>20+</strong> Calculators</span>
          <span class="nav-center-stat"><strong>100%</strong> Free Forever</span>
          <span class="nav-center-stat"><strong>Fast</strong> Instant Results</span>
        </div>
      </div>
"""

NAV_AUTH = """\
      <div class="nav-auth" id="navAuth">
        <button class="nav-signin-btn" id="navSignInBtn">Sign In</button>
      </div>
"""

FIREBASE_SCRIPT = '  <script type="module" src="firebase-auth.js"></script>\n'

files = [f for f in os.listdir(HTML_DIR) if f.endswith(".html")]
files.sort()

changed = []

for fname in files:
    path = os.path.join(HTML_DIR, fname)
    with open(path, "r", encoding="utf-8") as fh:
        html = fh.read()

    original = html
    modified = False

    # ── 1. Add nav-center if missing ──
    if 'class="nav-center"' not in html:
        # Insert nav-center after the nav-logo anchor, before nav-links or nav-toggle
        # Pattern: </a> followed by whitespace then <ul class="nav-links" or <button class="nav-toggle"
        pattern = r'(</a>\s*\n)(\s*<(?:ul class="nav-links"|button class="nav-toggle"))'
        replacement = r'\1' + NAV_CENTER + r'\2'
        new_html = re.sub(pattern, replacement, html, count=1)
        if new_html != html:
            html = new_html
            modified = True
            print(f"  [nav-center added]  {fname}")
        else:
            print(f"  [nav-center SKIP - pattern not found] {fname}")

    # ── 2. Add nav-auth if missing ──
    if 'id="navAuth"' not in html:
        # Insert nav-auth before <button class="nav-toggle"
        pattern = r'(\s*)(<button class="nav-toggle")'
        replacement = '\n' + NAV_AUTH + r'\1\2'
        new_html = re.sub(pattern, replacement, html, count=1)
        if new_html != html:
            html = new_html
            modified = True
            print(f"  [nav-auth added]    {fname}")
        else:
            print(f"  [nav-auth SKIP - pattern not found] {fname}")

    # ── 3. Add firebase-auth.js script if missing ──
    if fname not in SKIP_FIREBASE_SCRIPT:
        if 'firebase-auth.js' not in html:
            html = html.replace('</body>', FIREBASE_SCRIPT + '</body>', 1)
            modified = True
            print(f"  [firebase-auth.js]  {fname}")

    if modified:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(html)
        changed.append(fname)

print(f"\nDone. Updated {len(changed)} files:")
for f in changed:
    print(f"  {f}")
