#!/usr/bin/env python3
"""Stage real hunted Temu products into the 50 new EventBuzz articles' shop-grids.
Replaces PLACEHOLDER SHOP GRID sections with verified products (2026-10-17 hunt).
- Hassan's 22 catalog-verified products: real affiliate links + images -> used directly
- Qasim's 15 image-verified products: Temu search links -> used, flagged for Convert Link
- Suhail's couponhubusa-affiliate items: EXCLUDED
"""
import re, os, html

ART_DIR = os.path.expanduser("~/workspace/event-blog/site/articles")

def P(name, price, image_url, url):
    return {"name": name, "price": price, "image": image_url, "url": url}

# ---------- Hassan: 22 catalog-verified (own affiliate links + real images) ----------
H_COSTUMES = [
    P("Hooded Halloween Dress", "See live deal",
      "https://img.kwcdn.com/product/fancy/6ea5139e-a856-4c1e-8c3b-0b5ded39c43f.jpg",
      "https://www.temu.com/goods.html?goods_id=601099643706695&_x_cid=6013029639kol_affiliate"),
    P("2pcs Halloween Witch Costume - Velvet Cape and Feather Shawl Set", "See live deal",
      "https://img.kwcdn.com/product/fancy/83cf547e-0442-47c2-8efb-084399725410.jpg",
      "https://temu.to/k/pnpzdhb0lio"),
    P("Halloween Witch Costume 4pcs Set - Dress, Hat, Stockings and Broom", "See live deal",
      "https://img.kwcdn.com/product/fancy/3b97d0d6-5574-493e-b21c-29df766ce045.jpg",
      "https://temu.to/k/pmgnbpv2mdx"),
    P("1920s Handmade Sequin Halloween Party Cape Shawl", "$9.63",
      "https://img.kwcdn.com/product/fancy/b687706d-a959-4593-9671-56f0890edecd.jpg",
      "https://temu.to/k/egzfji5es5y"),
    P("Cape with Feathered Horns - Halloween Costume Accessory", "See live deal",
      "https://img.kwcdn.com/product/open/2024-04-05/1712320473051-7bc56325c623417d89817100f8836f43-goods.jpeg",
      "https://www.temu.com/goods.html?goods_id=601099560799010&_x_cid=6013029639kol_affiliate"),
    P("Dark Gothic Style Cosplay Costume with Shoulder Lace", "See live deal",
      "https://img.kwcdn.com/product/fancy/d47b923e-96fc-4348-8662-32469163b17f.jpg",
      "https://www.temu.com/goods.html?goods_id=601101553198375&_x_cid=6013029639kol_affiliate"),
]
H_MAKEUP = [
    P("Glitter Diamond Shiny Mascara - Waterproof, Curling and Lengthening", "See live deal",
      "https://img.kwcdn.com/product/fancy/ccbd270b-1a7a-4f21-8e7d-36ec2c63830d.jpg",
      "https://www.temu.com/goods.html?goods_id=601099670440932&_x_cid=6013029639kol_affiliate"),
    P("Easy-Apply Self-Adhesive False Eyelash Stickers, 12pcs Rainbow Glitter", "See live deal",
      "https://img.kwcdn.com/product/fancy/5f36dfab-5bb5-4673-b9a7-4b3592cfdf35.jpg",
      "https://www.temu.com/goods.html?goods_id=601099692867439&_x_cid=6013029639kol_affiliate"),
    P("Gradient Tea-Brown Straight Costume Wig for Cosplay and Halloween", "See live deal",
      "https://img.kwcdn.com/product/fancy/d5f54937-cc26-454b-9a42-0e3e6b3e2b36.jpg",
      "https://www.temu.com/goods.html?goods_id=601099933924358&_x_cid=6013029639kol_affiliate"),
]
H_KIDS = [
    P("30pcs Party Favors Fidget Keychain Mini Toys", "See live deal",
      "https://img.kwcdn.com/product/fancy/99cc2d69-7c52-41f8-aa55-d1769b1a89b5.jpg",
      "https://www.temu.com/goods.html?goods_id=601099548475563&_x_cid=6013029639kol_affiliate"),
    P("Halloween Dragon Fountain Pens Gift Set with 20 Ink Cartridges", "See live deal",
      "https://img.kwcdn.com/product/fancy/ff494161-dd1b-47a0-80e2-aff7fde57c7c.jpg",
      "https://www.temu.com/goods.html?goods_id=601102212705744&_x_cid=6013029639kol_affiliate"),
    P("Halloween Ghost with Pumpkin Resin Figurine", "See live deal",
      "https://img.kwcdn.com/product/fancy/2c31a5c8-3706-4dbb-8e93-fe4b3dd36169.jpg",
      "https://www.temu.com/goods.html?goods_id=601101900927747&_x_cid=6013029639kol_affiliate"),
    P("Black and White Pumpkin Resin Figurine", "See live deal",
      "https://img.kwcdn.com/product/fancy/2a06e4f1-fea1-405c-bf9b-188c1447b306.jpg",
      "https://www.temu.com/goods.html?goods_id=601099688310704&_x_cid=6013029639kol_affiliate"),
    P("Skeleton Bat Window Stickers", "See live deal",
      "https://img.kwcdn.com/product/fancy/4306867e-3e62-47ca-bed3-23437f6b04d0.jpg",
      "https://www.temu.com/goods.html?goods_id=606804369090587&_x_cid=6013029639kol_affiliate"),
]
H_HOME = [
    P("Witch Themed Wooden Round Wall Decor", "See live deal",
      "https://img.kwcdn.com/product/fancy/33eec79a-cd60-426a-9af1-516dc9606eb9.jpg",
      "https://www.temu.com/goods.html?goods_id=601099971415061&_x_cid=6013029639kol_affiliate"),
    P("4pcs Autumn Pumpkin Pillow Covers Set", "See live deal",
      "https://img.kwcdn.com/product/open/24d673df69364708843f72f1e05115b8-goods.jpeg",
      "https://www.temu.com/goods.html?goods_id=601102215390705&_x_cid=6013029639kol_affiliate"),
    P("Pumpkin Print Halloween Tablecloth", "See live deal",
      "https://img.kwcdn.com/product/fancy/2d24601a-090b-44e2-82b4-4e4dadd12d9b.jpg",
      "https://www.temu.com/goods.html?goods_id=601099619496558&_x_cid=6013029639kol_affiliate"),
    P("20pcs Orange Pumpkin String Lights with Timer, 11ft LED", "See live deal",
      "https://img.kwcdn.com/product/algo_check/auto/ed1ea5e5647aca95d4f04e9990b1b6de_1753351939498.jpg",
      "https://temu.to/k/pxfds41m4z5"),
    P("Halloween Ghost Bat Pumpkin LED String Lights", "See live deal",
      "https://img.kwcdn.com/product/fancy/eb0622b2-cf8e-4157-adf8-cc641f1edd21.jpg",
      "https://temu.to/k/prc5lotovj5"),
    P("Halloween String Lights 2pcs - 20 LEDs Pumpkins Witches Ghosts", "See live deal",
      "https://img.kwcdn.com/product/fancy/67af3791-25a0-44db-b89d-1c4d5a9dc5d3.jpg",
      "https://temu.to/k/pgv7om5qpl9"),
    P("Witch Hat Stained Glass Glowing Lamp", "See live deal",
      "https://img.kwcdn.com/product/fancy/2ddd3b98-058d-4605-af9c-813ab7ac189f.jpg",
      "https://www.temu.com/goods.html?goods_id=601100408547135&_x_cid=6013029639kol_affiliate"),
    P("Realistic Adult Skull Model Halloween Decor", "See live deal",
      "https://img.kwcdn.com/product/fancy/431ac578-b9c3-4587-97a1-9a8140d9a900.jpg",
      "https://www.temu.com/goods.html?goods_id=601103554182120&_x_cid=6013029639kol_affiliate"),
]

