#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import markdown
import os
import shutil
import re

src_dir = r"D:\Books for writing book\System Architecture"
completed_dir = os.path.join(src_dir, "completed_files")
os.makedirs(completed_dir, exist_ok=True)

CHAPTERS = [
    ("Chapter-1.md",  "chapter-1.html",  "১",  "সিস্টেম ডিজাইনের ভিত্তি"),
    ("Chapter-2.md",  "chapter-2.html",  "২",  "সিস্টেমের গুণাগুণ"),
    ("Chapter-3.md",  "chapter-3.html",  "৩",  "Client-Server Model, HTTP ও REST API"),
    ("Chapter-4.md",  "chapter-4.html",  "৪",  "RDBMS vs NoSQL ও Query Optimization"),
    ("Chapter-5.md",  "chapter-5.html",  "৫",  "Caching, Redis ও Cache Invalidation"),
    ("Chapter-6.md",  "chapter-6.html",  "৬",  "CDN এবং Object, Block ও File Storage"),
    ("Chapter-7.md",  "chapter-7.html",  "৭",  "REST vs gRPC vs WebSockets"),
    ("Chapter-8.md",  "chapter-8.html",  "৮",  "Message Queues ও Kafka"),
    ("Chapter-9.md",  "chapter-9.html",  "৯",  "Horizontal vs Vertical Scaling"),
    ("Chapter-10.md", "chapter-10.html", "১০", "Load Balancer Deep Dive ও Sharding"),
    ("Chapter-11.md", "chapter-11.html", "১১", "Circuit Breakers ও Rate Limiting"),
    ("Chapter-12.md", "chapter-12.html", "১২", "Redundancy, Failover ও Health Checks"),
    ("Chapter-13.md", "chapter-13.html", "১৩", "CAP Theorem ও Consistency Models"),
    ("Chapter-14.md", "chapter-14.html", "১৪", "Clock Skew, Idempotency ও 2PC"),
    ("Chapter-15.md", "chapter-15.html", "১৫", "Service Discovery, API Gateway ও CQRS"),
    ("Chapter-16.md", "chapter-16.html", "১৬", "Event Sourcing ও Service Mesh"),
    ("Chapter-17.md", "chapter-17.html", "১৭", "কেস স্টাডি: WhatsApp, Instagram ও Twitter"),
    ("Chapter-18.md", "chapter-18.html", "১৮", "AWS Fundamentals ও Core AWS Services"),
    ("Chapter-19.md", "chapter-19.html", "১৯", "কেস স্টাডি: Dropbox, YouTube ও Netflix"),
    ("Chapter-20.md", "chapter-20.html", "২০", "Scaling to Millions ও AWS Auto Scaling"),
]

MD_EXTENSIONS = [
    "markdown.extensions.tables",
    "markdown.extensions.fenced_code",
    "markdown.extensions.nl2br",
    "markdown.extensions.sane_lists",
    "markdown.extensions.attr_list",
]

