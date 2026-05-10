# Contributing

`wfloat` is a pure Python package. Native code comes from the
`wfloat-sherpa-onnx` dependency, which provides `import sherpa_onnx`.

## Prerequisites

- Python 3.9+

## Local setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install setuptools wheel build twine
```

Install `wfloat`:

```bash
pip install -e .
```

That will also install the matching `wfloat-sherpa-onnx` dependency.

## Build release artifacts

```bash
rm -rf build dist
python -m build
```

That produces:

- `dist/*.whl`
- `dist/*.tar.gz`

## Tests

Unit tests do not require `sherpa_onnx`:

```bash
python -m unittest discover -s tests -v
```

You can also run a smoke check:

```bash
python -c "import sherpa_onnx, wfloat; print(wfloat.__version__)"
```

## CI

CI now:

- builds pure Python artifacts once
- installs those artifacts on each target platform
- relies on normal dependency resolution for `wfloat-sherpa-onnx`
- runs the unit test suite and an integration smoke test