# ---------- Qasim: 15 image-verified (Temu search links - NEED Convert Link) ----------
def QP(name, price, image_url, search_key):
    return P(name, price, image_url,
             "https://www.temu.com/search_result.html?search_key=" + search_key)

Q_DECOR = [
    QP("Solar Flickering Flame Torch Lights (8 pack)", "~$10.42",
       "https://img.kwcdn.com/product/fancy/ba6eec82-135f-4443-9398-9801239319c9.jpg",
       "solar%20flickering%20flame%20torch%20lights%20halloween"),
    QP("3D Black PVC Bat Wall Decor", "~$1.13",
       "https://img.kwcdn.com/product/fancy/c94b7a8e-c18e-42a6-82e0-50d71794c0c8.jpg",
       "3d%20black%20pvc%20bat%20wall%20decor%20halloween"),
    QP("Halloween Eyeball String Lights (10 LED)", "~$2.43",
       "https://img.kwcdn.com/product/fancy/e4ef0177-85a5-461a-ba06-fe69565458e1.jpg",
       "halloween%20eyeball%20string%20lights"),
    QP("200 sq ft Stretch Cobweb with 10 Fake Spiders", "~$2.39",
       "https://img.kwcdn.com/product/algo_check/auto/b2c413d4b86e2624a7da9eecf6ae061d1786633891342.jpg",
       "stretch%20cobweb%20fake%20spiders%20halloween"),
    QP("Fright Caution Tape (2 x 33 ft)", "~$1.83",
       "https://img.kwcdn.com/product/fancy/922cedbd-fe13-4c36-b6e1-382ca9f58fae.jpg",
       "halloween%20fright%20caution%20tape"),
    QP("Giant 16 ft Spider Web with 60 in Spider", "~$6.65",
       "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/dd92fe39f084cd76e4adf6e078b72589.jpg",
       "giant%2016ft%20spider%20web%20halloween%20yard"),
    QP("Gothic Spider Web Mesh Drape", "~$2.85",
       "https://img.kwcdn.com/product/fancy/26b3bb6d-1b74-42a9-a392-3b34a5413fe4.jpg",
       "gothic%20spider%20web%20mesh%20drape%20halloween"),
    QP("Large Black and White Hanging Ghost", "~$5.41",
       "https://img.kwcdn.com/product/fancy/e0d1a2ae-7acf-4d7a-9eab-b11db434a2fd.jpg",
       "large%20hanging%20ghost%20halloween%20decoration"),
    QP("Floating Wizard Hats (3, 6 or 12 pcs)", "~$2.65",
       "https://img.kwcdn.com/product/fancy/bfdb7430-3f4d-4d52-a668-bb1b7162719b.jpg",
       "floating%20wizard%20witch%20hats%20halloween"),
    QP("Glow in the Dark 3D Hanging Bats (10 pcs)", "~$5.68",
       "https://img.kwcdn.com/product/fancy/0d399c3a-b639-4b36-8cd2-0590a78c195d.jpg",
       "glow%20in%20the%20dark%203d%20hanging%20bats"),
    QP("Halloween BOO Cat Doormat", "~$4.05",
       "https://img.kwcdn.com/product/open/de5c997cda0d4837bde9b0c628daaf89-goods.jpeg",
       "halloween%20boo%20cat%20doormat"),
    QP("Spider Web Lace Tablecloth", "~$2.15",
       "https://img.kwcdn.com/product/fancy/5d843f31-d8a2-4375-b2bb-1a0641a8a035.jpg",
       "spider%20web%20lace%20tablecloth%20halloween"),
    P("Halloween Decorations 3pcs Set - Sound-Activated Light-Up Eyes", "See live deal",
      "https://img.kwcdn.com/product/fancy/f89c8b69-6d2c-4c56-92d5-80c46f2c96c7.jpg",
      "https://www.temu.com/goods.html?goods_id=605542940552016"),
    P("Halloween Plush Spider Set with Webs", "See live deal",
      "https://img.kwcdn.com/product/fancy/51687a63-d5e9-4ac1-8d6a-4ffaceb10c84.jpg",
      "https://www.temu.com/goods.html?goods_id=607437608317573"),
    P("2pcs Rustic Farmhouse Halloween Decor Set", "See live deal",
      "https://img.kwcdn.com/product/fancy/89c6e9f1-c746-4878-8069-9778eb178780.jpg",
      "https://www.temu.com/goods.html?goods_id=607307115155085"),
]