# ─────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────
CSS = """
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
  --sidebar-w: 300px;
  --sidebar-bg: #0f172a;
  --sidebar-border: #1e293b;
  --accent: #6366f1;
  --accent-hover: #818cf8;
  --active-bg: #1e293b;
  --active-text: #c7d2fe;
  --text-muted: #64748b;
  --text-light: #94a3b8;
  --body-bg: #f8fafc;
  --content-bg: #ffffff;
  --text-dark: #1e293b;
  --text-body: #374151;
  --border: #e2e8f0;
  --code-bg: #0f172a;
  --blockquote-bg: #eff6ff;
  --blockquote-border: #6366f1;
  --table-header: #f1f5f9;
  --tag-bg: #e0e7ff;
  --tag-text: #3730a3;
  --h1-color: #1e293b;
  --h2-color: #312e81;
  --h3-color: #4338ca;
  --shadow: 0 1px 3px rgba(0,0,0,.08), 0 4px 16px rgba(0,0,0,.04);
}

html { font-size: 16px; }

body {
  font-family: "Segoe UI", system-ui, -apple-system, sans-serif;
  background: var(--body-bg);
  color: var(--text-body);
  line-height: 1.7;
  min-height: 100vh;
}

/* ── Layout ── */
.layout {
  display: flex;
  min-height: 100vh;
}

/* ── Sidebar ── */
.sidebar {
  width: var(--sidebar-w);
  min-width: var(--sidebar-w);
  background: var(--sidebar-bg);
  display: flex;
  flex-direction: column;
  position: fixed;
  top: 0; left: 0; bottom: 0;
  overflow-y: auto;
  z-index: 100;
  scrollbar-width: thin;
  scrollbar-color: #334155 transparent;
}
.sidebar::-webkit-scrollbar { width: 4px; }
.sidebar::-webkit-scrollbar-track { background: transparent; }
.sidebar::-webkit-scrollbar-thumb { background: #334155; border-radius: 2px; }

.sidebar-header {
  padding: 24px 20px 20px;
  border-bottom: 1px solid var(--sidebar-border);
  position: sticky;
  top: 0;
  background: var(--sidebar-bg);
  z-index: 10;
}
.sidebar-brand {
  display: flex;
  align-items: center;
  gap: 12px;
  text-decoration: none;
  color: #f1f5f9;
}
.brand-icon {
  width: 40px; height: 40px;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  font-size: 20px;
  flex-shrink: 0;
}
.brand-text { line-height: 1.3; }
.brand-text .title { font-size: 0.95rem; font-weight: 700; color: #f1f5f9; }
.brand-text .subtitle { font-size: 0.72rem; color: var(--text-muted); margin-top: 2px; }

.sidebar-nav { padding: 12px 0 24px; }
.nav-section-label {
  font-size: 0.68rem;
  font-weight: 700;
  letter-spacing: .1em;
  text-transform: uppercase;
  color: var(--text-muted);
  padding: 16px 20px 6px;
}

.chapter-list { list-style: none; }
.chapter-list li a {
  display: flex;
  flex-direction: column;
  padding: 9px 20px;
  text-decoration: none;
  color: var(--text-light);
  border-left: 3px solid transparent;
  transition: all .18s ease;
  gap: 2px;
}
.chapter-list li a:hover {
  background: #1e293b;
  color: #e2e8f0;
  border-left-color: #4338ca;
}
.chapter-list li a.active {
  background: var(--active-bg);
  color: var(--active-text);
  border-left-color: var(--accent);
}
.chapter-list li a .ch-num {
  font-size: 0.68rem;
  font-weight: 700;
  letter-spacing: .05em;
  color: var(--accent);
  text-transform: uppercase;
}
.chapter-list li a.active .ch-num { color: var(--accent-hover); }
.chapter-list li a .ch-title {
  font-size: 0.82rem;
  font-weight: 500;
  line-height: 1.4;
}

.sidebar-footer {
  margin-top: auto;
  padding: 16px 20px;
  border-top: 1px solid var(--sidebar-border);
  font-size: 0.72rem;
  color: var(--text-muted);
  text-align: center;
}

/* ── Main Content ── */
.main-content {
  margin-left: var(--sidebar-w);
  flex: 1;
  min-height: 100vh;
  padding: 0 0 60px;
}

/* ── Home Page ── */
.home-page { padding: 48px; max-width: 900px; }
.home-hero {
  background: linear-gradient(135deg, #312e81 0%, #4c1d95 50%, #1e1b4b 100%);
  color: white;
  border-radius: 20px;
  padding: 48px;
  margin-bottom: 40px;
  position: relative;
  overflow: hidden;
}
.home-hero::before {
  content: '';
  position: absolute;
  top: -50%; right: -10%;
  width: 400px; height: 400px;
  background: rgba(255,255,255,.05);
  border-radius: 50%;
}
.home-hero .badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: rgba(255,255,255,.15);
  border: 1px solid rgba(255,255,255,.2);
  border-radius: 999px;
  padding: 4px 14px;
  font-size: 0.8rem;
  margin-bottom: 20px;
}
.home-hero h1 {
  font-size: 2.2rem;
  font-weight: 800;
  line-height: 1.2;
  margin-bottom: 16px;
  color: white;
  border: none;
  padding: 0;
}
.home-hero p { font-size: 1.05rem; opacity: .85; max-width: 500px; line-height: 1.7; }
.home-hero .stats {
  display: flex; gap: 32px; margin-top: 32px; flex-wrap: wrap;
}
.home-hero .stat { text-align: center; }
.home-hero .stat .num { font-size: 2rem; font-weight: 800; }
.home-hero .stat .lbl { font-size: 0.78rem; opacity: .7; margin-top: 2px; }

.section-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--text-dark);
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
}
.section-title::after {
  content: '';
  flex: 1;
  height: 1px;
  background: var(--border);
}

.chapter-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 16px;
  margin-bottom: 40px;
}
.chapter-card {
  background: var(--content-bg);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 20px;
  text-decoration: none;
  display: block;
  transition: all .2s ease;
  box-shadow: var(--shadow);
}
.chapter-card:hover {
  border-color: var(--accent);
  transform: translateY(-2px);
  box-shadow: 0 4px 20px rgba(99,102,241,.15);
}
.chapter-card .card-num {
  font-size: 0.7rem;
  font-weight: 700;
  color: var(--accent);
  text-transform: uppercase;
  letter-spacing: .08em;
  margin-bottom: 8px;
}
.chapter-card .card-title {
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--text-dark);
  line-height: 1.4;
}

/* ── Article / Blog Post ── */
.article-header {
  background: linear-gradient(135deg, #1e1b4b 0%, #312e81 100%);
  color: white;
  padding: 48px;
}
.article-header .chapter-tag {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: rgba(255,255,255,.15);
  border: 1px solid rgba(255,255,255,.2);
  border-radius: 999px;
  padding: 4px 14px;
  font-size: 0.78rem;
  font-weight: 600;
  margin-bottom: 16px;
}
.article-header h1 {
  font-size: 1.9rem;
  font-weight: 800;
  line-height: 1.3;
  color: white;
  border: none;
  padding: 0;
  margin: 0;
}

.article-body { padding: 48px; max-width: 820px; }

/* ── Typography ── */
.article-body h1, .article-body h2, .article-body h3,
.article-body h4, .article-body h5 {
  font-weight: 700;
  line-height: 1.3;
  margin-top: 2em;
  margin-bottom: .6em;
}
.article-body h1 { font-size: 1.8rem; color: var(--h1-color); padding-bottom: .4em; border-bottom: 2px solid #e0e7ff; }
.article-body h2 { font-size: 1.35rem; color: var(--h2-color); padding-left: 12px; border-left: 4px solid var(--accent); }
.article-body h3 { font-size: 1.1rem; color: var(--h3-color); }
.article-body h4 { font-size: 1rem; color: var(--text-dark); }

.article-body p { margin-bottom: 1.1em; color: var(--text-body); }

.article-body ul, .article-body ol {
  margin: 0 0 1.1em 1.5em;
}
.article-body li { margin-bottom: .35em; }
.article-body li > ul, .article-body li > ol { margin-top: .35em; margin-bottom: .35em; }

.article-body hr {
  border: none;
  border-top: 1px solid var(--border);
  margin: 2.5em 0;
}

.article-body blockquote {
  background: var(--blockquote-bg);
  border-left: 4px solid var(--blockquote-border);
  border-radius: 0 8px 8px 0;
  padding: 16px 20px;
  margin: 1.5em 0;
  color: #1e40af;
  font-style: normal;
}
.article-body blockquote p { margin-bottom: 0; color: #1e40af; }

/* ── Code ── */
.article-body code {
  font-family: "Cascadia Code", "Fira Code", "Consolas", monospace;
  font-size: .875em;
  background: #f1f5f9;
  color: #be185d;
  padding: 2px 6px;
  border-radius: 4px;
  border: 1px solid #e2e8f0;
}
.article-body pre {
  background: var(--code-bg);
  border-radius: 10px;
  padding: 20px;
  margin: 1.5em 0;
  overflow-x: auto;
  border: 1px solid #1e293b;
  box-shadow: 0 4px 20px rgba(0,0,0,.15);
}
.article-body pre code {
  background: none;
  color: #e2e8f0;
  border: none;
  padding: 0;
  font-size: .88rem;
  line-height: 1.65;
}

/* ── Tables ── */
.article-body table {
  width: 100%;
  border-collapse: collapse;
  margin: 1.5em 0;
  font-size: .9rem;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: var(--shadow);
}
.article-body th {
  background: var(--sidebar-bg);
  color: #e2e8f0;
  padding: 12px 16px;
  text-align: left;
  font-weight: 600;
  font-size: .83rem;
  text-transform: uppercase;
  letter-spacing: .04em;
}
.article-body td {
  padding: 11px 16px;
  border-bottom: 1px solid var(--border);
  vertical-align: top;
}
.article-body tr:nth-child(even) td { background: #f8fafc; }
.article-body tr:last-child td { border-bottom: none; }
.article-body tr:hover td { background: #eff6ff; }

/* ── Mermaid ── */
.mermaid {
  background: #fff;
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 24px;
  margin: 1.5em 0;
  text-align: center;
  overflow-x: auto;
}

/* ── Strong / Em ── */
.article-body strong { color: var(--text-dark); font-weight: 700; }

/* ── Nav Top Bar ── */
.top-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 48px;
  background: white;
  border-bottom: 1px solid var(--border);
  position: sticky;
  top: 0;
  z-index: 50;
  box-shadow: 0 1px 4px rgba(0,0,0,.06);
}
.top-bar .breadcrumb {
  font-size: 0.82rem;
  color: var(--text-muted);
  display: flex;
  align-items: center;
  gap: 8px;
}
.top-bar .breadcrumb a { color: var(--accent); text-decoration: none; }
.top-bar .breadcrumb a:hover { text-decoration: underline; }
.top-bar .breadcrumb .sep { color: var(--text-muted); }
.top-bar .page-nav { display: flex; gap: 8px; }
.top-bar .page-nav a {
  font-size: 0.82rem;
  color: var(--accent);
  text-decoration: none;
  padding: 6px 14px;
  border: 1px solid var(--border);
  border-radius: 6px;
  transition: all .15s;
}
.top-bar .page-nav a:hover { background: #eff6ff; border-color: var(--accent); }

/* ── Responsive ── */
@media (max-width: 768px) {
  :root { --sidebar-w: 0px; }
  .sidebar { transform: translateX(-300px); width: 300px; }
  .sidebar.open { transform: translateX(0); }
  .main-content { margin-left: 0; }
  .article-header, .article-body, .home-page { padding: 24px; }
  .home-hero { padding: 28px; }
  .home-hero h1 { font-size: 1.5rem; }
  .top-bar { padding: 12px 24px; }
  .menu-btn {
    display: flex !important;
    align-items: center; justify-content: center;
    width: 36px; height: 36px;
    background: var(--accent);
    color: white;
    border-radius: 8px;
    cursor: pointer;
    font-size: 1.2rem;
    border: none;
  }
}
.menu-btn { display: none; }

/* Scrollbar for main */
.main-content { scrollbar-width: thin; scrollbar-color: #cbd5e1 transparent; }
"""

