import tkinter as tk

import google.generativeai as palm

from .gui import Settings, Conversation

class ChatPaLM:
    def __init__(self, kanu, google_key, model, temperature, prompt):
        self.kanu = kanu
        self.model = model
        self.temperature = temperature
        self.prompt = prompt
        palm.configure(api_key=google_key)
        self.settings = Settings(self)
        self.conversation = Conversation(self)
        self.tokens = 0
        self.price = 0

    def run(self):
        self.conversation.page()

    def send_message(self):
        self.messages += [{"author": '0', "content": self.user_input.get()}]
        response = palm.chat(
            model=f"models/{self.model}",
            messages=self.messages,
            temperature=self.temperature, 
            context=self.prompt,
        )
        self.messages += [{"author": '1', "content": response.last}]
        self.session.insert(tk.END, "You: " + self.user_input.get() + "\n", "user")
        self.session.insert(tk.END, f"Bot: " + response.last + "\n", "bot")
        self.chatbox.delete(0, tk.END)
        self.system.insert(tk.END, f"System: Communicated with PaLM API.\n", "system")

    def clear_session(self):
        self.tokens = self.price = 0
        self.run()