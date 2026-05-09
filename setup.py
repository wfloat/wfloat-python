#!/usr/bin/env python3

import importlib.util
import os
from pathlib import Path

import setuptools


ROOT_DIR = Path(__file__).resolve().parent


def load_build_support():
    support_path = ROOT_DIR / "_build_support" / "cmake_extension.py"
    spec = importlib.util.spec_from_file_location(
        "wfloat_build_support.cmake_extension", support_path
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load build support module from {support_path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


build_support = load_build_support()
BuildExtension = build_support.BuildExtension
bdist_wheel = build_support.bdist_wheel
cmake_extension = build_support.cmake_extension


def read_long_description() -> str:
    return (ROOT_DIR / "README.md").read_text(encoding="utf8")


def read_package_version() -> str:
    version_file = ROOT_DIR / "python" / "wfloat" / "_version.py"
    namespace = {}
    exec(version_file.read_text(encoding="utf8"), namespace)
    version = namespace.get("__version__")
    if not isinstance(version, str) or not version.strip():
        raise RuntimeError(f"Could not determine package version from {version_file}")

    return version.strip()


def get_sherpa_onnx_source_dir() -> Path:
    env_dir = os.environ.get("WFLOAT_SHERPA_ONNX_SOURCE_DIR")
    if env_dir:
        return Path(env_dir).expanduser().resolve()

    return (ROOT_DIR.parent.parent / "sherpa-onnx").resolve()


setuptools.setup(
    name="wfloat",
    version=read_package_version(),
    description="Low-level Python bindings for Wfloat TTS",
    long_description=read_long_description(),
    long_description_content_type="text/markdown",
    author="wfloat",
    license="MIT",
    python_requires=">=3.8",
    url="https://github.com/wfloat/wfloat",
    package_dir={"": "python"},
    packages=setuptools.find_packages(where="python"),
    package_data={"wfloat": ["lib/*"], "wfloat.lib": ["*"]},
    entry_points={
        "console_scripts": [
            "wfloat=wfloat._cli:main",
        ]
    },
    include_package_data=True,
    ext_modules=[cmake_extension("_sherpa_onnx")],
    cmdclass={"build_ext": BuildExtension, "bdist_wheel": bdist_wheel},
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: C++",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)