def card(p):
    name = html.escape(p["name"], quote=True)
    url = html.escape(p["url"], quote=True)
    img = html.escape(p["image"], quote=True)
    price = html.escape(p["price"], quote=True)
    return (
        '<div class="shop-card">'
        f'<a href="{url}" target="_blank" rel="sponsored nofollow noopener">'
        f'<img src="{img}" alt="{name}" loading="lazy"></a>'
        f'<div class="sc-body"><div class="sc-title">{html.escape(p["name"])}</div>'
        f'<div class="sc-price">{price}</div>'
        f'<a class="sc-btn" href="{url}" target="_blank" rel="sponsored nofollow noopener">View on Temu</a>'
        "</div></div>"
    )

def pick(pool, idx, n=4):
    return [pool[(idx + k) % len(pool)] for k in range(n)]

# slug -> list of 4 products
M = {}
# --- Costumes (17): rotate Hassan's 6 costume products, targeted for obvious ones ---
costume_slugs = [
    "halloween-costume-ideas-for-seniors-2026",
    "halloween-pregnancy-costume-ideas-2026",
    "halloween-twin-costume-ideas-2026",
    "halloween-sibling-costume-ideas-2026",
    "halloween-family-costume-ideas-2026",
    "halloween-disney-costume-ideas-2026",
    "halloween-superhero-costume-ideas-2026",
    "halloween-villain-costume-ideas-2026",
    "halloween-80s-costume-ideas-2026",
    "halloween-90s-costume-ideas-2026",
    "halloween-witch-costume-ideas-2026",
    "halloween-vampire-costume-ideas-2026",
    "halloween-pirate-costume-ideas-2026",
    "halloween-clown-costume-ideas-2026",
    "halloween-ghost-costume-ideas-2026",
    "halloween-plus-size-costume-ideas-2026",
    "halloween-diy-costume-ideas-under-20-2026",
]
C = H_COSTUMES
M["halloween-witch-costume-ideas-2026"] = [C[1], C[2], C[4], C[0]]
M["halloween-vampire-costume-ideas-2026"] = [C[5], C[4], C[3], C[0]]
M["halloween-ghost-costume-ideas-2026"] = [C[0], C[3], C[5], C[4]]
M["halloween-diy-costume-ideas-under-20-2026"] = [C[3], C[4], C[0], C[1]]
M["halloween-disney-costume-ideas-2026"] = [C[0], C[1], C[3], C[4]]
M["halloween-superhero-costume-ideas-2026"] = [C[5], C[0], C[4], C[3]]
M["halloween-villain-costume-ideas-2026"] = [C[5], C[4], C[2], C[0]]
M["halloween-pirate-costume-ideas-2026"] = [C[4], C[3], C[0], C[5]]
M["halloween-clown-costume-ideas-2026"] = [C[0], C[4], C[3], C[2]]
for i, s in enumerate(costume_slugs):
    if s not in M:
        M[s] = pick(C, i)

