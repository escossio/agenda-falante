from __future__ import annotations

import wave
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class WavInfo:
    channels: int
    sample_width: int
    frame_rate: int
    n_frames: int


def _read_wav(path: str | Path) -> tuple[WavInfo, bytes]:
    wav_path = Path(path)
    if not wav_path.exists():
        raise FileNotFoundError(f"Segment does not exist: {wav_path}")
    if wav_path.suffix.lower() != ".wav":
        raise ValueError(f"Segment is not a WAV file: {wav_path}")

    try:
        with wave.open(str(wav_path), "rb") as handle:
            info = WavInfo(
                channels=handle.getnchannels(),
                sample_width=handle.getsampwidth(),
                frame_rate=handle.getframerate(),
                n_frames=handle.getnframes(),
            )
            frames = handle.readframes(handle.getnframes())
    except wave.Error as exc:
        raise ValueError(f"Invalid WAV file: {wav_path}") from exc
    return info, frames


def compose_wav_segments(segments: list[str | Path], output_path: str | Path) -> dict[str, object]:
    if not segments:
        raise ValueError("At least one WAV segment is required.")

    resolved_segments = [Path(segment) for segment in segments]
    infos: list[WavInfo] = []
    frames_list: list[bytes] = []

    for segment_path in resolved_segments:
        info, frames = _read_wav(segment_path)
        infos.append(info)
        frames_list.append(frames)

    first = infos[0]
    for index, info in enumerate(infos[1:], start=2):
        if info.channels != first.channels:
            raise ValueError(f"Incompatible channel count at segment {index}: {info.channels} != {first.channels}")
        if info.sample_width != first.sample_width:
            raise ValueError(f"Incompatible sample width at segment {index}: {info.sample_width} != {first.sample_width}")
        if info.frame_rate != first.frame_rate:
            raise ValueError(f"Incompatible frame rate at segment {index}: {info.frame_rate} != {first.frame_rate}")

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    total_frames = 0
    with wave.open(str(output), "wb") as handle:
        handle.setnchannels(first.channels)
        handle.setsampwidth(first.sample_width)
        handle.setframerate(first.frame_rate)
        for info, frames in zip(infos, frames_list, strict=True):
            handle.writeframes(frames)
            total_frames += info.n_frames

    duration_seconds = total_frames / float(first.frame_rate) if first.frame_rate else 0.0
    return {
        "segments_count": len(resolved_segments),
        "output_path": str(output),
        "duration_seconds": duration_seconds,
        "sample_rate": first.frame_rate,
        "channels": first.channels,
        "sample_width": first.sample_width,
    }

