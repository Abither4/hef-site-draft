# Haiti Endowment Fund — website draft

A working draft of a redesigned haitiendowmentfund.org homepage.
Live preview: https://abither4.github.io/hef-site-draft/

Not the live site. The real site is still the Wix build at haitiendowmentfund.org.

## The one thing to know

`index.html` is **generated**. Do not edit it directly — it gets overwritten.

Edit `src/template.html`, then rebuild:

```
cd src
python build.py
cp hef-draft.html ../index.html
```

`build.py` inlines the fonts and photos into a single self-contained file, so
`index.html` makes no external requests. That is why it is ~3.3 MB.

## Layout

```
index.html          generated - do not edit
hef-hero.mp4        the hero loop. the ONE file not inlined.
src/template.html   the page. edit this.
src/build.py        inlines fonts + photos
src/assets.json     photos, base64. keys map to __IMG_<KEY>__ tokens
src/add_assets.py   re-encodes new photos into assets.json (strips EXIF)
src/fonts.json      Bebas Neue + Barlow woff2, base64
robots.txt          blocks search engines while this is a draft
```

To add a photo: put it in `add_assets.py`'s `NEW` map and run it — that path
resizes, trims any letterbox bars, strips metadata, and writes the base64 into
`assets.json`. Then reference it in the template as `__IMG_YOURKEY__`.

## The hero video

`hef-hero.mp4` is an 11-second silent loop cut from HEF's own 5-minute
highlight film — three shots with no titles, no captions and no aerials, so it
carries no content the publication rules exclude. It sits next to
`index.html`; the page requests it by relative path.

It is deliberately **not** inlined, and the page treats it as optional. The
`<video>` ships with no `src`; the script attaches the file only above 700px
wide, only when the visitor has not asked for reduced motion, and only when the
browser is not reporting a metered connection. If any of that fails — or the
file is missing, as it is in the Claude artifact preview — the still hero photo
underneath is what shows. Nothing breaks.

To recut it, the source is the full highlight film. Note that the film's own
title cards contain a last name and a Deaf School reference, so **only
untitled footage can be used**.

## Publication rules

These come from HEF and are not optional:

- **No last names anywhere on the site.** First names only.
- **Locations at region level only** — "Hinche, Central Plateau." No villages.
- **No compound detail** — no acreage, maps, layouts, or asset inventories.
  Describe programs, not property.
- **US-side contact info only.**
- **Nothing forward-looking** — no upcoming trip dates or itineraries.
- **Strip EXIF/GPS from every image.** Re-encoding through `build.py`'s
  pipeline does this; never commit a phone or DSLR original.
- **No names on photos of children**, and no name+place pairings.
- **No gang or security content.**

## Open questions

- Student / meal / gift counts: the trifold says 3,200, the Christmas letter
  says 3,500. Pick one.
- Ministry age: the prayer card says 50 years, the letter says "more than
  forty." Pick one.
- Giving is not wired up yet. The form collects a donor-entered amount and a
  frequency; set `STRIPE_ENDPOINT` in the template's script to turn the button
  on. Preset amount buttons were removed at HEF's request.
- The prayer list still mentions the Deaf Ministry. The Deaf *School* was
  removed as asked; confirm whether the ministry line should go too.
