# Adds the August photo batch to assets.json.
#
# Every image is re-encoded through PIL with no exif= argument, which is what
# actually strips EXIF/GPS -- see the publication rules in the repo README.
# Sizes are deliberately small: the whole page ships as one self-contained
# HTML file, so every kilobyte here is a kilobyte of first paint.

import base64, io, json, os
import numpy as np
from PIL import Image


def trim_black(im):
    """Several of these came out of a video editor with letterbox bars baked
    in. Cover-cropping a tile does not remove them, so cut them here."""
    a = np.asarray(im).max(2)
    rows = np.where(a.max(1) > 26)[0]
    cols = np.where(a.max(0) > 26)[0]
    if not len(rows) or not len(cols):
        return im
    box = (int(cols[0]), int(rows[0]), int(cols[-1]) + 1, int(rows[-1]) + 1)
    return im if box == (0, 0, im.width, im.height) else im.crop(box)

DL = r'C:\Users\andre\Downloads'
HERE = os.path.dirname(os.path.abspath(__file__))

# key -> (filename, max width, quality, optional crop box)
NEW = {
    # portrait feature
    'boy':      ('unnamed (1).jpg',  1000, 76, None),
    # who we are, second photo
    'walk':     ('unnamed (9).jpg',   820, 70, None),
    # wide banners
    'church':   ('unnamed (6).jpg',  1300, 64, (0, 188, 2048, 1340)),
    'doorwide': ('unnamed (8).jpg',  1300, 66, None),
    # gallery tiles
    'wave':     ('unnamed (4).jpg',   820, 72, None),
    'pink':     ('unnamed (7).jpg',   820, 72, None),
    'toddler':  ('unnamed (14).png',  820, 72, None),
    'juice':    ('unnamed (13).png',  820, 72, None),
    'rice':     ('unnamed.jpg',       820, 72, None),
    'elderman':   ('unnamed (3).jpg',   700, 70, None),
    'group':    ('unnamed (5).jpg',   820, 72, None),
}

assets = json.load(open(os.path.join(HERE, 'assets.json')))
added = 0
for key, (name, maxw, q, box) in NEW.items():
    im = Image.open(os.path.join(DL, name))
    im = im.convert('RGB')
    if box:
        im = im.crop(box)
    im = trim_black(im)
    if im.width > maxw:
        im = im.resize((maxw, round(im.height * maxw / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, 'JPEG', quality=q, optimize=True, progressive=True)
    data = buf.getvalue()

    # Confirm the re-encode really dropped the metadata before we ship it.
    check = Image.open(io.BytesIO(data))
    assert not check.getexif(), 'EXIF survived in %s' % name
    assert b'GPS' not in data[:4096], 'GPS marker in %s' % name

    assets[key] = 'data:image/jpeg;base64,' + base64.b64encode(data).decode()
    print('%-11s %-20s %4dx%-4d %6.1f KB' % (key, name, im.width, im.height, len(data) / 1024))
    added += 1

json.dump(assets, open(os.path.join(HERE, 'assets.json'), 'w'))
total = sum(len(v) for v in assets.values()) / 1024 / 1024
print('\n%d added, %d assets, %.2f MB of base64 total' % (added, len(assets), total))
