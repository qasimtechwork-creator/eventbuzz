#!/usr/bin/env python3
"""Add ~100 words to each Christmas article under 600 words of body text.
Inserts a tip blockquote after the 2nd H2 section and an extra paragraph
at the end of the 4th H2 section. Structure stays: intro + 4 H2 + FAQs + conclusion.
"""
import re, os

D = os.path.expanduser("~/workspace/event-blog/site/articles")

# slug -> (blockquote tip after section 2, extra paragraph at end of section 4)
ADDITIONS = {
"christmas-party-themes-2026": (
    "Theme-commitment tip: pick one signature element guests will photograph — a balloon arch, a themed backdrop, or a dramatic dessert table — and let the rest be simple. One wow-factor beats ten half-done ideas.",
    "Finally, send guests home with a small themed favor: a mini ornament, a bag of your signature cookie mix, or a printed photo from the night. Favors cost little but make the party linger in memory long after the last song ends."
),
"christmas-cookie-recipes-2026": (
    "Baker's secret: weigh your flour with a kitchen scale instead of scooping. Scooped flour can vary by 30 percent, which is the hidden cause of most dry, crumbly holiday cookies.",
    "Do not forget presentation: stack cookies in clear cellophane bags tied with ribbon, or arrange them on a vintage platter lined with parchment. Beautiful packaging turns a simple batch into a gift people rave about."
),
"christmas-stocking-stuffers-2026": (
    "Smart stuffer strategy: follow the something-fun, something-useful, something-tasty rule. One item from each category keeps the stocking balanced and exciting to explore.",
    "Presentation matters as much as contents: wrap a few individual stuffers in tissue paper so there are surprises within the surprise. Kids especially love unwrapping tiny parcels from inside the stocking."
),
"last-minute-christmas-gifts-2026": (
    "Speed tip: keep a small stash of universal gifts year-round — nice candles, quality chocolate, elegant notebooks. Future you, shopping on December 23rd, will be deeply grateful.",
    "Whatever you choose, the card carries the weight. Write two genuine sentences about the person, not the gift. A heartfelt note transforms even the simplest last-minute present into something cherished."
),
"christmas-countdown-ideas-2026": (
    "Make it reusable: invest once in a wooden or fabric countdown calendar with pockets. Refill it every year with fresh notes and treats — it becomes a beloved family heirloom within three Decembers.",
    "Do not overcomplicate the daily reveals. Some of the most loved countdown moments are the simplest: a joke, a compliment, or ten minutes of undivided attention. Consistency beats extravagance."
),
"christmas-office-party-ideas-2026": (
    "Inclusion check: survey dietary needs and accessibility quietly beforehand, schedule at a time parents can attend, and keep games voluntary. The best office parties are ones where nobody feels awkward.",
    "End on a high note: close with a brief, genuine thank-you from leadership and a group photo. People remember how a party made them feel — appreciated beats entertained every time."
),
"christmas-photo-ideas-2026": (
    "Golden rule of holiday photos: take ten times more than you think you need. Digital film is free, and the magic shot is almost never the first one. Burst mode is your best friend with kids and pets.",
    "Back up your favorites the same week — upload to cloud storage and order at least a few prints. Photos trapped on a phone might as well not exist when you want to relive the magic years later."
),
"winter-wonderland-party-2026": (
    "Lighting is everything: keep overhead lights off and rely on fairy lights, candles, and blue uplighting. The right glow makes even dollar-store decor look like a million dollars.",
    "Send guests off with a frosted favor: a snowflake ornament, white chocolate bar, or mini candle in silver wrapping. It extends the wonderland magic all the way home."
),
"christmas-charity-ideas-2026": (
    "Start where you are: you do not need a big budget to give meaningfully. An hour of volunteering or a bag of groceries for the food bank genuinely changes someone's holiday.",
    "Make giving visible to your kids — let them choose the toys, pack the boxes, and hand over donations. Generosity learned young becomes generosity practiced for life."
),
"post-christmas-sales-2026": (
    "Price-check discipline: use a price tracker or simply ask whether you would buy it at full price. A 70 percent discount on something you do not need is still money wasted.",
    "Inventory your decorations before shopping clearance. Knowing exactly what you own prevents duplicate purchases and keeps your storage sane for next December."
),
"new-years-eve-party-ideas-2026": (
    "Pacing secret: plan one anchor activity per hour — trivia at 9, photo booth at 10, balloon drop practice at 11 — so energy never dips before the big countdown moment.",
    "Designate your midnight crew in advance: one person on music, one on the countdown clock, one on cameras. Midnight chaos is fun; midnight confusion is not."
),
"holiday-travel-tips-2026": (
    "The 24-hour rule: never schedule important events within a day of your arrival. December delays are common, and buffer time turns a missed connection from disaster into anecdote.",
    "Pack a small Christmas kit in your carry-on: a string of battery fairy lights, a few ornaments, and a scented sachet. Any hotel room becomes festive in five minutes flat."
),
"christmas-scavenger-hunt-kids-2026": (
    "Difficulty calibration: test-run your clues once before the big day. What is obvious to an adult can stump a seven-year-old, and nothing kills the fun like a clue nobody can solve.",
    "For mixed ages, pair older kids as team captains with younger ones. The big kids feel important, the little ones feel included, and you get to just enjoy the chaos."
),
"christmas-movie-night-ideas-2026": (
    "Sound matters more than screen size: even a basic soundbar transforms a living-room screening. If you have one, use it — dialogue clarity makes or breaks the experience.",
    "Build a simple tradition around it: same blankets, same cocoa recipe, same opening-night film each year. Rituals are what turn movie nights into the memories kids talk about as adults."
),
"christmas-eve-traditions-2026": (
    "Protect the evening: say no to extra commitments on December 24th. An unhurried Eve with nowhere to be is the greatest gift you can give your family — and yourself.",
    "Write a short family letter each Christmas Eve — where you have been, what you hope for. Seal them in an envelope and read the whole stack together in five years."
),
"holiday-budget-tips-2026": (
    "The 48-hour rule for impulse buys: see something tempting? Wait two days. Most holiday impulse purchases lose their shine by then, and your budget stays intact.",
    "Talk money openly with your partner before December. Agreeing on the total spend in November prevents 90 percent of January money arguments."
),
"christmas-mantel-decor-2026": (
    "The rule of thirds: mentally divide your mantel into three zones and style each differently — tall candles left, low greenery center, framed art right. Asymmetry looks professionally designed.",
    "Refresh mid-season: swap a few elements after Christmas Day to carry the mantel into New Year's. It takes ten minutes and makes the whole room feel new again."
),
"christmas-table-settings-2026": (
    "The one-inch rule: keep centerpieces under twelve inches tall so guests can see each other. Great conversation is the real centerpiece of any holiday table.",
    "Set the table the night before, minus candles and fresh flowers. Christmas Day is hectic enough without folding napkins between cooking tasks."
),
"christmas-wreath-ideas-2026": (
    "Scale check: hold the wreath up to your door before buying or making. A wreath that looks generous in the store often looks timid on a real door — when in doubt, go bigger.",
    "For double doors, hang two smaller matching wreaths instead of one large one. Symmetry on double doors looks intentional and grand."
),
"holiday-baking-essentials-2026": (
    "Mise en place saves December: measure and line up all ingredients before you start mixing. Holiday baking goes wrong most often when someone is frantically searching for baking powder mid-recipe.",
    "Keep a baking log: jot down what you made, tweaks, and family ratings. Next December you will know exactly which recipes deserve a repeat and which to retire."
),
}

count = 0
for slug, (tip, extra) in ADDITIONS.items():
    path = os.path.join(D, slug + ".html")
    html = open(path, encoding="utf-8").read()

    # Insert blockquote tip after the 2nd H2 section's first closing </ul> or </p>
    # Strategy: find all <h2> positions; insert after end of 2nd section content
    h2_positions = [m.start() for m in re.finditer(r"<h2>", html)]
    # We want after section 2 content = before 3rd <h2>
    third_h2 = h2_positions[2]
    blockquote = f'\n<blockquote>{tip}</blockquote>\n'
    html = html[:third_h2] + blockquote + html[third_h2:]

    # Append extra paragraph at end of 4th section = before shop-picks section
    shop_idx = html.find('<section class="shop-picks"')
    extra_p = f"\n<p>{extra}</p>\n"
    html = html[:shop_idx] + extra_p + html[shop_idx:]

    open(path, "w", encoding="utf-8").write(html)
    count += 1
    print(f"  beefed {slug}")

print(f"\nDone: {count} articles beefed up")
