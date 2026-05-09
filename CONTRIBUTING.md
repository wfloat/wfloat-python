# Contributing

This package wraps a native `sherpa-onnx` build, so building and publishing it
is a little different from a pure-Python package.

## Prerequisites

You will need:

- Python 3.8+
- `cmake`
- a working C/C++ toolchain
- the `sherpa-onnx` source tree available locally

By default, `setup.py` expects the source tree to live at:

```text
../../sherpa-onnx
```

If your checkout lives somewhere else, set:

```bash
export WFLOAT_SHERPA_ONNX_SOURCE_DIR=/absolute/path/to/sherpa-onnx
```

## Local Setup

Create a virtualenv and install the packaging tools:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install setuptools wheel build twine ninja
```

`ninja` is recommended for faster native builds, but it is not required.

## Build For Local Development

If you just want to compile the native extension locally, run:

```bash
python setup.py build_ext --build-lib ./build-out --build-temp ./build-temp
```

This produces a local install tree under `build-out/` and temporary native build
files under `build-temp/`.

These directories are generated artifacts and should not be committed.

## Build Release Artifacts

For release builds, set `WFLOAT_SHERPA_ONNX_SOURCE_DIR` to an absolute path.
This package's wheel build compiles native code from the sibling
`sherpa-onnx` checkout, and build tools may run parts of the build from a
temporary directory where the default relative path no longer works.

```bash
export WFLOAT_SHERPA_ONNX_SOURCE_DIR=/absolute/path/to/sherpa-onnx
```

To build a release wheel:

```bash
rm -rf build dist
python -m build --wheel --no-isolation
```

That should produce:

- `dist/*.whl`

The package version comes from:

```text
python/wfloat/_version.py
```

Update that file before cutting a new PyPI release.

## CI Wheels

Multi-platform wheels are built in GitHub Actions with `cibuildwheel` via:

```text
.github/workflows/wheels.yml
```

That workflow checks out `wfloat-python`, checks out `wfloat/sherpa-onnx` as a
workspace sibling, and builds wheel artifacts for:

- Linux x86_64
- Windows x86_64
- macOS x86_64
- macOS arm64

The `sherpa-onnx` ref is currently controlled in the workflow file with the
`SHERPA_ONNX_REF` environment variable. It is pinned to a specific commit so CI
rebuilds against a stable native dependency.

The CI workflow intentionally builds wheels only. We should not publish an
sdist until the source-distribution story no longer depends on an external
`sherpa-onnx` checkout.

## Publish To PyPI

1. Build a fresh wheel:

```bash
rm -rf build dist
python -m build --wheel --no-isolation
```

2. Check the generated wheel:

```bash
python -m twine check dist/*
```

3. Upload to PyPI:

```bash
python -m twine upload dist/*
```

If you want to dry-run the process first, upload to TestPyPI:

```bash
python -m twine upload --repository testpypi dist/*
```

## Notes

- The package publishes as `wfloat` on PyPI.
- The CLI entrypoint is also `wfloat`.
- Native builds may download third-party dependencies during the CMake step if
  they are not already available locally.
- `python -m build` without `WFLOAT_SHERPA_ONNX_SOURCE_DIR` may fail because
  the wheel build can run from a temporary unpacked source tree.
- We currently publish wheels, not a self-contained source distribution. The
  source distribution path should only be documented after it no longer depends
  on an external sibling `sherpa-onnx` checkout.
- Release artifacts should be built from a clean tree so generated files do not
  get mixed into the package contents.

## Sanity Checks

Before publishing, it is worth running:

```bash
PYTHONPATH=python python3 -m unittest discover -s tests -v
python -m wfloat --help
```
