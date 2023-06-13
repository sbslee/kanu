import tkinter as tk

import openai

from .utils import Settings, tokens2price

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
        self.kanu.container.pack()
        l = tk.Label(self.kanu.container, text="ChatGPT")
        l.grid(row=0, column=0, columnspan=4)
        self.system = tk.Text(self.kanu.container, width=80, height=7)
        self.system.tag_configure("system", **self.settings.get_system_kwargs())
        self.system.insert(tk.END, "System: A new chat session has been created.\n", "system")
        self.system.grid(row=1, column=0, columnspan=4)
        self.session = tk.Text(self.kanu.container, width=80, height=20)
        self.session.grid(row=2, column=0, columnspan=4)
        self.session.tag_config("user", **self.settings.get_user_kwargs())
        self.session.tag_config("bot", **self.settings.get_bot_kwargs())
        user_input = tk.Entry(self.kanu.container, width=62)
        user_input.grid(row=3, column=0, columnspan=4)
        self.messages = []
        b = tk.Button(self.kanu.container, text="Send", command=lambda: self.send_message(user_input))
        b.grid(row=4, column=0)
        b = tk.Button(self.kanu.container, text="Clear", command=lambda: self.clear_session())
        b.grid(row=4, column=1)
        b = tk.Button(self.kanu.container, text="Go back", command=lambda: self.kanu.config_chatgpt())
        b.grid(row=4, column=2)
        b = tk.Button(self.kanu.container, text="Settings", command=lambda: self.settings.page())
        b.grid(row=4, column=3)

    def send_message(self, entry):
        if not self.messages:
            self.messages.append({"role": "system", "content": self.prompt})
        self.messages += [{"role": "user", "content": entry.get()}]
        bot_response = openai.ChatCompletion.create(
            model=self.model,
            messages=self.messages,
            temperature=self.temperature,
        )
        response = bot_response["choices"][0]["message"]["content"]
        self.messages += [{"role": "assistant", "content": response}]
        self.session.insert(tk.END, "You: " + entry.get() + "\n", "user")
        self.session.insert(tk.END, f"Bot: " + response + "\n", "bot")
        usage = self.calculate_usage(bot_response)
        self.system.insert(tk.END, f"{usage}\n", "system")
        entry.delete(0, tk.END)

    def calculate_usage(self, response):
        total_tokens = response["usage"]["total_tokens"]
        prompt_tokens = response["usage"]["prompt_tokens"]
        completion_tokens = response["usage"]["completion_tokens"]
        prompt_price = tokens2price(prompt_tokens, self.model, "prompt")
        completion_price = tokens2price(completion_tokens, self.model, "completion")
        self.price += prompt_price + completion_price
        self.tokens += total_tokens
        message = f"System: Used {prompt_tokens:,} prompt + {completion_tokens:,} completion = {total_tokens:,} tokens (total: {self.tokens:,} or ${self.price:.6f})."
        return message

    def clear_session(self):
        self.run()