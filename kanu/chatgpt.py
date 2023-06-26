import tkinter as tk

import openai

from .gui import Settings, Conversation
from .utils import tokens2price

class ChatGPT:
    def __init__(self, kanu, openai_key, model, temperature, prompt):
        self.kanu = kanu
        self.model = model
        self.temperature = temperature
        self.prompt = prompt
        openai.api_key = openai_key
        self.settings = Settings(self)
        self.conversation = Conversation(self)
        self.tokens = 0
        self.price = 0

    def run(self):
        self.conversation.page()

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
        self.calculate_usage(bot_response)
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
        self.system.insert(tk.END, f"{message}\n", "system")

    def clear_session(self):
        self.tokens = self.price = 0
        self.run()