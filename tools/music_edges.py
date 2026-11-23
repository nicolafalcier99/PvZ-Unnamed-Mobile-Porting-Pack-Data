#!/usr/bin/env python3
"""Measure each lawnbgm mp3: Xing/LAME header (encoder delay/padding), leading/trailing near-silence
(decoded with mpg123 CLI, gapless on, native rate), and the seam jump if looped as-is."""
import struct, subprocess, sys, os, glob
import numpy as np

ASSETS = sys.argv[1]

def id3_size(b):
    if b[:3] == b'ID3':
        s = b[6:10]
        return 10 + ((s[0] << 21) | (s[1] << 14) | (s[2] << 7) | s[3]) + (10 if b[5] & 0x10 else 0)
    return 0

def lame_info(path):
    b = open(path, 'rb').read(1 << 20)
    off = id3_size(b)
    # find first frame sync
    while off < len(b) - 4 and not (b[off] == 0xFF and (b[off+1] & 0xE0) == 0xE0):
        off += 1
    h = b[off:off+4]
    ver = (h[1] >> 3) & 3; ch = (h[3] >> 6) & 3
    side = (32 if ch != 3 else 17) if ver == 3 else (17 if ch != 3 else 9)
    x = off + 4 + side
    tag = b[x:x+4]
    if tag not in (b'Xing', b'Info'):
        vb = b[off+36:off+40]
        return {'tag': 'VBRI' if vb == b'VBRI' else 'none'}
    flags = struct.unpack('>I', b[x+4:x+8])[0]
    p = x + 8
    frames = None
    if flags & 1: frames = struct.unpack('>I', b[p:p+4])[0]; p += 4
    if flags & 2: p += 4
    if flags & 4: p += 100
    if flags & 8: p += 4
    enc = b[p:p+9]
    r = {'tag': tag.decode(), 'frames': frames, 'encoder': enc.decode('latin1', 'replace')}
    if enc[:4] in (b'LAME', b'Lavf', b'Lavc', b'GOGO') or enc[:1].isalpha():
        d = b[p+21:p+24]
        r['delay'] = (d[0] << 4) | (d[1] >> 4)
        r['padding'] = ((d[1] & 0xF) << 8) | d[2]
    return r

def decode(path, gapless=True):
    args = ['mpg123', '-q', '-s', '-e', 'f32']
    if not gapless: args.append('--no-gapless')
    out = subprocess.run(args + [path], capture_output=True, check=True).stdout
    return np.frombuffer(out, dtype='<f4').reshape(-1, 2)

def rate_of(path):
    o = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'a:0', '-show_entries', 'stream=sample_rate',
                        '-of', 'csv=p=0', path], capture_output=True, text=True).stdout.strip()
    return int(o)

def edge_silence(x, thr):
    a = np.abs(x).max(axis=1)
    nz = np.nonzero(a > thr)[0]
    if len(nz) == 0: return len(x), len(x)
    return int(nz[0]), int(len(x) - 1 - nz[-1])

def rms_db(x):
    r = np.sqrt(np.mean(np.square(x, dtype=np.float64))) if len(x) else 0
    return 20 * np.log10(max(r, 1e-9))

def main():
    files = sorted(glob.glob(os.path.join(ASSETS, 'lawnbgm(*).mp3')), key=lambda p: int(p.split('(')[1].split(')')[0]))
    for f in files:
        n = os.path.basename(f)
        sr = rate_of(f)
        li = lame_info(f)
        x = decode(f)
        lead60, trail60 = edge_silence(x, 10 ** (-60 / 20))
        lead40, trail40 = edge_silence(x, 10 ** (-40 / 20))
        ms = lambda s: f"{1000 * s / sr:.1f}"
        w = int(0.05 * sr)
        print(f"{n:16s} sr={sr} frames={len(x)} ({len(x)/sr:.3f}s) hdr={li}")
        print(f"   lead silence <-60dB: {lead60} ({ms(lead60)} ms)  <-40dB: {lead40} ({ms(lead40)} ms)")
        print(f"   trail silence <-60dB: {trail60} ({ms(trail60)} ms)  <-40dB: {trail40} ({ms(trail40)} ms)")
        print(f"   RMS last 50ms {rms_db(x[-w:]):.1f} dB, first 50ms {rms_db(x[:w]):.1f} dB, "
              f"last 2s {rms_db(x[-2*sr:]):.1f} dB, first 2s {rms_db(x[:2*sr]):.1f} dB; "
              f"seam step |x[0]-x[-1]| = {np.abs(x[0]-x[-1]).max():.4f}")

main()
