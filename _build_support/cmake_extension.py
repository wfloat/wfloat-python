# Derived from sherpa-onnx/cmake/cmake_extension.py and adapted for the
# standalone wfloat Python package.

import os
import platform
import shlex
import shutil
import subprocess
import sys
from pathlib import Path

import setuptools
from setuptools.command.build_ext import build_ext


def is_windows() -> bool:
    return platform.system() == "Windows"


try:
    from wheel.bdist_wheel import bdist_wheel as _bdist_wheel

    class bdist_wheel(_bdist_wheel):
        def finalize_options(self):
            _bdist_wheel.finalize_options(self)
            self.root_is_pure = False

except ImportError:
    bdist_wheel = None


def cmake_extension(name, *args, **kwargs) -> setuptools.Extension:
    kwargs["language"] = "c++"
    return setuptools.Extension(name, sources=[], *args, **kwargs)


def _get_repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _get_sherpa_onnx_source_dir() -> Path:
    env_dir = os.environ.get("WFLOAT_SHERPA_ONNX_SOURCE_DIR")
    if env_dir:
        source_dir = Path(env_dir).expanduser().resolve()
    else:
        source_dir = (_get_repo_root() / "sherpa-onnx").resolve()

    if not source_dir.is_dir():
        raise RuntimeError(
            f"Could not find sherpa-onnx source tree at {source_dir}. "
            "Set WFLOAT_SHERPA_ONNX_SOURCE_DIR to override."
        )

    return source_dir


def _run(cmd):
    print("Running:", " ".join(cmd))
    subprocess.run(cmd, check=True)


class BuildExtension(build_ext):
    def build_extension(self, ext: setuptools.extension.Extension):
        del ext

        build_temp = Path(self.build_temp).resolve()
        build_lib = Path(self.build_lib).resolve()
        install_dir = build_lib / "wfloat"
        source_dir = _get_sherpa_onnx_source_dir()

        build_temp.mkdir(parents=True, exist_ok=True)
        build_lib.mkdir(parents=True, exist_ok=True)

        user_cmake_args = shlex.split(os.environ.get("SHERPA_ONNX_CMAKE_ARGS", ""))
        default_cmake_args = [
            "-DCMAKE_BUILD_TYPE=Release",
            f"-DCMAKE_INSTALL_PREFIX={install_dir}",
            "-DBUILD_SHARED_LIBS=ON",
            "-DBUILD_PIPER_PHONMIZE_EXE=OFF",
            "-DBUILD_PIPER_PHONMIZE_TESTS=OFF",
            "-DBUILD_ESPEAK_NG_EXE=OFF",
            "-DBUILD_ESPEAK_NG_TESTS=OFF",
            "-DSHERPA_ONNX_ENABLE_C_API=OFF",
            "-DSHERPA_ONNX_BUILD_C_API_EXAMPLES=OFF",
            "-DSHERPA_ONNX_ENABLE_CHECK=OFF",
            "-DSHERPA_ONNX_ENABLE_PYTHON=ON",
            "-DSHERPA_ONNX_ENABLE_TTS=ON",
            "-DSHERPA_ONNX_ENABLE_BINARY=OFF",
            "-DSHERPA_ONNX_ENABLE_PORTAUDIO=OFF",
        ]

        if not any(arg.startswith("-DPYTHON_EXECUTABLE=") for arg in user_cmake_args):
            default_cmake_args.append(f"-DPYTHON_EXECUTABLE={sys.executable}")

        configure_cmd = [
            "cmake",
            *default_cmake_args,
            *user_cmake_args,
            "-B",
            str(build_temp),
            "-S",
            str(source_dir),
        ]

        build_cmd = ["cmake", "--build", str(build_temp), "--target", "install"]
        if is_windows():
            build_cmd.extend(["--config", "Release"])

        parallel_level = os.environ.get("CMAKE_BUILD_PARALLEL_LEVEL")
        if parallel_level:
            build_cmd.extend(["--parallel", parallel_level])
        else:
            build_cmd.extend(["--parallel", "4"])

        _run(configure_cmd)
        _run(build_cmd)

        # Keep only the runtime files that belong inside the Python package.
        for extra_dir in ("bin", "include", "share"):
            candidate = install_dir / extra_dir
            if candidate.is_dir():
                shutil.rmtree(candidate)

        pkgconfig_dir = install_dir / "lib" / "pkgconfig"
        if pkgconfig_dir.is_dir():
            shutil.rmtree(pkgconfig_dir)
