import tkinter as tk
from tkinter import font

# https://openai.com/pricing#language-models
def tokens2price(tokens, model, task):
    if model == "gpt-3.5-turbo":
        if task not in ["prompt", "completion"]:
            raise ValueError(f"Invalid task for {model}: {task}")
        if tokens <= 4096:
            if task == "completion":
                return 0.002 / 1000 * tokens
            else:
                return 0.0015 / 1000 * tokens
        elif tokens <= 16384:
            if task == "completion":
                return 0.004 / 1000 * tokens
            else:
                return 0.003 / 1000 * tokens
        else:
            raise ValueError(f"Tokens too large for {model}: {tokens}")
    elif model == "text-embedding-ada-002":
        if task == "embedding":
            return 0.0001 / 1000 * tokens
        else:
            raise ValueError(f"Invalid task for {model}: {task}")
    elif model == "gpt-4":
        if task not in ["prompt", "completion"]:
            raise ValueError(f"Invalid task for {model}: {task}")
        if tokens <= 8192:
            if task == "completion":
                return 0.06 / 1000 * tokens
            else:
                return 0.03 / 1000 * tokens
        elif tokens <= 32768:
            if task == "completion":
                return 0.12 / 1000 * tokens
            else:
                return 0.06 / 1000 * tokens
        else:
            raise ValueError(f"Tokens too large for {model}: {tokens}")
    else:
        raise ValueError(f"Invalid model: {model}")

def text2tokens(model, text):
    import tiktoken
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))