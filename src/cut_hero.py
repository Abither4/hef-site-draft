# Cuts the hero loop out of HEF's highlight film.
#
# Rules baked in: no title cards, no caption overlays, no aerial or
# compound-layout shots, and no photo-montage segments -- only live footage.
# Every clip below was checked frame by frame against the film's scene cuts
# so none of them run into a card.

#
# Two files come out of this. The phone one is cut from the ORIGINAL source
# rather than transcoded from the desktop file -- re-compressing an already
# compressed video costs bits to reproduce its artefacts, which made the
# small file bigger than the job needed.

import subprocess

SRC = 'drive-src.bin'
XF = 0.6      # crossfade
FPS = 24

# (output, extra filter, crf) -- the phone build is cropped to the 4:3 block
# it actually sits in, so no bits are spent on pixels the layout throws away.
BUILDS = [
    ('hef-hero.mp4',    'scale=1280:720',                        33),
    ('hef-hero-sm.mp4', 'crop=in_w*0.75:in_h,scale=640:480',     35),
]

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

for out, vf, crf in BUILDS:
    cmd = ['ffmpeg', '-v', 'error', '-y']
    for s, d, _ in SHOTS:
        cmd += ['-ss', str(s), '-t', str(d), '-i', SRC]

    parts = []
    for i in range(len(SHOTS)):
        parts.append('[%d:v]fps=%d,%s,setsar=1,format=yuv420p[c%d]' % (i, FPS, vf, i))

    acc = SHOTS[0][1]
    prev = 'c0'
    for i in range(1, len(SHOTS)):
        parts.append('[%s][c%d]xfade=transition=fade:duration=%s:offset=%.2f[x%d]'
                     % (prev, i, XF, acc - XF, i))
        acc = acc + SHOTS[i][1] - XF
        prev = 'x%d' % i

    # Fading both ends to black makes the loop seam invisible.
    parts.append('[%s]fade=t=in:st=0:d=0.6,fade=t=out:st=%.2f:d=0.6[v]' % (prev, acc - 0.6))

    # Baseline profile on the phone build: the widest possible decoder support.
    profile = 'baseline' if 'sm' in out else 'main'
    cmd += ['-filter_complex', ';'.join(parts), '-map', '[v]', '-an',
            '-c:v', 'libx264', '-crf', str(crf), '-preset', 'slow',
            '-profile:v', profile, '-level', '3.1', '-pix_fmt', 'yuv420p', '-g', '48',
            '-movflags', '+faststart', out]

    subprocess.run(cmd, check=True)
    print('%-16s %d shots, %.1fs' % (out, len(SHOTS), acc))
