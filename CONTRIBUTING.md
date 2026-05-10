# Contributing

`wfloat` is now a pure Python package. Native code comes from a separately
installed `sherpa-onnx` wheel.

## Prerequisites

- Python 3.9+
- a compatible `sherpa-onnx` wheel available from GitHub Releases or another
  package source

## Local setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install setuptools wheel build twine
```

Install `sherpa-onnx` first if you want to exercise the low-level bindings:

```bash
pip install https://github.com/wfloat/sherpa-onnx/releases/download/<tag>/<wheel>.whl
```

Then install `wfloat`:

```bash
pip install -e .
```

## Build release artifacts

```bash
rm -rf build dist
python -m build
```

That produces:

- `dist/*.whl`
- `dist/*.tar.gz`

## Tests

Unit tests do not require `sherpa-onnx`:

```bash
python -m unittest discover -s tests -v
```

If you have installed a compatible `sherpa-onnx` wheel, you can also run a
simple smoke check:

```bash
python -c "import sherpa_onnx, wfloat; print(wfloat.__version__)"
```

## CI

CI now:

- builds pure Python artifacts once
- installs those artifacts on each target platform
- runs the unit test suite

After `sherpa-onnx` release assets are published, CI can add a platform-specific
install step that pulls those wheel URLs before running integration smoke tests.
