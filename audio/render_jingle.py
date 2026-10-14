#!/usr/bin/env python3
"""Render a drums-only Stamp sting.

Ten bars at 160 bpm is 15.0 seconds. Numpy builds the kit. ffmpeg writes
the mp3. There is no lyric and no speech engine.
"""

import subprocess
import wave
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "stamp-jingle.mp3"
WAV = Path("/tmp/stamp-jingle.wav")

SR = 44100
BPM = 160
BARS = 10
STEPS = 16
STEP = 60.0 / BPM / 4
DURATION = BARS * STEPS * STEP  # 15.0 s

RNG = np.random.default_rng(20261001)


def env(n, curve):
    t = np.arange(n) / SR
    return np.exp(-t * curve)


def kick():
    n = int(SR * 0.32)
    t = np.arange(n) / SR
    freq = 46 + (168 - 46) * np.exp(-t * 32)
    phase = 2 * np.pi * np.cumsum(freq) / SR
    body = np.sin(phase) * env(n, 9.5)
    click = np.sin(2 * np.pi * 1650 * t) * env(n, 240)
    punch = np.sin(2 * np.pi * 80 * t) * env(n, 28)
    return body * 1.05 + click * 0.28 + punch * 0.35


def snare():
    n = int(SR * 0.20)
    t = np.arange(n) / SR
    noise = np.diff(RNG.normal(0, 1, n), prepend=0.0)
    noise *= env(n, 26)
    body = np.sin(2 * np.pi * 196 * t) * env(n, 34)
    snap = np.sin(2 * np.pi * 3200 * t) * env(n, 180)
    return noise * 0.72 + body * 0.42 + snap * 0.18


def clap():
    n = int(SR * 0.16)
    out = np.zeros(n)
    noise = np.diff(RNG.normal(0, 1, n), prepend=0.0)
    for delay, gain in ((0, 0.55), (int(0.011 * SR), 0.85), (int(0.023 * SR), 1.0)):
        burst = noise * env(n, 38) * gain
        out[delay:] += burst[: n - delay]
    return out * 0.55


def hat(opened=False):
    dur = 0.18 if opened else 0.045
    n = int(SR * dur)
    t = np.arange(n) / SR
    noise = np.diff(RNG.normal(0, 1, n), prepend=0.0)
    metal = (
        np.sign(np.sin(2 * np.pi * 5840 * t))
        + 0.6 * np.sign(np.sin(2 * np.pi * 8120 * t))
    )
    curve = 14 if opened else 78
    return (noise * 0.65 + metal * 0.22) * env(n, curve)


def tom(freq):
    n = int(SR * 0.26)
    t = np.arange(n) / SR
    f = freq * (0.72 + 0.28 * np.exp(-t * 24))
    phase = 2 * np.pi * np.cumsum(f) / SR
    body = np.sin(phase) * env(n, 11)
    click = np.diff(RNG.normal(0, 1, n), prepend=0.0) * env(n, 90)
    return body * 0.9 + click * 0.18


def crash():
    n = int(SR * 1.35)
    t = np.arange(n) / SR
    noise = np.diff(RNG.normal(0, 1, n), prepend=0.0)
    metal = sum(np.sign(np.sin(2 * np.pi * f * t)) for f in (4200, 6100, 8700))
    return (noise * 0.5 + metal * 0.12) * env(n, 3.4) * 0.7


def place(bus, sample, start, gain, pan):
    """pan is -1 (left) to +1 (right). Constant-power."""
    start = int(start)
    if start >= bus.shape[1] or gain <= 0:
        return
    sample = sample[: bus.shape[1] - start]
    left = np.cos((pan + 1) * np.pi / 4)
    right = np.sin((pan + 1) * np.pi / 4)
    bus[0, start : start + len(sample)] += sample * gain * left
    bus[1, start : start + len(sample)] += sample * gain * right


def step_time(bar, step):
    """Light swing: off-16ths sit a little late."""
    swing = 0.010 if step % 2 else 0.0
    return (bar * STEPS + step) * STEP + swing


def main():
    n = int(round(DURATION * SR))
    bus = np.zeros((2, n), dtype=np.float64)
    kit = {
        "kick": kick(),
        "snare": snare(),
        "clap": clap(),
        "hat": hat(False),
        "open": hat(True),
        "crash": crash(),
        "tom_hi": tom(240),
        "tom_mid": tom(170),
        "tom_lo": tom(118),
    }

    # 16th-note grids. Kick pushes off the grid; snare holds 2 and 4.
    kick_main = {0, 3, 6, 8, 11}
    snare_main = {4, 12}
    ghost = {7, 15}
    open_hat = {6, 14}

    for bar in range(BARS):
        fill = bar == 7
        ending = bar == 9
        hat_gain = 0.34 if bar == 0 else 0.46
        kick_gain = 0.78 if bar == 0 else 0.98
        for step in range(STEPS):
            when = step_time(bar, step) * SR
            accent = 1.0 if step % 4 == 0 else 0.62
            if not (ending and step >= 8):
                place(bus, kit["hat"], when, hat_gain * accent, 0.35)
            if step in open_hat and not fill and not ending:
                place(bus, kit["open"], when, 0.40, 0.45)
            if fill:
                # Snare roll, louder toward the last step.
                roll = 0.35 + 0.65 * (step / 15)
                place(bus, kit["snare"], when, 0.55 * roll, -0.15)
                if step in (0, 4, 8, 12):
                    drum = ("tom_hi", "tom_mid", "tom_lo", "tom_lo")[step // 4]
                    place(bus, kit[drum], when, 0.72, -0.4 + 0.25 * (step // 4))
            if ending and step == 0:
                place(bus, kit["crash"], when, 0.85, 0.1)
            kicks = {0, 8} if bar == 0 or fill or ending else kick_main
            if step in kicks:
                place(bus, kit["kick"], when, kick_gain, 0.0)
            if not fill and step in snare_main and not (ending and step == 12):
                place(bus, kit["snare"], when, 0.82, -0.12)
                place(bus, kit["clap"], when, 0.48, 0.05)
            if not fill and not ending and step in ghost:
                place(bus, kit["snare"], when, 0.16, -0.12)

    # Soft clip, then a 12 ms fade so the file does not click.
    peak = np.max(np.abs(bus))
    bus *= 1.7 / peak
    bus = np.tanh(bus) 
    # Leave headroom. The mp3 encoder overshoots a hot peak.
    bus *= 0.45 / np.max(np.abs(bus))
    fade = int(0.012 * SR)
    bus[:, :fade] *= np.linspace(0, 1, fade)
    bus[:, -fade:] *= np.linspace(1, 0, fade)

    pcm = np.clip(bus.T, -1, 1)
    pcm = (pcm * 32767).astype(np.int16)
    with wave.open(str(WAV), "w") as handle:
        handle.setnchannels(2)
        handle.setsampwidth(2)
        handle.setframerate(SR)
        handle.writeframes(pcm.tobytes())

    subprocess.run(
        [
            "ffmpeg", "-y", "-i", str(WAV),
            "-ar", "44100", "-ac", "2",
            "-c:a", "libmp3lame", "-b:a", "192k",
            str(OUT),
        ],
        check=True,
        capture_output=True,
    )
    probe = subprocess.run(
        [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=nw=1:nk=1",
            str(OUT),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    print(f"wrote {OUT}")
    print(f"duration {float(probe.stdout.strip()):.3f}s")
    print(f"wav peak {np.max(np.abs(bus)):.3f}")


if __name__ == "__main__":
    main()
