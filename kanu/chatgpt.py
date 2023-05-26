import tkinter as tk

import openai

class ChatGPT:
    def __init__(self, kanu, openai_key):
        self.kanu = kanu
        self.kanu.container.pack_forget()
        self.kanu.container = tk.Frame(self.kanu.root)
        self.kanu.container.pack()
        openai.api_key = openai_key

    def run(self):
        title_label = tk.Label(self.kanu.container, text="ChatGPT")
        title_label.grid(row=0, column=0, columnspan=3)
        self.model = tk.StringVar(self.kanu.container, value="gpt-3.5-turbo")
        model_label = tk.Label(self.kanu.container, text="Model:")
        model_label.grid(row=1, column=0)
        model1_button = tk.Radiobutton(self.kanu.container, variable=self.model, text="gpt-3.5-turbo", value="gpt-3.5-turbo")
        model2_button = tk.Radiobutton(self.kanu.container, variable=self.model, text="gpt-4", value="gpt-4")
        model1_button.grid(row=1, column=1)
        model2_button.grid(row=1, column=2)
        session_label = tk.Label(self.kanu.container, text="Chat session")
        session_label.grid(row=2, column=0, columnspan=3)
        self.session = tk.Text(self.kanu.container, width=70, height=20)
        self.session.grid(row=3, column=0, columnspan=3)
        entry = tk.Entry(self.kanu.container, width=54)
        entry.grid(row=4, column=0, columnspan=3)
        self.messages = []
        send_button = tk.Button(self.kanu.container, text="Send", command=lambda: self._send_message(entry))
        send_button.grid(row=5, column=0)
        clear_butoon = tk.Button(self.kanu.container, text="Clear", command=lambda: self._clear_session())
        clear_butoon.grid(row=5, column=1)
        back_button = tk.Button(self.kanu.container, text="Go back", command=lambda: self.kanu.chatgpt_config())
        back_button.grid(row=5, column=2)

    def _send_message(self, entry):
        if not self.messages:
            self.messages.append({"role": "system", "content": "You are a helpful assistant."})
        self.messages += [{"role": "user", "content": entry.get()}]
        bot_response = openai.ChatCompletion.create(
            model=self.model.get(),
            messages=self.messages,
        )
        response = bot_response["choices"][0]["message"]["content"]
        self.messages += [{"role": "assistant", "content": response}]
        self.session.insert(tk.END, "You: " + entry.get() + "\n")
        self.session.insert(tk.END, f"Bot ({self.model.get()}): " + response + "\n")
        entry.delete(0, tk.END)

    def _clear_session(self):
        self.session.delete(1.0, tk.END)
        self.messages.clear()