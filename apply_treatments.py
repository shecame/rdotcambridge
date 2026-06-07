#!/usr/bin/env python3
"""Apply visual treatments, remove progress bars, add icons + metrics to all case study pages."""

import re, os, shutil

GIT = '/Users/rashetdacambridge/Documents/Git'
TMP = '/private/tmp'

# ── SVG icons ────────────────────────────────────────────────────────────────
def svg(d, extra=''):
    return f'<svg class="si" xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"{extra}>{d}</svg> '

ICONS = {
    'Overview':           svg('<circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>'),
    'Research':           svg('<circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>'),
    'Approach':           svg('<polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/>'),
    'Strategy':           svg('<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>'),
    'Solution':           svg('<polyline points="20 6 9 17 4 12"/>'),
    'Outcomes':           svg('<polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/>'),
    'Outcome':            svg('<polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/>'),
    'Brand':              svg('<polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>'),
    'Product':            svg('<rect x="2" y="3" width="20" height="14" rx="2" ry="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/>'),
    'Campaign':           svg('<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.93 12 19.79 19.79 0 0 1 1.85 3.43 2 2 0 0 1 3.83 1h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9c1.82 3.13 4.27 5.73 7.11 7.55l1.36-1.25a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>'),
    'Structure':          svg('<line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/><line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/>'),
    'Design':             svg('<circle cx="12" cy="12" r="3"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14M4.93 4.93a10 10 0 0 0 0 14.14"/>'),
    'Design Foundation':  svg('<polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/>'),
    'Interface Architecture': svg('<rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/>'),
    'Feature Design':     svg('<circle cx="12" cy="12" r="3"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14M4.93 4.93a10 10 0 0 0 0 14.14"/>'),
    'Impact & Outcomes':  svg('<polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/>'),
    'Reflection':         svg('<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>'),
    'Problem Statement':  svg('<circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>'),
    'The Approach':       svg('<polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/>'),
    'Who Was in the System': svg('<circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/>'),
    'What We Found':      svg('<circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>'),
    'Process Map':        svg('<line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/>'),
    'The Recommendation': svg('<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>'),
    'Design Work':        svg('<circle cx="12" cy="12" r="3"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14M4.93 4.93a10 10 0 0 0 0 14.14"/>'),
    'Brand System':       svg('<polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>'),
    'Product Design':     svg('<rect x="2" y="3" width="20" height="14" rx="2" ry="2"/><line x1="8" y1="21" x2="16" y2="21"/>'),
    'Leading a Global Team': svg('<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>'),
}

