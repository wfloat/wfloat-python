# wfloat

`wfloat` is a high-level Python wrapper around `sherpa-onnx` for loading
Wfloat-compatible speech models and generating audio files.

## Install

Install `wfloat` normally:

```bash
pip install wfloat
```

That will also install the matching `wfloat-sherpa-onnx` dependency from PyPI.

When installing from this repo locally:

```bash
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
- Low-level bindings come from the installed `wfloat-sherpa-onnx` dependency,
  which provides `import sherpa_onnx`.
- The public API is intentionally high-level; low-level native config objects
  are re-exported only for advanced use.
