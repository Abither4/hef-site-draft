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
`index.html` has no external requests at all. That is why it is ~2 MB.

## Layout

```
index.html          generated - do not edit
src/template.html   the page. edit this.
src/build.py        inlines fonts + photos
src/assets.json     photos, base64. keys map to __IMG_<KEY>__ tokens
src/fonts.json      Bebas Neue + Barlow woff2, base64
robots.txt          blocks search engines while this is a draft
```

To add a photo: add a key to `assets.json` as a `data:image/jpeg;base64,...`
string, then reference it in the template as `__IMG_YOURKEY__`.

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
- Giving is not wired up yet. The form collects amount and frequency; set
  `STRIPE_ENDPOINT` in the template's script to turn the button on.