# ─────────────────────────────────────────────
# JS
# ─────────────────────────────────────────────
JS = """
document.addEventListener('DOMContentLoaded', function () {
  // Mobile menu toggle
  var btn = document.getElementById('menuBtn');
  var sidebar = document.querySelector('.sidebar');
  if (btn && sidebar) {
    btn.addEventListener('click', function () {
      sidebar.classList.toggle('open');
    });
    document.addEventListener('click', function (e) {
      if (!sidebar.contains(e.target) && e.target !== btn) {
        sidebar.classList.remove('open');
      }
    });
  }

  // Highlight.js
  if (typeof hljs !== 'undefined') {
    document.querySelectorAll('pre code:not(.language-mermaid)').forEach(function (el) {
      hljs.highlightElement(el);
    });
  }

  // Mermaid
  if (typeof mermaid !== 'undefined') {
    mermaid.initialize({ startOnLoad: false, theme: 'default', securityLevel: 'loose' });
    document.querySelectorAll('.mermaid').forEach(function (el) {
      mermaid.run({ nodes: [el] }).catch(function (e) {
        el.innerHTML = '<em style="color:#ef4444">Diagram rendering requires a server (open via http://)</em>';
      });
    });
  }

  // Active sidebar item scroll into view
  var active = document.querySelector('.chapter-list .active');
  if (active) {
    active.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
  }
});
"""


