import hashlib
import tempfile
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

        if text == "The door is locked.":
            return FakePreparedText(
                text=["The door is locked."],
                text_clean=["door.clean"],
            )

        if text == "Then we open it the loud way.":
            return FakePreparedText(
                text=["Then we open it the loud way."],
                text_clean=["loud.clean"],
            )

        raise AssertionError("Unexpected text in fake native TTS: %s" % text)

    def generate(self, text, sid, speed):
        self.generate_calls.append((text, sid, speed))
        if text == "Hello.clean":
            return FakeGeneratedAudio([0.1, 0.2], self.sample_rate)
        if text == "World.clean":
            return FakeGeneratedAudio([0.3], self.sample_rate)
        if text == "door.clean":
            return FakeGeneratedAudio([0.4, 0.5], self.sample_rate)
        if text == "loud.clean":
            return FakeGeneratedAudio([0.6], self.sample_rate)
        raise AssertionError("Unexpected clean text in fake native TTS: %s" % text)


class TestHighLevelApi(unittest.TestCase):
    def test_top_level_exports_exist(self):
        self.assertTrue(hasattr(wfloat, "load"))
        self.assertTrue(hasattr(wfloat, "Model"))
        self.assertTrue(hasattr(wfloat, "Audio"))
        self.assertTrue(hasattr(wfloat, "GenerationResult"))
        self.assertIn("narrator_woman", wfloat.SPEAKER_IDS)

    def test_audio_can_write_wave_bytes_without_numpy(self):
        audio = Audio(samples=[0.0, 0.5, -0.5], sample_rate=22050)
        wav_bytes = audio.wav_bytes()

        self.assertTrue(wav_bytes.startswith(b"RIFF"))
        self.assertGreater(len(wav_bytes), 44)

    def test_generate_returns_audio_and_timeline(self):
        fake_native_tts = FakeNativeTts(sample_rate=10)
        model = Model("wfloat/wfloat-tts", fake_native_tts)

        result = model.generate(
            text="Hello. World!",
            voice_id="narrator_woman",
            emotion="neutral",
            intensity=0.5,
            speed=1.0,
            silence_padding_sec=0.2,
        )

        self.assertEqual(result.audio.sample_rate, 10)
        self.assertEqual(len(result.timeline.chunks), 2)
        self.assertEqual(result.timeline.chunks[0].highlight_start, 0)
        self.assertEqual(result.timeline.chunks[0].highlight_end, 6)
        self.assertEqual(result.timeline.chunks[1].highlight_start, 6)
        self.assertEqual(result.timeline.chunks[1].highlight_end, 13)
        self.assertAlmostEqual(result.timeline.chunks[0].start_sec, 0.0)
        self.assertAlmostEqual(result.timeline.chunks[0].end_sec, 0.2)
        self.assertAlmostEqual(result.timeline.chunks[1].start_sec, 0.4)
        self.assertAlmostEqual(result.timeline.chunks[1].end_sec, 0.5)
        self.assertAlmostEqual(result.audio.duration_sec, 0.5)
        self.assertEqual(fake_native_tts.generate_calls[0][1], 11)
        self.assertEqual(list(result), [result.audio, result.timeline])

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "out.wav"
            result.audio.save(output_path)
            self.assertTrue(output_path.is_file())

    def test_generate_dialogue_tracks_segment_indices(self):
        fake_native_tts = FakeNativeTts(sample_rate=10)
        model = Model("wfloat/wfloat-tts", fake_native_tts)

        result = model.generate_dialogue(
            segments=[
                {
                    "text": "The door is locked.",
                    "voice_id": "narrator_man",
                    "emotion": "neutral",
                },
                {
                    "text": "Then we open it the loud way.",
                    "voice_id": "strong_hero_woman",
                    "emotion": "joy",
                    "intensity": 0.65,
                },
            ],
            silence_between_segments_sec=0.3,
        )

        self.assertEqual(len(result.timeline.chunks), 2)
        self.assertEqual(result.timeline.chunks[0].segment_index, 0)
        self.assertEqual(result.timeline.chunks[1].segment_index, 1)
        self.assertAlmostEqual(result.timeline.chunks[1].start_sec, 0.5)

    def test_cache_model_assets_downloads_and_extracts_from_local_urls(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            source_dir = root / "source"
            source_dir.mkdir()

            model_file = source_dir / "model.onnx"
            model_file.write_bytes(b"model-bytes")

            tokens_file = source_dir / "tokens.txt"
            tokens_file.write_text("token-bytes")

            espeak_archive = source_dir / "espeak.zip"
            with zipfile.ZipFile(espeak_archive, "w") as archive:
                archive.writestr("espeak-ng-data/voices.txt", "voice-data")

            assets = ModelAssets(
                model_onnx=model_file.as_uri(),
                model_onnx_checksum=sha256_file(model_file),
                model_tokens=tokens_file.as_uri(),
                model_tokens_checksum=sha256_file(tokens_file),
                espeak_data=espeak_archive.as_uri(),
                espeak_checksum=sha256_file(espeak_archive),
            )

            cached = cache_model_assets(
                "wfloat/wfloat-tts",
                assets,
                cache_dir=root / "cache",
            )

            self.assertTrue(cached.model_path.is_file())
            self.assertTrue(cached.tokens_path.is_file())
            self.assertTrue((cached.espeak_data_dir / "voices.txt").is_file())
            self.assertTrue(cached.manifest_path.is_file())
            self.assertEqual(normalize_model_name("wfloat/wfloat-tts"), "wfloat--wfloat-tts")

    def test_persistent_id_is_stored_and_loaded_best_effort(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            cache_dir = Path(tmpdir) / "cache"
            self.assertIsNone(load_persistent_id(cache_dir))
            save_persistent_id("persist-123", cache_dir)
            self.assertEqual(load_persistent_id(cache_dir), "persist-123")

    def test_load_wires_endpoint_cache_and_native_builder(self):
        fake_assets = ModelAssets(
            model_onnx="https://example.com/model.onnx",
            model_onnx_checksum="abc",
            model_tokens="https://example.com/tokens.txt",
            model_tokens_checksum="def",
            espeak_data="https://example.com/espeak.zip",
            espeak_checksum="ghi",
            persistent_id="persist-456",
        )
        fake_cached = CachedModelAssets(
            model_name="wfloat/wfloat-tts",
            cache_dir=Path("/tmp/cache"),
            model_path=Path("/tmp/cache/model.onnx"),
            tokens_path=Path("/tmp/cache/tokens.txt"),
            espeak_data_dir=Path("/tmp/cache/espeak"),
            manifest_path=Path("/tmp/cache/manifest.json"),
        )
        fake_native_tts = FakeNativeTts()

        with tempfile.TemporaryDirectory() as tmpdir:
            cache_dir = Path(tmpdir) / "cache"
            save_persistent_id("persist-123", cache_dir)
            with mock.patch("wfloat._model.fetch_model_assets", return_value=fake_assets) as fetch_mock, mock.patch(
                "wfloat._model.cache_model_assets", return_value=fake_cached
            ), mock.patch("wfloat._model.create_native_tts", return_value=fake_native_tts):
                model = wfloat.load("wfloat/wfloat-tts", cache_dir=cache_dir)

            self.assertIsInstance(model, Model)
            self.assertEqual(model.model_name, "wfloat/wfloat-tts")
            fetch_mock.assert_called_once_with(
                "wfloat/wfloat-tts",
                persistent_id="persist-123",
            )
            self.assertEqual(load_persistent_id(cache_dir), "persist-456")


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
