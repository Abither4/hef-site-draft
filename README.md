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
hef-hero.mp4        the hero loop. not inlined.
hef-music.m4a       the background music loop. not inlined.
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

`hef-hero.mp4` is a 28-second silent loop cut from HEF's own 5-minute
highlight film — eight shots with no titles, no captions, no aerials and no
photo-montage segments, so it carries no content the publication rules
exclude. It sits next to `index.html`; the page requests it by relative path.

`src/cut_hero.py` is the recipe: edit the `SHOTS` list and re-run it to recut.

It is deliberately **not** inlined, and the page treats it as optional. The
`<video>` ships with no `src`; the script attaches the file only above 700px
wide, only when the visitor has not asked for reduced motion, and only when the
browser is not reporting a metered connection. If any of that fails — or the
file is missing, as it is in the Claude artifact preview — the still hero photo
underneath is what shows. Nothing breaks.

To recut it, the source is the full highlight film. Note that the film's own
title cards contain a last name and a Deaf School reference, so **only
untitled footage can be used**.

## The background music

`hef-music.m4a` is 96 seconds of the film's own instrumental bed. HEF
confirmed the track is theirs to use on the site.

It starts on its own, as far as the browser allows. **Every current browser
blocks audio that starts without a user gesture**, so "plays on load" is not
something a website can actually guarantee. The script asks anyway, and if it
is refused it starts at the visitor's first click, tap or keypress instead —
a second or two in for most people. Scrolling deliberately is not treated as
that gesture, because browsers do not count it as one.

What keeps that from being obnoxious:

- The speaker button in the nav switches it off, and because the nav is
  sticky that switch is reachable from anywhere on the page. Nobody should
  have to scroll back to the top to make a website be quiet. (This is also
  what WCAG 1.4.2 requires of any audio that plays for more than 3 seconds.)
- **If someone switches it off, it stays off** — the choice is remembered in
  `localStorage`, and on their next visit nothing is even downloaded.
- It does not start at all on a connection reporting Save Data.
- It pauses when the tab goes to the background, fades in and out rather than
  cutting, and hides its own button if the file fails to load.

Volume is set in the script by `MUSIC_VOLUME` (currently `0.14` — deliberately
faint). That one number is the whole tuning knob.

`src/cut_music.py` builds the file. It is not a plain trim: the clip is
constructed so its end and its start are the same moment in the source, which
is what makes the loop seamless instead of clicking every 96 seconds.

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
