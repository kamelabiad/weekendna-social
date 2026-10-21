"""Original background music for Weekendna Reels, synthesised from scratch (no samples, so no copyright or licence issues).

Usage: python3 tools/make_music.py <mood> <seconds> <out.wav> [--seed N]
Moods:
  calm     slow fingerpicked guitar + soft pad (mountain guesthouses, nature)
  cozy     warm guitar strum + piano notes (huts, cabins, chalets in winter)
  oud      plucked oud-like melody in a Lebanese/Hijaz flavour over a drone + daf (traditional houses)
  upbeat   bright guitar, bass and light shaker/claps (resorts, pools, clubs)
  lounge   mellow electric-piano chords, bass and soft beat (hotels)
  summer   happy ukulele-style strum, bass and claps (beach, Batroun)
The same mood + seed always gives the same track; a different seed varies the progression and melody.
"""
import sys, wave
import numpy as np

SR = 44100
rng = None

def note(n):  # MIDI number -> Hz
    return 440.0 * 2 ** ((n - 69) / 12)

def env(length, a=0.005, r=None, decay=None):
    t = np.arange(length) / SR
    e = np.minimum(1, t / max(a, 1e-4))
    if decay: e *= np.exp(-t / decay)
    if r:
        rl = min(int(r * SR), length)
        e[-rl:] *= np.linspace(1, 0, rl)
    return e

def pluck(freq, dur, bright=0.5, amp=0.3):
    """Karplus-Strong plucked string (guitar / oud / ukulele)."""
    n = int(dur * SR); p = max(2, int(SR / freq))
    buf = rng.uniform(-1, 1, p)
    if bright < 1:  # soften the attack
        for _ in range(int((1 - bright) * 4)): buf = (buf + np.roll(buf, 1)) / 2
    out = np.empty(n); idx = 0; damp = 0.996 if freq < 300 else 0.994
    for i in range(n):
        v = buf[idx]; nxt = buf[(idx + 1) % p]
        buf[idx] = damp * 0.5 * (v + nxt); out[i] = v; idx = (idx + 1) % p
    return out * amp * env(n, a=0.002, r=0.05)

def keys(freq, dur, amp=0.2, tone="piano"):
    n = int(dur * SR); t = np.arange(n) / SR
    if tone == "rhodes":  # FM electric piano
        mod = np.sin(2 * np.pi * freq * t) * 1.2 * np.exp(-t * 2.5)
        s = np.sin(2 * np.pi * freq * t + mod) + 0.15 * np.sin(2 * np.pi * 2 * freq * t)
        return amp * s * env(n, a=0.004, decay=1.4, r=0.08)
    s = sum(a * np.sin(2 * np.pi * freq * k * t) * np.exp(-t * (1.2 + 0.9 * k)) for k, a in ((1, 1), (2, .45), (3, .2), (4, .1)))
    return amp * s * env(n, a=0.003, r=0.08)

def pad(freqs, dur, amp=0.06):
    n = int(dur * SR); t = np.arange(n) / SR; s = np.zeros(n)
    for f in freqs:
        for d in (-0.15, 0, 0.15):  # slight detune for warmth
            s += np.sin(2 * np.pi * (f + d) * t) + 0.3 * np.sin(2 * np.pi * 2 * (f + d) * t)
    s /= max(1, len(freqs) * 3)
    return amp * s * env(n, a=min(0.8, dur / 3), r=min(0.8, dur / 3))

def bass(freq, dur, amp=0.25):
    n = int(dur * SR); t = np.arange(n) / SR
    s = np.sin(2 * np.pi * freq * t) + 0.25 * np.sin(2 * np.pi * 2 * freq * t)
    return amp * s * env(n, a=0.006, decay=0.6, r=0.05)

def noise_hit(dur, amp, hp=True, decay=0.04):
    n = int(dur * SR); s = rng.uniform(-1, 1, n)
    if hp: s = np.diff(np.concatenate([[0], s]))
    return amp * s * env(n, a=0.001, decay=decay)

def kick(amp=0.5):
    n = int(0.25 * SR); t = np.arange(n) / SR
    f = 50 + 70 * np.exp(-t * 30)
    return amp * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 12)

def daf(amp=0.35, low=True):
    n = int(0.3 * SR); t = np.arange(n) / SR
    body = np.sin(2 * np.pi * (90 if low else 220) * t) * np.exp(-t * (14 if low else 30))
    return amp * (body + 0.25 * noise_hit(0.3, 1, decay=0.03))