# --- Decor (11): Qasim decor + Hassan home/decor ---
D = Q_DECOR + H_HOME
decor_slugs = [
    "halloween-mantel-decoration-ideas-2026",
    "halloween-porch-decoration-ideas-2026",
    "halloween-staircase-decoration-ideas-2026",
    "halloween-bedroom-decoration-ideas-2026",
    "halloween-kitchen-decoration-ideas-2026",
    "halloween-diy-paper-decorations-2026",
    "halloween-balloon-decoration-ideas-2026",
    "halloween-candle-decoration-ideas-2026",
    "halloween-wreath-ideas-2026",
    "halloween-centerpiece-ideas-2026",
    "halloween-outdoor-lighting-ideas-2026",
]
M["halloween-outdoor-lighting-ideas-2026"] = [Q_DECOR[0], Q_DECOR[2], H_HOME[3], H_HOME[4]]
M["halloween-porch-decoration-ideas-2026"] = [Q_DECOR[10], Q_DECOR[7], Q_DECOR[0], H_HOME[3]]
M["halloween-mantel-decoration-ideas-2026"] = [Q_DECOR[14], H_HOME[0], Q_DECOR[11], H_HOME[1]]
M["halloween-candle-decoration-ideas-2026"] = [H_HOME[6], H_HOME[3], Q_DECOR[2], H_HOME[4]]
M["halloween-centerpiece-ideas-2026"] = [Q_DECOR[14], H_HOME[1], H_HOME[2], Q_DECOR[11]]
for i, s in enumerate(decor_slugs):
    if s not in M:
        M[s] = pick(D, i * 4)

# --- Party (7) ---
P_POOL = [Q_DECOR[4], Q_DECOR[8], Q_DECOR[11], Q_DECOR[3], H_HOME[2], H_HOME[1], H_HOME[3], H_HOME[4], H_HOME[5]]
party_slugs = [
    "halloween-birthday-party-ideas-2026",
    "halloween-virtual-party-ideas-2026",
    "halloween-neighborhood-block-party-2026",
    "halloween-party-themes-2026",
    "halloween-murder-mystery-party-2026",
    "halloween-bonfire-party-ideas-2026",
    "halloween-party-playlist-2026",
]
M["halloween-murder-mystery-party-2026"] = [Q_DECOR[4], H_HOME[7], Q_DECOR[8], H_HOME[6]]
M["halloween-bonfire-party-ideas-2026"] = [Q_DECOR[0], Q_DECOR[7], H_HOME[7], Q_DECOR[4]]
for i, s in enumerate(party_slugs):
    if s not in M:
        M[s] = pick(P_POOL, i * 4)

