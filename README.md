# wfloat

`wfloat` is a high-level Python wrapper around `sherpa-onnx` for loading
Wfloat-compatible speech models and generating audio files.

## Install

Install a compatible `sherpa-onnx` wheel first, then install `wfloat`:

```bash
pip install https://github.com/wfloat/sherpa-onnx/releases/download/<tag>/<wheel>.whl
pip install ./packages/wfloat-python
```

## Usage

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
```

## Notes

- `wfloat` does not build or bundle native libraries.
- Low-level bindings come from the installed `sherpa-onnx` wheel.
- The public API is intentionally high-level; low-level native config objects
  are re-exported only for advanced use.
