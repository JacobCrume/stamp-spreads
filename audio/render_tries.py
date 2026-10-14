#!/usr/bin/env python3
"""Three drums-only alternatives to the machine beat.

Each file is 15.0 seconds, instrumental, and uses a different kit.
Does not overwrite audio/stamp-jingle.mp3.
"""

import subprocess
import wave
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
SR = 44100


def lowpass(x, coef):
    y = np.empty_like(x)
    acc = 0.0
    for i, sample in enumerate(x):
        acc += coef * (sample - acc)
        y[i] = acc
    return y


def highpass(x, coef):
    return x - lowpass(x, coef)


def decay(n, curve):
    return np.exp(-np.arange(n) / SR * curve)


def noise(n, rng):
    return rng.normal(0, 1, n)


def write_mp3(bus, path):
    peak = np.max(np.abs(bus))
    if peak == 0:
        raise SystemExit(f"silent mix: {path}")
    bus = np.tanh(bus * 1.4 / peak)
    bus *= 0.45 / np.max(np.abs(bus))
    fade = int(0.012 * SR)
    bus[:, :fade] *= np.linspace(0, 1, fade)
    bus[:, -fade:] *= np.linspace(1, 0, fade)
    pcm = (np.clip(bus.T, -1, 1) * 32767).astype(np.int16)
    wav = Path("/tmp") / (path.stem + ".wav")
    with wave.open(str(wav), "w") as handle:
        handle.setnchannels(2)
        handle.setsampwidth(2)
        handle.setframerate(SR)
        handle.writeframes(pcm.tobytes())
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(wav), "-ar", "44100", "-ac", "2",
         "-c:a", "libmp3lame", "-b:a", "192k", str(path)],
        check=True, capture_output=True,
    )
    probe = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(path)],
        check=True, capture_output=True, text=True,
    )
    raw = subprocess.check_output(
        ["ffmpeg", "-v", "error", "-i", str(path), "-f", "f32le", "-ac", "1", "-"]
    )
    decoded = np.frombuffer(raw, dtype=np.float32)
    print(
        f"{path.name}  {float(probe.stdout.strip()):.3f}s  "
        f"peak {float(np.max(np.abs(decoded))):.2f}"
    )


def place(bus, sample, start, gain, pan):
    start = int(start)
    if start >= bus.shape[1] or gain <= 0:
        return
    sample = np.asarray(sample, dtype=np.float64)
    sample = sample[: bus.shape[1] - start]
    left = np.cos((pan + 1) * np.pi / 4)
    right = np.sin((pan + 1) * np.pi / 4)
    bus[0, start : start + len(sample)] += sample * gain * left
    bus[1, start : start + len(sample)] += sample * gain * right


def empty(seconds):
    return np.zeros((2, int(round(seconds * SR))))


def stomp_kit(rng):
    def stomp():
        n = int(SR * 0.28)
        t = np.arange(n) / SR
        freq = 48 + 70 * np.exp(-t * 18)
        body = np.sin(2 * np.pi * np.cumsum(freq) / SR) * decay(n, 8)
        thud = lowpass(noise(n, rng), 0.08) * decay(n, 22)
        return body * 0.85 + thud * 0.9

    def clap():
        n = int(SR * 0.22)
        burst = highpass(noise(n, rng), 0.35)
        out = np.zeros(n)
        for delay, gain in ((0, 0.5), (int(0.012 * SR), 0.8), (int(0.026 * SR), 1.0)):
            piece = burst * decay(n, 28) * gain
            out[delay:] += piece[: n - delay]
        return out * 0.6

    def tambourine():
        n = int(SR * 0.16)
        t = np.arange(n) / SR
        jingle = sum(np.sin(2 * np.pi * f * t) * decay(n, 40) for f in (3200, 4700, 6100))
        shake = highpass(noise(n, rng), 0.55) * decay(n, 32)
        return jingle * 0.08 + shake * 0.55

    def shaker():
        n = int(SR * 0.05)
        return highpass(noise(n, rng), 0.7) * decay(n, 70) * 0.8

    return {"stomp": stomp(), "clap": clap(), "tam": tambourine(), "shaker": shaker()}


def render_stomp():
    """Foot stomp, hand clap, tambourine. 128 bpm, 8 bars."""
    bpm = 128
    step = 60 / bpm / 4
    bus = empty(8 * 16 * step)
    kit = stomp_kit(np.random.default_rng(7))
    for bar in range(8):
        for i in range(16):
            when = (bar * 16 + i) * step * SR
            if i in (0, 8) or (bar >= 4 and i == 10):
                place(bus, kit["stomp"], when, 1.0, 0.0)
            if i in (4, 12) or (bar >= 5 and i == 14):
                place(bus, kit["clap"], when, 0.85, 0.08)
            if i % 2 == 0:
                place(bus, kit["tam"], when, 0.42 if i % 4 == 0 else 0.28, 0.4)
            place(bus, kit["shaker"], when, 0.18, 0.55)
        if bar == 7:
            for i, g in zip((12, 13, 14, 15), (0.4, 0.55, 0.75, 1.0)):
                place(bus, kit["clap"], (bar * 16 + i) * step * SR, g, 0.1)
    write_mp3(bus, ROOT / "try-stomp.mp3")


