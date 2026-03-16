try:
    from wfloat.lib._sherpa_onnx import (
        GeneratedAudio,
        GenerationConfig,
        OfflineTts,
        OfflineTtsConfig,
        OfflineTtsModelConfig,
        OfflineTtsWfloatModelConfig,
        WfloatPreparedText,
        git_date,
        git_sha1,
        prepare_wfloat_text,
        version,
        write_wave,
    )
except ImportError as exc:
    raise ImportError(
        "Failed to import the wfloat native extension. "
        "Build the package from this repo or install a wheel for your platform."
    ) from exc


__all__ = [
    "GeneratedAudio",
    "GenerationConfig",
    "OfflineTts",
    "OfflineTtsConfig",
    "OfflineTtsModelConfig",
    "OfflineTtsWfloatModelConfig",
    "WfloatPreparedText",
    "git_date",
    "git_sha1",
    "prepare_wfloat_text",
    "version",
    "write_wave",
]