def build_sidebar(active_file=None):
    home_cls = ' class="active"' if active_file == "index.html" else ""
    items = [
        f'<li><a href="index.html"{home_cls}>'
        f'<span class="ch-num">🏠 হোম</span>'
        f'<span class="ch-title">বইয়ের পরিচয় ও অধ্যায় তালিকা</span>'
        f'</a></li>'
    ]
    for _md, html_file, ch_num, ch_title in CHAPTERS:
        cls = ' class="active"' if html_file == active_file else ""
        items.append(
            f'<li><a href="{html_file}"{cls}>'
            f'<span class="ch-num">অধ্যায় {ch_num}</span>'
            f'<span class="ch-title">{ch_title}</span>'
            f'</a></li>'
        )
    return "\n          ".join(items)


def page_shell(title, body_html, active_file=None, prev_link=None, next_link=None, breadcrumb=""):
    nav_prev = f'<a href="{prev_link}">← আগের অধ্যায়</a>' if prev_link else ""
    nav_next = f'<a href="{next_link}">পরের অধ্যায় →</a>' if next_link else ""

    return f"""<!DOCTYPE html>
<html lang="bn">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} — সিস্টেম আর্কিটেকচার</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link href="https://fonts.googleapis.com/css2?family=Hind+Siliguri:wght@400;500;600;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/atom-one-dark.min.css" />
  <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js" defer></script>
  <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js" defer></script>
  <style>{CSS}</style>
</head>
<body>
<div class="layout">

  <!-- Sidebar -->
  <aside class="sidebar">
    <div class="sidebar-header">
      <a href="index.html" class="sidebar-brand">
        <div class="brand-icon">📚</div>
        <div class="brand-text">
          <div class="title">সিস্টেম আর্কিটেকচার</div>
          <div class="subtitle">System Design Bangla Book</div>
        </div>
      </a>
    </div>
    <nav class="sidebar-nav">
      <div class="nav-section-label">অধ্যায়সমূহ</div>
      <ul class="chapter-list">
        {build_sidebar(active_file)}
      </ul>
    </nav>
    <div class="sidebar-footer">© 2025 সিস্টেম আর্কিটেকচার</div>
  </aside>

  <!-- Main -->
  <div class="main-content">
    <div class="top-bar">
      <div class="breadcrumb">
        <button class="menu-btn" id="menuBtn" aria-label="Menu">☰</button>
        <a href="index.html">হোম</a>
        {('<span class="sep">›</span>' + breadcrumb) if breadcrumb else ""}
      </div>
      <div class="page-nav">
        {nav_prev}
        {nav_next}
      </div>
    </div>
    {body_html}
  </div>

</div>
<script>{JS}</script>
</body>
</html>"""