def break_kit(rng):
    def kick():
        n = int(SR * 0.40)
        t = np.arange(n) / SR
        freq = 42 + 90 * np.exp(-t * 14)
        body = np.sin(2 * np.pi * np.cumsum(freq) / SR) * decay(n, 6.5)
        return body

    def snare():
        n = int(SR * 0.28)
        t = np.arange(n) / SR
        body = np.sin(2 * np.pi * 178 * t) * decay(n, 18)
        grit = highpass(noise(n, rng), 0.25) * decay(n, 16)
        return body * 0.55 + grit * 0.7

    def hat():
        n = int(SR * 0.06)
        return highpass(noise(n, rng), 0.62) * decay(n, 55)

    def open_hat():
        n = int(SR * 0.22)
        return highpass(noise(n, rng), 0.5) * decay(n, 14) * 0.8

    return {"kick": kick(), "snare": snare(), "hat": hat(), "open": open_hat()}


def render_break():
    """Swung break. Round kick, loose snare, no machine hats. 144 bpm, 9 bars."""
    bpm = 144
    step = 60 / bpm / 4
    swing = 0.016
    bus = empty(9 * 16 * step + swing)
    kit = break_kit(np.random.default_rng(11))
    kicks = {0, 7, 8, 13}
    for bar in range(9):
        for i in range(16):
            when = ((bar * 16 + i) * step + (swing if i % 2 else 0)) * SR
            if i % 2 == 0:
                place(bus, kit["hat"], when, 0.36 if i % 4 == 0 else 0.22, 0.35)
            if i in kicks:
                place(bus, kit["kick"], when, 1.0, 0.0)
            if i in (4, 12):
                place(bus, kit["snare"], when, 0.9, -0.08)
            elif i in (10, 15) and bar % 2 == 1:
                place(bus, kit["snare"], when, 0.22, -0.08)
            if i == 14 and bar not in (0, 8):
                place(bus, kit["open"], when, 0.4, 0.4)
    write_mp3(bus, ROOT / "try-break.mp3")


def perc_kit(rng):
    def tone(freq, length, curve):
        n = int(SR * length)
        t = np.arange(n) / SR
        f = freq * (0.86 + 0.14 * np.exp(-t * 30))
        body = np.sin(2 * np.pi * np.cumsum(f) / SR) * decay(n, curve)
        skin = lowpass(noise(n, rng), 0.2) * decay(n, curve * 2.2)
        return body * 0.8 + skin * 0.35

    def wood():
        n = int(SR * 0.07)
        t = np.arange(n) / SR
        hit = (np.sin(2 * np.pi * 920 * t) + 0.4 * np.sin(2 * np.pi * 1840 * t)) * decay(n, 48)
        return hit

    def shaker():
        n = int(SR * 0.07)
        return highpass(noise(n, rng), 0.58) * decay(n, 46)

    return {
        "low": tone(168, 0.22, 12),
        "slap": tone(310, 0.09, 28),
        "open": tone(210, 0.32, 8),
        "wood": wood(),
        "shaker": shaker(),
    }


def render_percussion():
    """Conga, woodblock, shaker. 112 bpm, 7 bars. Sunny rather than club."""
    bpm = 112
    eighth = 60 / bpm / 2
    bus = empty(7 * 8 * eighth)
    kit = perc_kit(np.random.default_rng(19))
    # Eighths: low, slap, low, open, repeated. Woodblock on the off-eighths.
    cycle = ("low", "slap", "low", "open")
    for bar in range(7):
        for i in range(8):
            when = (bar * 8 + i) * eighth * SR
            voice = "slap" if bar == 5 and i >= 4 else cycle[i % 4]
            gain = 0.95 if voice == "slap" else 0.8
            place(bus, kit[voice], when, gain, -0.15 if voice != "open" else 0.1)
            if i % 2 == 1:
                place(bus, kit["wood"], when, 0.48, 0.45)
            place(bus, kit["shaker"], when, 0.22, 0.5)
            place(bus, kit["shaker"], when + eighth * 0.5 * SR, 0.14, 0.5)
    write_mp3(bus, ROOT / "try-percussion.mp3")


def main():
    render_stomp()
    render_break()
    render_percussion()


if __name__ == "__main__":
    main()
