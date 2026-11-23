"""Seam metrics for a 4 s WAV (2 s before + 2 s after the loop point, seam at frame 88200 unless given).
gap60/gap40: longest run of frames quieter than -60/-40 dBFS (peak of both channels) that touches the seam
(+-10 ms), in ms (capped by the 4 s window: 2 s each side). dip: quietest 50 ms RMS within +-1 s of the seam minus the median 50 ms RMS of the whole 4 s (dB).
step: largest sample jump across the seam vs. the 99.9th percentile jump elsewhere (a click shows step >> typical).
usage: measure.py label file.wav [seam_frame] ..."""
import sys
import numpy as np

SR = 44100


def read_wav(path):
    b = open(path, 'rb').read()
    i = 12
    fmt = None
    while i < len(b):
        cid, sz = b[i:i + 4], int.from_bytes(b[i + 4:i + 8], 'little')
        if cid == b'fmt ':
            fmt = int.from_bytes(b[i + 8:i + 10], 'little'), int.from_bytes(b[i + 10:i + 12], 'little'), int.from_bytes(b[i + 22:i + 24], 'little')
        if cid == b'data':
            d = b[i + 8:i + 8 + sz]
            tag, ch, bits = fmt
            x = np.frombuffer(d, '<f4') if tag == 3 else np.frombuffer(d, '<i2').astype(np.float32) / 32768.0
            return x.reshape(-1, ch)
        i += 8 + sz + (sz & 1)
    raise ValueError(path)


def db(v):
    return 20 * np.log10(max(float(v), 1e-9))


def longest_quiet_run(peak, thr, lo, hi):
    quiet = peak < thr
    best = 0
    i = 0
    n = len(peak)
    while i < n:
        if quiet[i]:
            j = i
            while j < n and quiet[j]:
                j += 1
            if j > lo and i < hi:
                best = max(best, j - i)
            i = j
        else:
            i += 1
    return best


def metrics(x, seam):
    peak = np.abs(x).max(axis=1)
    lo, hi = seam - SR // 100, seam + SR // 100  # the quiet run that touches the seam (+-10 ms)
    gap60 = longest_quiet_run(peak, 10 ** (-60 / 20), lo, hi) * 1000 / SR
    gap40 = longest_quiet_run(peak, 10 ** (-40 / 20), lo, hi) * 1000 / SR
    w = SR // 20
    hop = SR // 200
    rms = np.array([np.sqrt(np.mean(x[i:i + w].astype(np.float64) ** 2)) for i in range(0, len(x) - w, hop)])
    centers = np.arange(0, len(x) - w, hop) + w // 2
    near = np.abs(centers - seam) <= SR
    dip = db(rms[near].min()) - db(np.median(rms))
    d = np.abs(np.diff(x, axis=0)).max(axis=1)
    step = d[seam - 1] if 0 < seam <= len(d) else 0.0
    typical = np.percentile(np.delete(d, range(max(seam - 3, 0), seam + 3)), 99.9)
    return gap60, gap40, dip, step, typical


def main():
    a = sys.argv[1:]
    label, path = a[0], a[1]
    seam = int(a[2]) if len(a) > 2 else 2 * SR
    x = read_wav(path)
    g60, g40, dip, step, typ = metrics(x, seam)
    print(f"{label:10s} gap<-60dB {g60:7.1f} ms  gap<-40dB {g40:7.1f} ms  dip {dip:6.1f} dB  "
          f"seam step {step:.4f} (p99.9 elsewhere {typ:.4f})")


main()
