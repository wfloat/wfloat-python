from ._constants import SPEAKER_IDS, VALID_EMOTIONS, VALID_SIDS
from ._model import Model, load
from ._results import Audio, GenerationResult, Timeline, TimelineChunk
from ._version import __version__

_LOW_LEVEL_IMPORT_ERROR = None

try:
    from ._bindings import (
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
    _LOW_LEVEL_IMPORT_ERROR = exc


__all__ = [
    "Audio",
    "GenerationResult",
    "Model",
    "SPEAKER_IDS",
    "Timeline",
    "TimelineChunk",
    "VALID_EMOTIONS",
    "VALID_SIDS",
    "load",
]

if _LOW_LEVEL_IMPORT_ERROR is None:
    __all__.extend(
        [
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
    )
