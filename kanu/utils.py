import tkinter as tk
from tkinter import font

# https://openai.com/pricing#language-models
def tokens2price(model, task, tokens):
    models = {
        "gpt-3.5-turbo"          : {"prompt": 0.0015, "completion": 0.002},
        "gpt-3.5-turbo-0613"     : {"prompt": 0.0015, "completion": 0.002},
        "gpt-3.5-turbo-16k"      : {"prompt": 0.003,  "completion": 0.004},
        "gpt-3.5-turbo-16k-0613" : {"prompt": 0.003,  "completion": 0.004},
        "gpt-4"                  : {"prompt": 0.03,   "completion": 0.06},
        "gpt-4-0613"             : {"prompt": 0.03,   "completion": 0.06},
        "gpt-4-32k"              : {"prompt": 0.06,   "completion": 0.12},
        "gpt-4-32k-0613"         : {"prompt": 0.06,   "completion": 0.12},
        "text-embedding-ada-002" : {"embedding": 0.0001},
    }
    return models[model][task] / 1000 * tokens

def text2tokens(model, text):
    import tiktoken
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))