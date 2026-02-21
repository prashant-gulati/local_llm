# local_llm

A minimal terminal chat interface for local LLMs via [LM Studio](https://lmstudio.ai). No data leaves your machine.

> "LM Studio is essentially a polished GUI wrapper around llama.cpp"

## How it works

`chat.py` connects to LM Studio's local server (OpenAI-compatible API on `localhost:1234`) and streams responses token-by-token. Conversation history is maintained in memory for the duration of the session.

## Requirements

- [LM Studio](https://lmstudio.ai) with a model downloaded and server running
- Python 3.8+

## Setup

```bash
# Virtual environment
python3 -m venv .venv
source .venv/bin/activate
mkdir -p .vscode && cat > .vscode/settings.json << 'EOF'
{
    "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python"
}
EOF

# Install requirements
pip install -r requirements.txt

# Github
gh repo create local_llm --public --source=. --remote=origin --push
```

## Usage

```bash
python chat.py
```

| Command | Action |
|---|---|
| Type a message + Enter | Chat with the LLM |
| `clear` | Reset conversation history |
| `quit` / `exit` | Exit |
| `Ctrl-C` / `Ctrl-D` | Exit |

## LM Studio CLI reference

```bash
lms server start                                          # start the local server
lms server stop                                           # stop the server
lms server status                                         # check if server is running
lms ls                                                    # list downloaded models
lms ps                                                    # list loaded models and RAM usage
lms get <model-name>                                      # download a model
lms load <model-name>                                     # load a model into memory
lms unload <model-name>                                   # unload a model
ps -o pid,rss,comm -p $(pgrep -f "LM Studio" | head -1)  # check RAM usage (in KB)
```

## Notes

- The OpenAI library is used as the client — LM Studio's API is OpenAI-compatible, so no Anthropic/OpenAI account is needed
- The `api_key` field is required by the library but ignored by LM Studio (any value works)
- Conversation history grows unbounded per session — if you hit the model's context limit, type `clear` to reset
- On Apple Silicon, prefer MLX model variants over GGUF for better performance
