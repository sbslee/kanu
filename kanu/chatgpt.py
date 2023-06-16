import tkinter as tk

import openai

from .gui import Settings
from .utils import tokens2price

class ChatGPT:
    def __init__(self, kanu, openai_key, model, temperature, prompt):
        self.kanu = kanu
        self.model = model
        self.temperature = temperature
        self.prompt = prompt
        openai.api_key = openai_key
        self.settings = Settings(self)
        self.tokens = 0
        self.price = 0

    def run(self):
        self.kanu.container.pack_forget()
        self.kanu.container = tk.Frame(self.kanu.root)
        self.kanu.container.pack(fill="both", expand=True)
        self.kanu.container.bind_all("<Return>", lambda event: self.send_message())
        self.kanu.container.focus_set()
        l = tk.Label(self.kanu.container, text="ChatGPT")
        l.grid(row=0, column=0, columnspan=4, sticky="ew")
        self.system = tk.Text(self.kanu.container, height=7)
        self.system.tag_configure("system", **self.settings.get_system_kwargs())
        self.system.insert(tk.END, f"System: A new chat session has been created using {self.model}.\n", "system")
        self.system.grid(row=1, column=0, columnspan=4, sticky="ew")
        self.session = tk.Text(self.kanu.container)
        self.session.grid(row=2, column=0, columnspan=4, sticky="nsew")
        self.session.tag_config("user", **self.settings.get_user_kwargs())
        self.session.tag_config("bot", **self.settings.get_bot_kwargs())
        self.user_input = tk.StringVar()
        self.chatbox = tk.Entry(self.kanu.container, textvariable=self.user_input)
        self.chatbox.grid(row=3, column=0, columnspan=4, sticky="ew")
        self.messages = []
        button_frame = tk.Frame(self.kanu.container)
        button_frame.grid(row=4, column=0, sticky="ew")
        b = tk.Button(button_frame, text="Send", command=lambda: self.send_message())
        b.grid(row=0, column=0, sticky="ew")
        b = tk.Button(button_frame, text="Clear", command=lambda: self.clear_session())
        b.grid(row=0, column=1, sticky="ew")
        b = tk.Button(button_frame, text="Go back", command=lambda: self.kanu.config_chatgpt())
        b.grid(row=0, column=2, sticky="ew")
        b = tk.Button(button_frame, text="Settings", command=lambda: self.settings.page())
        b.grid(row=0, column=3, sticky="ew")
        self.kanu.container.grid_columnconfigure(0, weight=1)
        self.kanu.container.grid_rowconfigure(2, weight=1)
        for i in range(4):
            button_frame.grid_columnconfigure(i, weight=1)

    def send_message(self):
        if not self.messages:
            self.messages.append({"role": "system", "content": self.prompt})
        self.messages += [{"role": "user", "content": self.user_input.get()}]
        bot_response = openai.ChatCompletion.create(
            model=self.model,
            messages=self.messages,
            temperature=self.temperature,
        )
        response = bot_response["choices"][0]["message"]["content"]
        self.messages += [{"role": "assistant", "content": response}]
        self.session.insert(tk.END, "You: " + self.user_input.get() + "\n", "user")
        self.session.insert(tk.END, f"Bot: " + response + "\n", "bot")
        usage = self.calculate_usage(bot_response)
        self.system.insert(tk.END, f"{usage}\n", "system")
        self.chatbox.delete(0, tk.END)

    def calculate_usage(self, response):
        total_tokens = response["usage"]["total_tokens"]
        prompt_tokens = response["usage"]["prompt_tokens"]
        completion_tokens = response["usage"]["completion_tokens"]
        prompt_price = tokens2price(self.model, "prompt", prompt_tokens)
        completion_price = tokens2price(self.model, "completion", completion_tokens)
        self.price += prompt_price + completion_price
        self.tokens += total_tokens
        message = f"System: Used {prompt_tokens:,} prompt + {completion_tokens:,} completion = {total_tokens:,} tokens (total: {self.tokens:,} or ${self.price:.6f})."
        return message

    def clear_session(self):
        self.tokens = self.price = 0
        self.run()