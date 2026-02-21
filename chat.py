# uses the OpenAI library as the local LLM is OpenAI compatible
from openai import OpenAI

# api_key is dummy value
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

history = []

print("Chat with your local LLM (type 'quit' or 'exit' to stop, 'clear' to reset history)\n")

while True:
    try:
        # blocks until the user hits Enter, returns what they typed; .strip() — removes leading/trailing whitespace
        user_input = input("You: ").strip()
        # Ctrl-C / Ctrl-D
    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye!")
        break

    if not user_input:
        continue
    if user_input.lower() in ("quit", "exit"):
        print("Goodbye!")
        break
    if user_input.lower() == "clear":
        history.clear()
        print("History cleared.\n")
        continue

    history.append({"role": "user", "content": user_input})

    # With stream=True, the response comes back in chunks as tokens are generated — like watching text being typed in real time
    # response is a generator that yields one chunk at a time as they arrive
    # each chunk is a ChatCompletionChunk
    # ChatCompletionChunk
    # ├── id: str
    # ├── model: str
    # ├── created: int
    # └── choices: list[Choice]
    #     └── [0]
    #         ├── index: int
    #         ├── finish_reason: str | None   # "stop" on the last chunk, None otherwise
    #         └── delta: ChoiceDelta
    #             ├── role: str | None        # "assistant" on first chunk, None after
    #             └── content: str | None     # the actual text token, None on first/last

    response = client.chat.completions.create(
        model="liquid/lfm2.5-1.2b",
        messages=history,
        stream=True,
    )

    # end="" overrides the default newline 
    # flush=True forces it to write to the terminal immediately, without waiting.
    print("Assistant: ", end="", flush=True)
    reply = ""
    for chunk in response:
        delta = chunk.choices[0].delta.content or ""
        print(delta, end="", flush=True)
        reply += delta
    print("\n")

    history.append({"role": "assistant", "content": reply})
