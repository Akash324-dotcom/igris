# IGRIS

> 🚧 **Work in progress — being built in public.** This repo is public on purpose so anyone can follow along as IGRIS is built step by step. Expect frequent changes, rough edges and features that aren't finished yet.

**An offline personal AI assistant that runs entirely on a laptop.**

IGRIS runs a local large language model through [Ollama](https://ollama.com). After setup, no internet connection, cloud API or API key is needed. Everything stays on the machine.

> Status: **v0.1, early development.** A terminal chat assistant for now. Voice, gestures and Android TV control are planned (see the roadmap).

---

## Features (v0.1)

- **Fully offline:** runs a local model (Qwen 3.5) through Ollama.
- **Custom personality:** behaviour is defined in an editable `system_prompt.txt` (tone, honesty rules, no pretending to take actions it can't).
- **Conversation memory:** remembers everything said earlier in the current session.
- **Auto-think mode:** detects "hard" questions (plan, solve, debug, compare...) and switches reasoning on automatically; normal chat stays fast.
  - `/think` forces reasoning on
  - `/fast` forces it off
- **Streaming replies:** words appear as they are generated.
- **Latency tracking:** every reply prints time-to-first-word and total time.
- **Laptop-friendly:** a capped CPU thread count and output budget keep the machine from overheating, and a warm-up at startup plus `keep_alive` keep the model loaded between messages.

## Requirements

- Python 3.10+
- [Ollama](https://ollama.com/download) installed and running
- A local model, e.g.:
  ```
  ollama pull qwen3.5
  ```
- Tested on: Intel Core i5-12500H, 16 GB RAM, integrated graphics only (no GPU), Windows

## Setup

```bash
git clone https://github.com/Akash324-dotcom/igris.git
cd igris
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS / Linux
pip install -r requirements.txt
```

Make sure Ollama is running (open the Ollama app or run `ollama serve`), then:

```bash
python igris.py
```

## Usage

```
You: hi
[mode: FAST]
IGRIS: Hello, Mr. Specter. How can I help?
[first word: 2.6s | total: 14.3s]

You: plan a 1 hour study session
[mode: THINKING]
...
```

Type `bye` to exit.

## Configuration

| Setting | Where | What it does |
|---|---|---|
| `MODEL` | `igris.py` | Which Ollama model to use |
| `OPTIONS["num_thread"]` | `igris.py` | CPU threads (lower = cooler, slower) |
| `THINK_WORDS` | `igris.py` | Words that trigger reasoning mode |
| Personality and rules | `system_prompt.txt` | How IGRIS talks and behaves |

## Findings so far (CPU-only laptop)

- The first reply after a cold start can take ~50s while the model loads and reads the system prompt; replies later in the same conversation start in a few seconds.
- The model's native "thinking" mode is very expensive on CPU: on a simple quadratic equation it used its full 1,500-token budget without reaching an answer. Next step: replace it with visible step-by-step prompting and compare the latency.
- Running on all CPU cores at full boost caused thermal shutdowns, which is why threads are capped at 4.

## Roadmap

- [x] Local LLM chat loop with personality
- [x] Auto-think mode and latency tracking
- [ ] Steps mode (visible step-by-step reasoning instead of hidden thinking)
- [ ] Long-term memory that persists between sessions
- [ ] Tools (open apps, read files) with confirmation before risky actions
- [ ] Offline voice: Whisper (speech-to-text) and Piper (text-to-speech)
- [ ] Custom hand-gesture recognition model (MediaPipe landmarks and a self-trained classifier)
- [ ] Android TV control via adb, then a native Kotlin TV app
- [ ] LoRA fine-tuning for more reliable tool selection

## License

MIT. See [LICENSE](LICENSE).
