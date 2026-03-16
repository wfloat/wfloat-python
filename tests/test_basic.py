import unittest

try:
    import wfloat
except ImportError as exc:
    wfloat = None
    IMPORT_ERROR = exc
else:
    IMPORT_ERROR = None


class TestWfloatSmoke(unittest.TestCase):
    def test_import_wfloat(self) -> None:
        if IMPORT_ERROR is not None:
            self.fail(
                "Could not import wfloat. Build/install the package first. "
                f"Original error: {IMPORT_ERROR}"
            )

    def test_public_api_exports(self) -> None:
        if IMPORT_ERROR is not None:
            self.skipTest(f"wfloat is not importable yet: {IMPORT_ERROR}")

        expected_exports = {
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
        }

        self.assertTrue(expected_exports.issubset(set(wfloat.__all__)))
        for name in expected_exports:
            self.assertTrue(hasattr(wfloat, name), f"Missing export: {name}")

    def test_version_matches_expected(self) -> None:
        if IMPORT_ERROR is not None:
            self.skipTest(f"wfloat is not importable yet: {IMPORT_ERROR}")

        self.assertEqual(wfloat.version, "1.12.23")


if __name__ == "__main__":
    # unittest.main()

    import wfloat

    model = wfloat.OfflineTtsWfloatModelConfig(
        model="../wfloat-web/assets/models/wfloat-model/1.0.0/wfloat-model-1.0.0.onnx",
        tokens="../wfloat-web/assets/models/wfloat-model/1.0.0/wfloat-model-1.0.0_tokens.txt",
        data_dir="../../sherpa-onnx/wasm/tts/assets/espeak-ng-data",
    )

    tts_model = wfloat.OfflineTtsModelConfig(
        wfloat=model,
        num_threads=1,
        debug=False,
        provider="cpu",
    )

    config = wfloat.OfflineTtsConfig(
        model=tts_model,
        max_num_sentences=1,
    )

    tts = wfloat.OfflineTts(config)
    audio = tts.generate("Hello world.", sid=0, speed=1.0)
    ok = wfloat.write_wave("out.wav", audio.samples, audio.sample_rate)

    print("sample_rate:", audio.sample_rate)
    print("num_samples:", len(audio.samples))
    print("write_wave:", ok)
