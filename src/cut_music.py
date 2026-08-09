# Cuts the background music bed out of HEF's highlight film.
#
# The film's soundtrack is one continuous instrumental with no narration
# anywhere (checked on spectrograms across the full 5 minutes), so any stretch
# works musically. The trick here is the loop seam.
#
# A plain <audio loop> jumps from the last sample back to the first, which is
# audible every time round. So the file is built to loop into itself:
#
#   S = source[T0 .. T0+L+X]
#   head = S[0..X]   body = S[X..L]   tail = S[L..L+X]
#   out  = crossfade(tail -> head) ++ body
#
# The file now ENDS on S[L] and BEGINS on S[L] as well, so the wrap point is
# continuous audio rather than a cut, and the crossfade carries it back into
# the body. Result: L seconds that loop indefinitely with no seam.

import subprocess

SRC = 'drive-src.bin'
OUT = 'hef-music.m4a'
T0 = 6.0      # after the opening swell, music fully established
L = 96.0      # loop length
X = 3.0       # crossfade

cmd = [
    'ffmpeg', '-v', 'error', '-y',
    '-ss', str(T0 + L),     '-t', str(X),     '-i', SRC,   # tail
    '-ss', str(T0),         '-t', str(X),     '-i', SRC,   # head
    '-ss', str(T0 + X),     '-t', str(L - X), '-i', SRC,   # body
    '-filter_complex',
    '[0:a]aformat=sample_rates=44100:channel_layouts=stereo[t];'
    '[1:a]aformat=sample_rates=44100:channel_layouts=stereo[h];'
    '[2:a]aformat=sample_rates=44100:channel_layouts=stereo[b];'
    '[t][h]acrossfade=d=%s:c1=tri:c2=tri[x];'
    '[x][b]concat=n=2:v=0:a=1[a]' % X,
    '-map', '[a]', '-vn',
    '-c:a', 'aac', '-b:a', '96k', '-ar', '44100', '-ac', '2',
    '-movflags', '+faststart', OUT,
]
subprocess.run(cmd, check=True)

dur = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                      '-of', 'csv=p=0', OUT], capture_output=True, text=True).stdout.strip()
print('%s  %.1fs' % (OUT, float(dur)))