# ── Page-specific style blocks ────────────────────────────────────────────────
TREATMENTS = {
    'att-casestudy-rdot.html': """
<style>
.si{display:inline-block;vertical-align:middle;margin-right:6px;margin-top:-2px;color:currentColor}
:root{--page-accent:#004E7C}
.section-label{color:var(--page-accent)}
.dark-band .section-label,.findings-section .section-label{color:var(--yellow)}
.hero{background:linear-gradient(145deg,#080C14 55%,#0B1A2C 100%)}
.blockquote-pull{border-left-color:var(--page-accent)}
.pull-quote{border-left-color:var(--page-accent)}
</style>""",

    'boa-flagscape-casestudy-rdot.html': """
<style>
.si{display:inline-block;vertical-align:middle;margin-right:6px;margin-top:-2px;color:currentColor}
:root{--page-accent:#005080}
.section-label{color:var(--page-accent)}
.dark-band .section-label,.findings-section .section-label{color:var(--yellow)}
.hero{background:linear-gradient(145deg,#080C12 55%,#0A1522 100%)}
.blockquote-pull{border-left-color:var(--page-accent)}
.pull-quote{border-left-color:var(--page-accent)}
</style>""",

    'btki-casestudy-rdot.html': """
<style>
.si{display:inline-block;vertical-align:middle;margin-right:6px;margin-top:-2px;color:currentColor}
:root{--page-accent:#5A5A5A}
.section-label{color:var(--page-accent);letter-spacing:0.22em}
.dark-band .section-label,.findings-section .section-label{color:var(--yellow)}
.hero{background:#0C0C0C}
.blockquote-pull{border-left-color:var(--yellow)}
.pull-quote{border-left-color:var(--yellow)}
</style>""",

    'ctrax-casestudy-rdot.html': """
<style>
.si{display:inline-block;vertical-align:middle;margin-right:6px;margin-top:-2px;color:currentColor}
:root{--page-accent:#1B5E35}
.section-label{color:var(--page-accent)}
.dark-band .section-label,.findings-section .section-label{color:var(--yellow)}
.hero{background:linear-gradient(145deg,#070E07 55%,#0A180A 100%)}
.blockquote-pull{border-left-color:var(--page-accent)}
.pull-quote{border-left-color:var(--page-accent)}
</style>""",

    'ehe-casestudy-rdot.html': """
<style>
.si{display:inline-block;vertical-align:middle;margin-right:6px;margin-top:-2px;color:currentColor}
:root{--page-accent:#1A6B44}
.section-label{color:var(--page-accent)}
.dark-band .section-label,.findings-section .section-label{color:var(--yellow)}
.hero{background:linear-gradient(145deg,#060C09 55%,#091A10 100%)}
.blockquote-pull{border-left-color:var(--page-accent)}
.pull-quote{border-left-color:var(--page-accent)}
</style>""",

    'goosehead-casestudy-rdot.html': """
<style>
.si{display:inline-block;vertical-align:middle;margin-right:6px;margin-top:-2px;color:currentColor}
:root{--page-accent:#7B5E1A}
.section-label{color:var(--page-accent)}
.dark-band .section-label,.findings-section .section-label{color:var(--yellow)}
.hero{background:linear-gradient(145deg,#0C0A06 55%,#1A1408 100%)}
.blockquote-pull{border-left-color:var(--page-accent)}
.pull-quote{border-left-color:var(--page-accent)}
</style>""",

    # Existing pages — only add .si rule + accent tweak, keep their existing treatments
    'andela-casestudy-rdot.html': """
<style>
.si{display:inline-block;vertical-align:middle;margin-right:6px;margin-top:-2px;color:currentColor}
</style>""",

    'boa-casestudy-rdot.html': """
<style>
.si{display:inline-block;vertical-align:middle;margin-right:6px;margin-top:-2px;color:currentColor}
</style>""",

    'platinum-case-study_1.html': """
<style>
.si{display:inline-block;vertical-align:middle;margin-right:6px;margin-top:-2px;color:currentColor}
</style>""",
}

# ── Stats row HTML ─────────────────────────────────────────────────────────────
STATS_ROW_ATT = """
    <div class="stats-row fade-up" style="display:flex;gap:0;margin:40px 0;border-top:1px solid var(--border);border-bottom:1px solid var(--border);padding:32px 0">
      <div style="flex:1;text-align:center;border-right:1px solid var(--border);padding:0 24px">
        <div style="font-family:'Montserrat',sans-serif;font-size:40px;font-weight:800;color:var(--page-accent,var(--blue));line-height:1">3</div>
        <div style="font-size:11px;font-weight:600;letter-spacing:0.12em;text-transform:uppercase;color:var(--mid);margin-top:8px">Layout Patterns<br/>Evaluated</div>
      </div>
      <div style="flex:1;text-align:center;border-right:1px solid var(--border);padding:0 24px">
        <div style="font-family:'Montserrat',sans-serif;font-size:40px;font-weight:800;color:var(--page-accent,var(--blue));line-height:1">1</div>
        <div style="font-size:11px;font-weight:600;letter-spacing:0.12em;text-transform:uppercase;color:var(--mid);margin-top:8px">Hybrid System<br/>Designed</div>
      </div>
      <div style="flex:1;text-align:center;padding:0 24px">
        <div style="font-family:'Montserrat',sans-serif;font-size:40px;font-weight:800;color:var(--page-accent,var(--blue));line-height:1">2+</div>
        <div style="font-size:11px;font-weight:600;letter-spacing:0.12em;text-transform:uppercase;color:var(--mid);margin-top:8px">Scalable Consent<br/>Frameworks</div>
      </div>
    </div>"""

