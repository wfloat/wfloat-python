# wfloat

Low-level Python bindings for Wfloat TTS built from the modified `sherpa-onnx`
source in this monorepo.

This package intentionally exposes the native binding surface directly. Model
download, filesystem cache management, and higher-level client APIs are out of
scope for this package skeleton.

## Scope

- Native `OfflineTts` binding for Wfloat TTS
- Low-level config objects
- Text preparation helpers
- Wave writing helpers

## Build Notes

This package builds against the sibling `sherpa-onnx` source tree in this repo.
It is meant to produce platform-specific wheels that bundle the compiled native
extension inside the `wfloat` package.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel build cmake ninja

# optional override: export WFLOAT_SHERPA_ONNX_SOURCE_DIR=/some/other/sherpa-onnx
python -m build --wheel

# Install the built wheel into the same venv for testing:
python -m pip install dist/*.whl
```

