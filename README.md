# wfloat

`wfloat` is the Python package for `wfloat-tts`, Wfloat's on-device English
text-to-speech model.

It runs speech locally in Python instead of calling a hosted inference API.
The model supports 20 voices with emotion and intensity control.

If you're building for the browser, use
[`@wfloat/wfloat-web`](https://github.com/wfloat/wfloat-web). If you're
building for React Native, use
[`@wfloat/react-native-wfloat`](https://github.com/wfloat/react-native-wfloat).

Try it in the browser: https://wfloat.com/demo

[sample.wav](https://github.com/user-attachments/files/27574802/sample.wav)

[Sample dialogue](sample.wav)

## Install

```bash
pip install wfloat
```

## Usage

```python
import wfloat

model = wfloat.load("wfloat/wfloat-tts")

result = model.generate(
    text="No, no, that's not possible. The formula should have crystallized, but it adapted instead. Do you realize what that means for the rest of my work?",
    voice_id="mad_scientist_woman",
    emotion="surprise",
    intensity=0.7,
)

result.audio.save("out.wav")
```

For multi-speaker dialogue:

```python
import wfloat

model = wfloat.load("wfloat/wfloat-tts")

result = model.generate_dialogue(
    segments=[
        {
            "voice_id": "wise_elder_man",
            "text": "Rain taps against the tavern shutters as you step inside.",
            "emotion": "neutral",
            "intensity": 0.5,
        },
        {
            "voice_id": "strong_hero_man",
            "text": "You're late. Two bandits stole the king's map over three hours ago.",
            "emotion": "fear",
            "intensity": 0.6,
        },
        {
            "voice_id": "strong_hero_man",
            "text": "They fled north, up into the woods.",
            "emotion": "neutral",
            "intensity": 0.5,
        },
    ],
    silence_between_segments_sec=0.35,
)

result.audio.save("dialogue.wav")
```

You can also generate a WAV from the command line:

```bash
wfloat generate \
  --text "Hello world!" \
  --out out.wav \
  --voice-id mad_scientist_woman \
  --emotion surprise \
  --intensity 0.7 \
  --silence-padding-sec 0
```

For the full CLI help:

```bash
wfloat generate --help
```

The first load downloads the model assets. After that, the package uses the
cached local copy.

## Speaker IDs

Use `voice_id` string names or numeric `sid` values:

| Speaker | SID |
| --- | ---: |
| `skilled_hero_man` | 0 |
| `skilled_hero_woman` | 1 |
| `fun_hero_man` | 2 |
| `fun_hero_woman` | 3 |
| `strong_hero_man` | 4 |
| `strong_hero_woman` | 5 |
| `mad_scientist_man` | 6 |
| `mad_scientist_woman` | 7 |
| `clever_villain_man` | 8 |
| `clever_villain_woman` | 9 |
| `narrator_man` | 10 |
| `narrator_woman` | 11 |
| `wise_elder_man` | 12 |
| `wise_elder_woman` | 13 |
| `outgoing_anime_man` | 14 |
| `outgoing_anime_woman` | 15 |
| `scary_villain_man` | 16 |
| `scary_villain_woman` | 17 |
| `news_reporter_man` | 18 |
| `news_reporter_woman` | 19 |

## Emotions

Supported emotion labels:

- `neutral`
- `joy`
- `sadness`
- `anger`
- `fear`
- `surprise`
- `dismissive`
- `confusion`

`intensity` must be between `0.0` and `1.0`.

## More

- Docs: https://docs.wfloat.com
- Model card, voices, emotions, and samples: https://huggingface.co/Wfloat/wfloat-tts
- Web package: https://github.com/wfloat/wfloat-web
- React Native package: https://github.com/wfloat/react-native-wfloat
