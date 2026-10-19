import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load template + all article data parts in order
_d = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(_d, "gen_25_christmas.py")).read())  # defines template + ARTICLES = []
exec(open(os.path.join(_d, "gen_25_christmas_a1.py")).read())
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "gen_25_christmas_a2.py")).read())
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "gen_25_christmas_a3.py")).read())

OUT = os.path.expanduser("~/workspace/event-blog/site/articles")
os.makedirs(OUT, exist_ok=True)

print(f"Generating {len(ARTICLES)} articles...")
slugs = []
for a in ARTICLES:
    html = article_html(a)
    path = os.path.join(OUT, a["slug"] + ".html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    words = len(html.split())
    slugs.append(a["slug"])
    print(f"  OK {a['slug']}.html (~{words} words)")

print(f"\nDone: {len(slugs)} articles written to {OUT}")
print("SLUGS:")
for s in slugs:
    print(f"  - {s}")
