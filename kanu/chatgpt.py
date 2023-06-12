import tkinter as tk

import openai

from .utils import Settings, Tokenizer

class ChatGPT:
    def __init__(self, kanu, openai_key, model, temperature, prompt):
        self.kanu = kanu
        self.model = model
        self.temperature = temperature
        self.prompt = prompt
        openai.api_key = openai_key
        self.settings = Settings(self)
        self.tokenizer = Tokenizer(model)

    def run(self):
        self.kanu.container.pack_forget()
        self.kanu.container = tk.Frame(self.kanu.root)
        self.kanu.container.pack()
        l = tk.Label(self.kanu.container, text="ChatGPT")
        l.grid(row=0, column=0, columnspan=4)
        self.session = tk.Text(self.kanu.container, width=70, height=20)
        self.session.grid(row=1, column=0, columnspan=4)
        self.session.tag_config("user", **self.settings.get_user_kwargs())
        self.session.tag_config("bot", **self.settings.get_bot_kwargs())
        user_input = tk.Entry(self.kanu.container, width=54)
        user_input.grid(row=2, column=0, columnspan=4)
        self.messages = []
        b = tk.Button(self.kanu.container, text="Send", command=lambda: self.send_message(user_input))
        b.grid(row=3, column=0)
        b = tk.Button(self.kanu.container, text="Clear", command=lambda: self.clear_session())
        b.grid(row=3, column=1)
        b = tk.Button(self.kanu.container, text="Go back", command=lambda: self.kanu.config_chatgpt())
        b.grid(row=3, column=2)
        b = tk.Button(self.kanu.container, text="Settings", command=lambda: self.settings.page())
        b.grid(row=3, column=3)
        self.tally = tk.Text(self.kanu.container, width=22, height=1)
        self.tally.grid(row=4, column=0, columnspan=4)
        self.tally.configure(background="gray93", foreground="red")

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
        self.tokenizer.add(entry.get())
        self.tally.delete(1.0, tk.END)
        self.tally.insert(tk.END, f"Tokens: {self.tokenizer.total} (${self.tokenizer.cost()})\n")
        entry.delete(0, tk.END)

    def clear_session(self):
        self.session.delete(1.0, tk.END)
        self.messages.clear()
        self.tally.delete(1.0, tk.END)