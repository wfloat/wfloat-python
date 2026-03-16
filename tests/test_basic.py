import unittest
import json
from pathlib import Path

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

    print(wfloat.version)

    SPEAKER_IDS = {
        "skilled_hero_man": 0,
        "skilled_hero_woman": 1,
        "fun_hero_man": 2,
        "fun_hero_woman": 3,
        "strong_hero_man": 4,
        "strong_hero_woman": 5,
        "mad_scientist_man": 6,
        "mad_scientist_woman": 7,
        "clever_villain_man": 8,
        "clever_villain_woman": 9,
        "narrator_man": 10,
        "narrator_woman": 11,
        "wise_elder_man": 12,
        "wise_elder_woman": 13,
        "outgoing_anime_man": 14,
        "outgoing_anime_woman": 15,
        "scary_villain_man": 16,
        "scary_villain_woman": 17,
        "news_reporter_man": 18,
        "news_reporter_woman": 19,
    }

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

    voices_path = "../../web/assets/js/voices.js"  # string path to the JSON file
    with open(voices_path, "r", encoding="utf-8") as f:
        voices_text = f.read()
    prefix = "export const VOICES = "
    voices_text = voices_text[len(prefix) :]

    voices = json.loads(voices_text)
    out_dir = Path("out")
    out_dir.mkdir(exist_ok=True)
    progress_by_voice = {}

    for v in voices:
        sid = SPEAKER_IDS[v["voiceId"]]
        silence_padding_sec = v["padding"]
        speed = v["speed"]
        final_samples = []
        sample_rate = None
        raw_text_cursor = 0
        current_time_sec = 0.0
        progress_events = []

        prepared = tts.prepare_wfloat_text(
            v["text"],
            emotion=v["emotion"],
            intensity=v["intensity"],
        )

        for i in range(len(prepared.text)):
            audio = tts.generate(prepared.text_clean[i], sid=sid, speed=speed)
            if sample_rate is None:
                sample_rate = audio.sample_rate
            elif sample_rate != audio.sample_rate:
                raise ValueError(
                    f"Sample rate changed for {v['voiceId']}: "
                    f"{sample_rate} != {audio.sample_rate}"
                )

            raw_chunk_text = prepared.text[i] or ""
            highlight_start = raw_text_cursor
            highlight_end = raw_text_cursor + len(raw_chunk_text)
            raw_text_cursor = highlight_end

            chunk_duration_sec = len(audio.samples) / sample_rate
            padding_sec = silence_padding_sec if i < len(prepared.text) - 1 else 0.0
            start_time_sec = current_time_sec
            end_time_sec = start_time_sec + chunk_duration_sec + padding_sec

            progress_events.append(
                {
                    "text": raw_chunk_text,
                    "progress": (i + 1) / len(prepared.text),
                    "textHighlightStart": highlight_start,
                    "textHighlightEnd": highlight_end,
                    "startTimeSec": start_time_sec,
                    "endTimeSec": end_time_sec,
                }
            )

            final_samples.extend(audio.samples)
            current_time_sec += chunk_duration_sec

            if i < len(prepared.text) - 1:
                silence_samples = int(sample_rate * silence_padding_sec)
                final_samples.extend([0] * silence_samples)
                current_time_sec += silence_padding_sec

        output_path = out_dir / f"{v['voiceId']}.wav"
        ok = wfloat.write_wave(str(output_path), final_samples, sample_rate)
        progress_by_voice[v["voiceId"]] = progress_events
        print(f"{output_path}: sample_rate={sample_rate} num_samples={len(final_samples)} write_wave={ok}")

    progress_path = out_dir / "progress.json"
    with open(progress_path, "w", encoding="utf-8") as f:
        json.dump(progress_by_voice, f, ensure_ascii=False, indent=2)