STATS_ROW_CTRAX = """
    <div class="stats-row fade-up" style="display:flex;gap:0;margin:40px 0;border-top:1px solid var(--border);border-bottom:1px solid var(--border);padding:32px 0">
      <div style="flex:1;text-align:center;border-right:1px solid var(--border);padding:0 24px">
        <div style="font-family:'Montserrat',sans-serif;font-size:40px;font-weight:800;color:var(--page-accent,var(--blue));line-height:1">3</div>
        <div style="font-size:11px;font-weight:600;letter-spacing:0.12em;text-transform:uppercase;color:var(--mid);margin-top:8px">Distinct<br/>Audience Types</div>
      </div>
      <div style="flex:1;text-align:center;border-right:1px solid var(--border);padding:0 24px">
        <div style="font-family:'Montserrat',sans-serif;font-size:40px;font-weight:800;color:var(--page-accent,var(--blue));line-height:1">2</div>
        <div style="font-size:11px;font-weight:600;letter-spacing:0.12em;text-transform:uppercase;color:var(--mid);margin-top:8px">Core Product<br/>Surfaces</div>
      </div>
      <div style="flex:1;text-align:center;padding:0 24px">
        <div style="font-family:'Montserrat',sans-serif;font-size:40px;font-weight:800;color:var(--page-accent,var(--blue));line-height:1">1</div>
        <div style="font-size:11px;font-weight:600;letter-spacing:0.12em;text-transform:uppercase;color:var(--mid);margin-top:8px">Unified Design<br/>System</div>
      </div>
    </div>"""

STATS_ROW_EHE = """
    <div class="stats-row fade-up" style="display:flex;gap:0;margin:40px 0;border-top:1px solid var(--border);border-bottom:1px solid var(--border);padding:32px 0">
      <div style="flex:1;text-align:center;border-right:1px solid var(--border);padding:0 24px">
        <div style="font-family:'Montserrat',sans-serif;font-size:40px;font-weight:800;color:var(--page-accent,var(--blue));line-height:1">9</div>
        <div style="font-size:11px;font-weight:600;letter-spacing:0.12em;text-transform:uppercase;color:var(--mid);margin-top:8px">Research<br/>Participants</div>
      </div>
      <div style="flex:1;text-align:center;border-right:1px solid var(--border);padding:0 24px">
        <div style="font-family:'Montserrat',sans-serif;font-size:40px;font-weight:800;color:var(--page-accent,var(--blue));line-height:1">2</div>
        <div style="font-size:11px;font-weight:600;letter-spacing:0.12em;text-transform:uppercase;color:var(--mid);margin-top:8px">Journey<br/>Maps Built</div>
      </div>
      <div style="flex:1;text-align:center;padding:0 24px">
        <div style="font-family:'Montserrat',sans-serif;font-size:40px;font-weight:800;color:var(--page-accent,var(--blue));line-height:1">4</div>
        <div style="font-size:11px;font-weight:600;letter-spacing:0.12em;text-transform:uppercase;color:var(--mid);margin-top:8px">Core Features<br/>Designed</div>
      </div>
    </div>"""

