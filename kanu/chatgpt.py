import tkinter as tk

import openai

class ChatGPT:
    def __init__(self, kanu, openai_key, model, temperature, prompt):
        self.kanu = kanu
        self.model = model
        self.temperature = temperature
        self.prompt = prompt
        openai.api_key = openai_key

    def run(self):
        self.kanu.container.pack_forget()
        self.kanu.container = tk.Frame(self.kanu.root)
        self.kanu.container.pack()
        l = tk.Label(self.kanu.container, text="ChatGPT")
        l.grid(row=0, column=0, columnspan=3)
        self.session = tk.Text(self.kanu.container, width=70, height=20)
        self.session.grid(row=1, column=0, columnspan=3)
        e = tk.Entry(self.kanu.container, width=54)
        e.grid(row=2, column=0, columnspan=3)
        self.messages = []
        b = tk.Button(self.kanu.container, text="Send", command=lambda: self.send_message(e))
        b.grid(row=3, column=0)
        b = tk.Button(self.kanu.container, text="Clear", command=lambda: self.clear_session())
        b.grid(row=3, column=1)
        b = tk.Button(self.kanu.container, text="Go back", command=lambda: self.kanu.config_chatgpt())
        b.grid(row=3, column=2)

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
        self.session.insert(tk.END, "You: " + entry.get() + "\n")
        self.session.insert(tk.END, f"Bot: " + response + "\n")
        entry.delete(0, tk.END)

    def clear_session(self):
        self.session.delete(1.0, tk.END)
        self.messages.clear()