def add(track, sig, at):
    i = int(at * SR)
    if i >= len(track): return
    j = min(len(track), i + len(sig)); track[i:j] += sig[: j - i]

def reverb(x, mix=0.25):
    out = x.copy()
    for d, g in ((0.031, .5), (0.047, .4), (0.071, .33), (0.097, .27), (0.131, .2), (0.173, .15)):
        k = int(d * SR); y = np.zeros_like(x); y[k:] = x[:-k] * g; out += mix * y
    return out

# Chord shapes as MIDI root + intervals
MAJ, MIN, MAJ7, MIN7, SUS2 = (0, 4, 7), (0, 3, 7), (0, 4, 7, 11), (0, 3, 7, 10), (0, 2, 7)
PROGS = {  # (root, quality) in a key, each one bar
    "calm": [[(0, MAJ), (7, MAJ), (9, MIN), (5, MAJ)], [(0, SUS2), (5, MAJ7), (9, MIN7), (7, MAJ)], [(9, MIN), (5, MAJ), (0, MAJ), (7, MAJ)]],
    "cozy": [[(0, MAJ7), (9, MIN7), (5, MAJ7), (7, MAJ)], [(0, MAJ), (4, MIN), (5, MAJ), (7, MAJ)]],
    "upbeat": [[(0, MAJ), (7, MAJ), (9, MIN), (5, MAJ)], [(5, MAJ), (0, MAJ), (7, MAJ), (9, MIN)]],
    "lounge": [[(2, MIN7), (7, MAJ), (0, MAJ7), (9, MIN7)], [(5, MAJ7), (4, MIN7), (2, MIN7), (0, MAJ7)]],
    "summer": [[(0, MAJ), (5, MAJ), (7, MAJ), (5, MAJ)], [(0, MAJ), (9, MIN), (5, MAJ), (7, MAJ)]],
}
SETTINGS = {  # bpm, key (MIDI root)
    "calm": (76, 50), "cozy": (84, 52), "oud": (92, 50), "upbeat": (112, 55), "lounge": (96, 50), "summer": (118, 55),
}

def chord_notes(key, root, q, octave=0):
    return [key + root + i + 12 * octave for i in q]

