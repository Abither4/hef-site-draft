# Cuts the hero loop out of HEF's highlight film.
#
# Rules baked in: no title cards, no caption overlays, no aerial or
# compound-layout shots, and no photo-montage segments -- only live footage.
# Every clip below was checked frame by frame against the film's scene cuts
# so none of them run into a card.

import subprocess

SRC = 'drive-src.bin'
OUT = 'hef-hero.mp4'
XF = 0.6      # crossfade
FPS = 24
CRF = 33      # it lives under a dark scrim, so this holds up

# (start, duration, what it is)
SHOTS = [
    (97.8,  2.5, 'kids crossing the schoolyard'),
    (106.5, 2.7, 'two girls laughing'),
    (112.1, 3.5, 'blue-uniform class at their desks'),
    (43.0,  4.5, 'orchard'),
    (138.3, 7.0, 'preschoolers eating, coloured bowls'),
    (182.4, 3.4, 'kids holding up their drawings'),
    (155.9, 4.4, 'teacher serving the meal'),
    (49.8,  4.6, 'banana grove'),
]

cmd = ['ffmpeg', '-v', 'error', '-y']
for s, d, _ in SHOTS:
    cmd += ['-ss', str(s), '-t', str(d), '-i', SRC]

parts = []
for i in range(len(SHOTS)):
    parts.append('[%d:v]fps=%d,scale=1280:720,setsar=1,format=yuv420p[c%d]' % (i, FPS, i))

acc = SHOTS[0][1]
prev = 'c0'
for i in range(1, len(SHOTS)):
    off = acc - XF
    tag = 'x%d' % i
    parts.append('[%s][c%d]xfade=transition=fade:duration=%s:offset=%.2f[%s]'
                 % (prev, i, XF, off, tag))
    acc = acc + SHOTS[i][1] - XF
    prev = tag

# Fading both ends to black makes the loop seam invisible.
parts.append('[%s]fade=t=in:st=0:d=0.6,fade=t=out:st=%.2f:d=0.6[v]' % (prev, acc - 0.6))

cmd += ['-filter_complex', ';'.join(parts), '-map', '[v]', '-an',
        '-c:v', 'libx264', '-crf', str(CRF), '-preset', 'slow',
        '-profile:v', 'main', '-pix_fmt', 'yuv420p', '-g', '48',
        '-movflags', '+faststart', OUT]

subprocess.run(cmd, check=True)
print('%d shots, %.1fs' % (len(SHOTS), acc))