def convert_md_to_html(md_text):
    """Convert markdown to HTML, handle mermaid blocks separately."""
    mermaid_blocks = {}
    counter = [0]

    def replace_mermaid(m):
        # Use a placeholder that markdown won't mangle (no underscores/asterisks)
        key = f"MERMAIDDIVPLACEHOLDER{counter[0]}END"
        mermaid_blocks[key] = m.group(1).strip()
        counter[0] += 1
        return key

    # Extract ```mermaid ... ``` blocks before markdown processing
    md_text = re.sub(r"```mermaid\s*\n(.*?)```", replace_mermaid, md_text, flags=re.DOTALL)

    html = markdown.markdown(md_text, extensions=MD_EXTENSIONS)

    # Restore mermaid blocks — placeholder appears as <p>KEY</p> or plain KEY
    for key, diagram in mermaid_blocks.items():
        div = f'<div class="mermaid">{diagram}</div>'
        html = html.replace(f"<p>{key}</p>", div)
        html = html.replace(key, div)

    return html


def build_chapter_page(idx):
    md_file, html_file, ch_num, ch_title = CHAPTERS[idx]
    # MD files may already be in completed_files from a prior run
    md_path = os.path.join(src_dir, md_file)
    if not os.path.exists(md_path):
        md_path = os.path.join(completed_dir, md_file)

    with open(md_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    # Strip the first H1 (we'll render it in the header)
    first_h1 = re.match(r"^# .+\n", md_text)
    full_title = first_h1.group(0).strip("# \n") if first_h1 else f"অধ্যায় {ch_num}"
    if first_h1:
        md_text = md_text[first_h1.end():]

    body_html = convert_md_to_html(md_text)

    prev_link = CHAPTERS[idx - 1][1] if idx > 0 else None
    next_link = CHAPTERS[idx + 1][1] if idx < len(CHAPTERS) - 1 else None

    article = f"""
    <div class="article-header">
      <div class="chapter-tag">📖 অধ্যায় {ch_num}</div>
      <h1>{full_title}</h1>
    </div>
    <div class="article-body">
      {body_html}
    </div>
"""
    return page_shell(
        title=full_title,
        body_html=article,
        active_file=html_file,
        prev_link=prev_link,
        next_link=next_link,
        breadcrumb=f"অধ্যায় {ch_num}",
    )


def build_home_page():
    cards = []
    for md_file, html_file, ch_num, ch_title in CHAPTERS:
        cards.append(
            f'<a href="{html_file}" class="chapter-card">'
            f'<div class="card-num">অধ্যায় {ch_num}</div>'
            f'<div class="card-title">{ch_title}</div>'
            f'</a>'
        )

    cards_html = "\n      ".join(cards)

    body = f"""
    <div class="home-page">
      <div class="home-hero">
        <div class="badge">📚 বাংলায় সিস্টেম ডিজাইন</div>
        <h1>সিস্টেম আর্কিটেকচার</h1>
        <p>বড় মাপের সফটওয়্যার সিস্টেম কীভাবে ডিজাইন করতে হয় — তার পূর্ণাঙ্গ বাংলা গাইড।
           Scalability, Reliability, Databases, Caching, Microservices এবং আরও অনেক কিছু।</p>
        <div class="stats">
          <div class="stat"><div class="num">১৯</div><div class="lbl">অধ্যায়</div></div>
          <div class="stat"><div class="num">৩০০+</div><div class="lbl">ধারণা</div></div>
          <div class="stat"><div class="num">৫০+</div><div class="lbl">আর্কিটেকচার ডায়াগ্রাম</div></div>
          <div class="stat"><div class="num">১০০+</div><div class="lbl">কোড উদাহরণ</div></div>
        </div>
      </div>

      <div class="section-title">সকল অধ্যায়</div>
      <div class="chapter-grid">
        {cards_html}
      </div>
    </div>
"""
    return page_shell(
        title="হোম পেজ",
        body_html=body,
        active_file="index.html",
        breadcrumb="",
    )


def main():
    # Write home page
    home_html = build_home_page()
    with open(os.path.join(src_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(home_html)
    print("OK index.html")

    # Write chapter pages and move MD files
    for idx, (md_file, html_file, ch_num, ch_title) in enumerate(CHAPTERS):
        md_path = os.path.join(src_dir, md_file)
        if not os.path.exists(md_path):
            md_path = os.path.join(completed_dir, md_file)
        if not os.path.exists(md_path):
            print(f"  SKIP (not found): {md_file}")
            continue

        chapter_html = build_chapter_page(idx)
        out_path = os.path.join(src_dir, html_file)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(chapter_html)
        print(f"OK {html_file}")

        # Move MD to completed_files (only if still in src_dir)
        src_md = os.path.join(src_dir, md_file)
        if os.path.exists(src_md):
            dest = os.path.join(completed_dir, md_file)
            shutil.move(src_md, dest)
            print(f"   moved {md_file} to completed_files/")

    print("\nAll done!")


if __name__ == "__main__":
    main()
