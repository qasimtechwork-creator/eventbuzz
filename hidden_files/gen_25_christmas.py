#!/usr/bin/env python3
"""Generate 25 Christmas 2026 SEO articles for EventBuzz.
Structure: intro + 4 H2 + shop-picks placeholders + 4 FAQs + Adsterra + conclusion.
Run: python3 gen_25_christmas.py
"""
import os

OUT = os.path.expanduser("~/workspace/event-blog/site/articles")
BASE = "https://eventbuzz-beta.vercel.app"
DATE = "2026-10-19"
DATE_HUMAN = "October 19, 2026"
ADSTERRA = '''      <script async="async" data-cfasync="false" src="https://pl31744790.profitableratecpmnetwork.com/76f7064cdd204b0b608553dc38d731b4/invoke.js"></script>
      <div id="container-76f7064cdd204b0b608553dc38d731b4"></div>'''

# Placeholder product cards (real affiliate products to be staged later)
PLACEHOLDER_CARDS = "".join(
    f'''<div class="shop-card"><a href="#" target="_blank" rel="sponsored nofollow noopener"><img src="../assets/images/product-placeholder.jpg" alt="Product placeholder {i+1}" loading="lazy"></a><div class="sc-body"><div class="sc-title">Product Placeholder {i+1}</div><div class="sc-price">$--</div><a class="sc-btn" href="#" target="_blank" rel="sponsored nofollow noopener">View Deal</a></div></div>'''
    for i in range(4)
)

def article_html(a):
    slug = a["slug"]; title = a["title"]; desc = a["desc"]
    cat = a["cat"]; cat_slug = a["cat_slug"]
    thumb = f"{BASE}/assets/thumbnails/christmas-2026/{slug}.jpg"
    canon = f"{BASE}/articles/{slug}"
    sections = "\n\n".join(f"<h2>{h}</h2>\n{body}" for h, body in a["sections"])
    faqs = "\n".join(
        f'''        <details>
          <summary>{q}</summary>
          <p>{ans}</p>
        </details>''' for q, ans in a["faqs"]
    )
    related = "\n".join(
        f'''          <article class="card">
            <span class="pill">{cat}</span>
            <h3><a href="{href}">{t}</a></h3>
            <p>{d}</p>
            <p style="margin-top:12px"><a class="read-more" href="{href}">Read &rarr;</a></p>
          </article>''' for href, t, d in a["related"]
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} &mdash; EventBuzz</title>
  <meta name="description" content="{desc}">
  <meta name="keywords" content="{a['keywords']}">
  <link rel="canonical" href="{canon}">
  <meta property="og:type" content="article">
  <meta property="og:site_name" content="EventBuzz">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{canon}">
  <meta property="og:image" content="{thumb}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image" content="{thumb}">
  <link rel="stylesheet" href="../assets/style.css">
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "{title}",
    "description": "{desc}",
    "author": {{ "@type": "Organization", "name": "EventBuzz" }},
    "publisher": {{ "@type": "Organization", "name": "EventBuzz" }},
    "datePublished": "{DATE}",
    "dateModified": "{DATE}",
    "image": "{thumb}",
    "mainEntityOfPage": "{canon}"
  }}
  </script>
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>

  <header class="site-header">
    <div class="container header-inner">
      <a class="logo" href="../" aria-label="EventBuzz home"><span class="logo-mark" aria-hidden="true">&#10022;</span><span>Event<em>Buzz</em></span></a>
      <nav class="main-nav" aria-label="Primary"><ul><li><a href="../">Home</a></li><li><a href="../categories/festivals">Festivals</a></li><li><a href="../categories/holidays">Holidays</a></li><li><a href="../categories/sports">Sports</a></li><li><a href="../categories/shopping-events">Shopping</a></li><li><a href="../categories/national-days">National Days</a></li><li><a href="../categories/seasonal-events">Seasonal</a></li><li><a href="../about">About</a></li><li><a href="../contact">Contact</a></li></ul></nav>
      <button class="nav-toggle" type="button" data-nav-toggle aria-expanded="false" aria-controls="mobile-nav">Menu &#9776;</button>
    </div>
    <nav class="mobile-nav container" id="mobile-nav" data-mobile-nav aria-label="Mobile"><ul><li><a href="../">Home</a></li><li><a href="../categories/festivals">Festivals</a></li><li><a href="../categories/holidays">Holidays</a></li><li><a href="../categories/sports">Sports Events</a></li><li><a href="../categories/shopping-events">Shopping Events</a></li><li><a href="../categories/national-days">National Days</a></li><li><a href="../categories/seasonal-events">Seasonal Events</a></li><li><a href="../about">About</a></li><li><a href="../contact">Contact</a></li></ul></nav>
  </header>

  <main id="main" class="container">
    <nav class="breadcrumb" aria-label="Breadcrumb">
      <a href="../">Home</a> &rsaquo; <a href="../categories/{cat_slug}">{cat}</a> &rsaquo; {a['crumb']}
    </nav>

    <article class="article-wrap">
      <div class="article-panel">
      <span class="pill">{cat}</span>
      <h1>{title}</h1>
      <figure class="hero-figure">
        <img src="../assets/thumbnails/christmas-2026/{slug}.jpg" alt="{title}" loading="eager">
      </figure>

      <div class="article-meta">
        <span>By EventBuzz Team</span>
        <span aria-hidden="true">&bull;</span>
        <time datetime="{DATE}">{DATE_HUMAN}</time>
        <span aria-hidden="true">&bull;</span>
        <span>7 min read</span>
      </div>

      <p>{a['intro']}</p>

{sections}

<section class="shop-picks" data-shop="20261019-auto">
<h2>{a['shop_title']}</h2>
<p class="shop-sub">{a['shop_sub']}</p>
<!-- PRODUCT PLACEHOLDERS: replace with 4 real hunted affiliate product cards before publishing -->
<div class="shop-grid">{PLACEHOLDER_CARDS}</div>
<p class="shop-note">Prices shown at the time of publishing and can change.</p>
</section>

      <section class="faq" aria-labelledby="faq-heading">
        <h2 id="faq-heading">Frequently Asked Questions</h2>
{faqs}
      </section>

{ADSTERRA}

      <h2>Conclusion</h2>
      <p>{a['conclusion']}</p>

      <section class="related" aria-labelledby="related-heading">
        <div class="section-head">
          <div>
            <div class="section-label"><span class="section-number">02</span><span class="eyebrow">Keep Reading</span></div>
            <h2 id="related-heading">Related Articles</h2>
          </div>
        </div>
        <div class="grid grid-3">
{related}
        </div>
      </section>
          </div>
    </article>
  </main>

  <footer class="site-footer">
    <div class="container">
      <div class="footer-grid">
        <div><p><strong>EventBuzz</strong></p><p>Your guide to holidays, festivals and celebrations around the world.</p></div>
        <div><p><a href="../">Home</a> &middot; <a href="../categories/festivals">Festivals</a> &middot; <a href="../categories/holidays">Holidays</a></p></div>
      </div>
      <p>&copy; 2026 EventBuzz. All rights reserved.</p>
      <p class="bookmark-hint">Tip: press <kbd>Ctrl</kbd>+<kbd>D</kbd> to bookmark EventBuzz so you never miss an event.</p>
    </div>
  </footer>
</body>
</html>
"""

ARTICLES = []