# --- Food (7): table/decor items ---
F_POOL = [H_HOME[2], H_HOME[1], H_KIDS[2], H_KIDS[3], Q_DECOR[11], Q_DECOR[8], H_HOME[3], H_HOME[5]]
food_slugs = [
    "halloween-dinner-party-menu-2026",
    "halloween-appetizer-ideas-2026",
    "halloween-cake-ideas-2026",
    "halloween-cookie-recipes-2026",
    "halloween-cupcake-ideas-2026",
    "halloween-punch-recipes-2026",
    "halloween-healthy-snacks-2026",
]
for i, s in enumerate(food_slugs):
    M[s] = pick(F_POOL, i * 4)

# --- Kids (3) ---
K_POOL = H_KIDS + H_COSTUMES[:3]
kids_slugs = [
    "halloween-toddler-activities-2026",
    "halloween-science-experiments-for-kids-2026",
    "halloween-no-carve-pumpkin-ideas-2026",
]
M["halloween-toddler-activities-2026"] = [H_KIDS[0], H_KIDS[1], H_KIDS[2], H_COSTUMES[0]]
M["halloween-science-experiments-for-kids-2026"] = [H_KIDS[1], H_KIDS[0], H_KIDS[2], H_KIDS[4]]
M["halloween-no-carve-pumpkin-ideas-2026"] = [H_KIDS[3], H_KIDS[2], H_KIDS[4], H_HOME[3]]

# --- Beauty (3) ---
M["halloween-glam-makeup-ideas-2026"] = [H_MAKEUP[0], H_MAKEUP[1], H_MAKEUP[2], H_COSTUMES[5]]
M["halloween-sfx-makeup-for-beginners-2026"] = [H_MAKEUP[0], H_MAKEUP[1], H_HOME[7], H_COSTUMES[5]]
M["halloween-hair-ideas-2026"] = [H_MAKEUP[2], H_MAKEUP[0], H_MAKEUP[1], H_COSTUMES[4]]

# --- Movies + Pakistan ---
M["halloween-movies-for-kids-2026"] = [H_HOME[7], H_HOME[4], H_HOME[3], Q_DECOR[7]]
M["halloween-celebration-in-pakistan-2026"] = [Q_DECOR[1], Q_DECOR[3], H_HOME[3], Q_DECOR[10]]

NEEDS_CONVERT = "search_result.html?search_key="

done, missing, converted_flag = 0, [], 0
for slug, products in M.items():
    path = os.path.join(ART_DIR, slug + ".html")
    if not os.path.exists(path):
        missing.append(slug)
        continue
    with open(path, encoding="utf-8") as f:
        htxt = f.read()
    if "PLACEHOLDER SHOP GRID" not in htxt:
        missing.append(slug + " (no placeholder)")
        continue
    grid = '<div class="shop-grid">' + "".join(card(p) for p in products) + "</div>"
    needs = any(NEEDS_CONVERT in p["url"] for p in products)
    note = ("<!-- STAGED 2026-10-17: real hunted Temu products. "
            + ("Some links are Temu search links - run through Temu Convert Link for affiliate credit. " if needs else "")
            + "Images verified img.kwcdn.com. -->\n")
    # replace placeholder comment
    htxt = htxt.replace("<!-- PLACEHOLDER SHOP GRID: replace search links + placeholder images with verified Temu affiliate products -->", note.rstrip("\n"), 1)
    # replace shop-grid content
    new_txt, n = re.subn(r'<div class="shop-grid">.*?</div>\s*(<p class="shop-note">)',
                         lambda m: grid + "\n" + m.group(1), htxt, count=1, flags=re.DOTALL)
    if n == 0:
        missing.append(slug + " (grid regex failed)")
        continue
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_txt)
    done += 1
    if needs:
        converted_flag += 1

print(f"STAGED: {done} articles")
print(f"articles needing Convert Link: {converted_flag}")
print(f"MISSING/FAILED: {missing if missing else 'none'}")
