try:
    from sherpa_onnx import (
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
        "Failed to import sherpa-onnx. "
        "Install a compatible sherpa-onnx wheel before using wfloat."
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