def compose(mood, seconds):
    bpm, key = SETTINGS[mood]
    beat = 60 / bpm; bar = 4 * beat
    total = seconds + 2
    T = np.zeros(int(total * SR))
    if mood == "oud":
        # Hijaz on D: D Eb F# G A Bb C D -- a drone, a daf rhythm (maqsum-like) and a plucked melody.
        scale = [0, 1, 4, 5, 7, 8, 10, 12, 13, 16]
        add(T, pad([note(key - 12), note(key - 5)], total, amp=0.07), 0)
        t = 0.0; pattern = [(0, True), (1, False), (1.5, False), (2, True), (3, False)]
        while t < total:
            for off, low in pattern: add(T, daf(0.28 if low else 0.16, low), t + off * beat)
            t += bar
        t = beat; deg = 0
        phrase = [0, 1, 2, 3, 4, 3, 2, 1]
        while t < total - 1:
            for i, p in enumerate(phrase):
                deg = max(0, min(len(scale) - 1, p + int(rng.integers(-1, 2))))
                f = note(key + 12 + scale[deg]); d = beat * (1 if i % 4 != 3 else 2)
                add(T, pluck(f, d + 0.4, bright=0.7, amp=0.28), t)
                if rng.random() < 0.35: add(T, pluck(f, 0.3, bright=0.7, amp=0.16), t + d / 2)  # oud tremolo flourish
                t += d
            phrase = phrase[::-1] if rng.random() < 0.5 else [p + 1 for p in phrase]
        return reverb(T, 0.3)

    prog = PROGS[mood][int(rng.integers(len(PROGS[mood])))]
    nbars = int(np.ceil(total / bar))
    pentatonic = [0, 2, 4, 7, 9, 12, 14, 16]
    for b in range(nbars):
        root, q = prog[b % len(prog)]
        t0 = b * bar
        notes = chord_notes(key, root, q)
        if mood == "calm":
            add(T, pad([note(n + 12) for n in notes], bar + 0.5, amp=0.05), t0)
            arp = [notes[0] - 12, notes[1], notes[2], notes[1] + 12, notes[2], notes[1]]
            for i in range(8):
                add(T, pluck(note(arp[i % len(arp)]), 1.6, bright=0.5, amp=0.22), t0 + i * beat / 2)
            if b % 2 == 1 and rng.random() < 0.7:
                add(T, keys(note(key + 24 + pentatonic[int(rng.integers(len(pentatonic)))]), 2.0, amp=0.07), t0 + 2 * beat)
        elif mood == "cozy":
            for s, (off, amp) in enumerate(((0, .2), (1.5, .12), (2, .17), (3, .12), (3.5, .1))):
                for k, n in enumerate(sorted(notes + [notes[0] + 12])):
                    add(T, pluck(note(n), 1.2, bright=0.4, amp=amp), t0 + off * beat + k * 0.012)
            add(T, bass(note(key + root - 12), bar * 0.9, amp=0.18), t0)
            for i in range(2):
                if rng.random() < 0.6:
                    add(T, keys(note(key + 24 + pentatonic[int(rng.integers(len(pentatonic)))]), 1.5, amp=0.08), t0 + (i * 2 + 1) * beat)
        elif mood in ("upbeat", "summer"):
            strum = [(0, .2), (1, .14), (1.5, .12), (2.5, .14), (3, .16), (3.5, .1)]
            for off, amp in strum:
                for k, n in enumerate(notes + [notes[0] + 12]):
                    add(T, pluck(note(n + (12 if mood == "summer" else 0)), 0.5, bright=0.8, amp=amp), t0 + off * beat + k * 0.01)
            for i in range(4):
                add(T, bass(note(key + root - 12 + (7 if i % 2 else 0)), beat * 0.8, amp=0.22), t0 + i * beat)
                add(T, kick(0.35), t0 + i * beat) if mood == "upbeat" else None
            for i in range(8): add(T, noise_hit(0.08, 0.05 if i % 2 else 0.03, decay=0.02), t0 + i * beat / 2)  # shaker
            for i in (1, 3): add(T, noise_hit(0.15, 0.16, decay=0.05), t0 + i * beat)  # clap
            if b % 2 == 0:
                for i in range(4):
                    if rng.random() < 0.6:
                        add(T, keys(note(key + 24 + pentatonic[int(rng.integers(len(pentatonic)))]), 0.6, amp=0.07), t0 + i * beat + beat / 2)
        elif mood == "lounge":
            for off in (0, 2.5):
                for n in notes: add(T, keys(note(n + 12), 1.8, amp=0.1, tone="rhodes"), t0 + off * beat)
            for i, off in enumerate((0, 1.5, 2, 3.5)):
                add(T, bass(note(key + root - 12 + (0, 7, 12, 7)[i]), beat * 0.6, amp=0.22), t0 + off * beat)
            for i in range(4):
                if i % 2 == 0: add(T, kick(0.3), t0 + i * beat)
                else: add(T, noise_hit(0.2, 0.08, decay=0.06), t0 + i * beat)
                add(T, noise_hit(0.05, 0.025, decay=0.015), t0 + i * beat + beat / 2)
    return reverb(T, 0.22 if mood in ("calm", "cozy", "lounge") else 0.12)

LOWPASS = {"calm": 5500, "cozy": 6000, "oud": 7000, "lounge": 7000, "upbeat": 10000, "summer": 10000}

def lowpass(x, cutoff):
    """Smooth FFT low-pass (cosine roll-off over one octave) to take the edge off the plucks."""
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    g = np.clip((2 * cutoff - f) / cutoff, 0, 1); g = 0.5 - 0.5 * np.cos(np.pi * g)
    return np.fft.irfft(X * g, len(x))

def master(x, seconds, mood):
    x = lowpass(x[: int(seconds * SR)], LOWPASS[mood])
    fi, fo = int(0.6 * SR), int(1.5 * SR)
    x[:fi] *= np.linspace(0, 1, fi); x[-fo:] *= np.linspace(1, 0, fo)
    x = np.tanh(1.4 * x / (np.max(np.abs(x)) + 1e-9))  # gentle limiter
    return x / (np.max(np.abs(x)) + 1e-9) * 0.7

def write_wav(path, x):
    st = np.stack([x, np.roll(x, int(0.012 * SR)) * 0.96], axis=1)  # tiny stereo width
    with wave.open(path, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((st * 32767).astype("<i2").tobytes())

if __name__ == "__main__":
    a = sys.argv[1:]
    mood, seconds, out = a[0], float(a[1]), a[2]
    seed = int(a[a.index("--seed") + 1]) if "--seed" in a else 7
    if mood not in SETTINGS: sys.exit(f"mood must be one of {', '.join(SETTINGS)}")
    rng = np.random.default_rng(seed)
    write_wav(out, master(compose(mood, seconds), seconds, mood))
    print("wrote", out)
