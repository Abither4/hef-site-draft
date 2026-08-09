"""Inline fonts + photos into the HEF draft page.

Edit template.html (readable, token placeholders) -> writes hef-draft.html (publishable).
Tokens: __FONTS__  and  __IMG_<key>__  for each key in assets.json
"""
import json, re, os

HERE = os.path.dirname(os.path.abspath(__file__))
assets = json.load(open(os.path.join(HERE, 'assets.json')))
fonts = json.load(open(os.path.join(HERE, 'fonts.json')))

face = []
for f in fonts:
    face.append(
        "@font-face{font-family:'%s';font-style:normal;font-weight:%s;font-display:swap;"
        "src:url(data:font/woff2;base64,%s) format('woff2');}" % (f['family'], f['weight'], f['b64'])
    )
font_css = ''.join(face)

html = open(os.path.join(HERE, 'template.html'), encoding='utf-8').read()
html = html.replace('__FONTS__', font_css)
for k, v in assets.items():
    html = html.replace('__IMG_%s__' % k.upper(), v)

# Digits count: a token like __IMG_ELDER2__ used to slip past this guard.
left = re.findall(r'__[A-Z0-9_]+__', html)
if left:
    raise SystemExit('unreplaced tokens: %s' % sorted(set(left)))

out = os.path.join(HERE, 'hef-draft.html')
open(out, 'w', encoding='utf-8').write(html)
print('wrote %s  %.2f MB' % (out, len(html.encode('utf-8')) / 1024 / 1024))
