from ._constants import SPEAKER_IDS, VALID_EMOTIONS, VALID_SIDS
from ._model import Model, load
from ._results import Audio, GenerationResult, Timeline, TimelineChunk
from ._version import __version__

_LOW_LEVEL_EXPORTS = {
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
}


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
__all__.extend(sorted(_LOW_LEVEL_EXPORTS))


def __getattr__(name):
    if name not in _LOW_LEVEL_EXPORTS:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    from . import _bindings

    value = getattr(_bindings, name)
    globals()[name] = value
    return value


def __dir__():
    return sorted(set(globals()) | _LOW_LEVEL_EXPORTS)
