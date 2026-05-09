# wfloat

`wfloat` is the Python package for loading Wfloat-compatible speech models and
generating audio files with `sherpa-onnx` under the hood.

The intended high-level flow is:

```python
import wfloat

model = wfloat.load("wfloat/wfloat-tts")

result = model.generate(
    text="The signal is clean. Start the recording.",
    voice_id="narrator_woman",
    emotion="neutral",
    intensity=0.5,
    speed=1.0,
)

result.audio.save("out.wav")

print(result.audio.sample_rate)
print(result.timeline.chunks[0].start_sec)
```

## Status

The package now contains the high-level Python API shape:

- `wfloat.load(...)`
- `model.generate(...)`
- `model.generate_dialogue(...)`
- `result.audio.save(...)`
- timing metadata via `result.timeline`

The Python model asset endpoint still needs to return Python-compatible asset
metadata for live downloads to work end to end.

## CLI

The package also exposes a `wfloat` CLI:

```bash
wfloat synth --text "Hello world." --out out.wav
```

## Notes

- The package is designed to cache model assets locally.
- Voice IDs can be passed as strings such as `narrator_woman` or as numeric
  speaker IDs.
- The public API is intentionally high-level; low-level native config objects
  are not the primary integration surface.

More implementation detail lives in [DESIGN.md](./DESIGN.md).
