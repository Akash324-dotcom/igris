import time
import ollama

MODEL = "qwen3.5:latest"
OPTIONS = {"num_thread": 4}

with open("system_prompt.txt", "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()


THINK_WORDS = [
    "plan", "solve", "calculate", "debug", "why", "explain",
    "compare", "design", "prove", "step by step", "analyze", "analyse",
]


def needs_thinking(text):
    """Decide whether IGRIS should think before answering."""
    text = text.lower()
    if text.startswith("/think"):    
        return True
    if text.startswith("/fast"):    
        return False
    return any(word in text for word in THINK_WORDS)


def clean(text):
    """Remove /think or /fast from the message before sending it."""
    for tag in ("/think", "/fast"):
        if text.lower().startswith(tag):
            return text[len(tag):].strip()
    return text


messages = [{"role": "system", "content": SYSTEM_PROMPT}]
print("IGRIS is waking up...")

ollama.chat(
    model=MODEL,
    messages=[{"role": "system", "content": SYSTEM_PROMPT},
              {"role": "user", "content": "hi"}],
    think=False,
    options={**OPTIONS, "num_predict": 1},
    keep_alive="30m",
)

print("IGRIS is online. Type 'bye' to exit.")
print("Tip: start with /think to force thinking, or /fast to skip it.\n")

while True:
    user_text = input("You: ")
    if user_text.lower() in ("bye", "exit", "quit"):
        print("IGRIS: Goodbye, Mr. Specter.")
        break

    think = needs_thinking(user_text)
    messages.append({"role": "user", "content": clean(user_text)})

    mode = "THINKING" if think else "FAST"
    print(f"[mode: {mode}]")
    if think:
        print("IGRIS is thinking...", flush=True)

    start = time.time()
    first_word_time = None
    reply = ""
    budget = 1500 if think else 400  

    stream = ollama.chat(
        model=MODEL, messages=messages, stream=True, think=think,
        options={**OPTIONS, "num_predict": budget},
        keep_alive="30m",
    )
    for chunk in stream:
        if chunk.message.thinking:            
            print(".", end="", flush=True)    
        piece = chunk.message.content or ""
        if piece:
            if first_word_time is None:
                first_word_time = time.time() - start
                print("\nIGRIS: ", end="", flush=True)
            print(piece, end="", flush=True)
            reply += piece

    total_time = time.time() - start

    if not reply:
        print("\n[IGRIS ran out of thinking budget. Try /fast or a simpler question.]\n")
        messages.pop()       # remove your unanswered question from the notebook
        continue

    print(f"\n[first word: {first_word_time:.1f}s | total: {total_time:.1f}s]\n")
    messages.append({"role": "assistant", "content": reply})