# ── Helpers ────────────────────────────────────────────────────────────────────
def remove_progress_bar(html):
    # Remove the div
    html = re.sub(r'\n?[ \t]*<div class="progress-bar" id="progress"></div>', '', html)
    # Remove CSS block for progress-bar
    html = re.sub(r'\n?[ \t]*#progress\{[^}]*\}', '', html)
    html = re.sub(r'\n?[ \t]*\.progress-bar\{[^}]*\}', '', html)
    # Remove JS that reads/sets progress
    html = re.sub(r'\n?[ \t]*(?:var|const|let) progress\s*=\s*document\.getElementById\([\'"]progress[\'"]\);?', '', html)
    html = re.sub(r'\n?[ \t]*progress\.style\.transform[^\n]+', '', html)
    # Remove the scroll listener block if it only contains progress logic
    html = re.sub(r'\n?[ \t]*window\.addEventListener\([\'"]scroll[\'"],\s*function\(\)\s*\{[^}]*progress[^}]*\}\s*(?:,\s*\{[^}]*\}\s*)?\);', '', html)
    return html

def add_icons_to_section_labels(html):
    def replace_label(m):
        open_tag = m.group(1)
        text = m.group(2)
        close_tag = m.group(3)
        icon = ICONS.get(text.strip(), '')
        if icon and icon not in html[max(0, m.start()-5):m.start()+5]:
            return f'{open_tag}{icon}{text}{close_tag}'
        return m.group(0)
    # Match both <p> and <div> section-labels
    pattern = r'(<(?:p|div)[^>]*class="section-label[^"]*"[^>]*>)((?:(?!</).)+?)(</(?:p|div)>)'
    return re.sub(pattern, replace_label, html, flags=re.DOTALL)

def inject_after(html, anchor_text, injection):
    """Inject HTML string right after the first occurrence of anchor_text."""
    idx = html.find(anchor_text)
    if idx == -1:
        return html
    insert_at = idx + len(anchor_text)
    return html[:insert_at] + injection + html[insert_at:]

def add_treatment(html, filename):
    block = TREATMENTS.get(filename)
    if not block:
        return html
    # Only inject if not already present
    if 'class="si"' in html:
        return html  # already done
    return html.replace('</head>', block + '\n</head>', 1)

# ── Per-file processing ────────────────────────────────────────────────────────
def process_file(filename):
    path = os.path.join(GIT, filename)
    if not os.path.exists(path):
        print(f'  SKIP (not found): {filename}')
        return

    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    original = html

    # 1. Remove progress bar
    html = remove_progress_bar(html)

    # 2. Add page treatment / .si style
    html = add_treatment(html, filename)

    # 3. Add icons to section labels
    html = add_icons_to_section_labels(html)

    # 4. Inject metrics (file-specific)
    if filename == 'att-casestudy-rdot.html':
        anchor = 'The Layout Problem Nobody Warned About'
        # inject after the subtitle paragraph
        anchor2 = 'and a requirement that none of it feel coercive.</p>'
        if anchor2 in html and 'stats-row' not in html:
            html = inject_after(html, anchor2, STATS_ROW_ATT)

    elif filename == 'ctrax-casestudy-rdot.html':
        anchor = "The previous system treated them all the same. That&#8217;s where the friction lived.</p>"
        if anchor in html and 'stats-row' not in html:
            html = inject_after(html, anchor, STATS_ROW_CTRAX)

    elif filename == 'ehe-casestudy-rdot.html':
        anchor = 'what each audience needed from a digital experience.</p>'
        if anchor in html and 'stats-row' not in html:
            html = inject_after(html, anchor, STATS_ROW_EHE)

    if html != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f'  UPDATED: {filename}')
    else:
        print(f'  NO CHANGE: {filename}')

    # Copy to /tmp
    shutil.copy2(path, os.path.join(TMP, filename))
    print(f'  COPIED to /tmp/{filename}')

# ── Run ────────────────────────────────────────────────────────────────────────
FILES = [
    'att-casestudy-rdot.html',
    'boa-flagscape-casestudy-rdot.html',
    'btki-casestudy-rdot.html',
    'ctrax-casestudy-rdot.html',
    'ehe-casestudy-rdot.html',
    'goosehead-casestudy-rdot.html',
    'andela-casestudy-rdot.html',
    'boa-casestudy-rdot.html',
    'platinum-case-study_1.html',
    'index.html',
]

for fn in FILES:
    print(f'\n{fn}')
    process_file(fn)

print('\nDone.')
