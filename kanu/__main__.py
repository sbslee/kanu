import tkinter as tk
from tkinter import messagebox, font

import openai

from .version import __version__

def get_input(entry):
    user_input = entry.get()
    openai.api_key = user_input

def send_message(chat_log, entry, messages):
    if openai.api_key is None:
        messagebox.showerror("Error", "OpenAI API Key is not set.")
        return

    message = entry.get()
    if not messages:
        messages.append({"role": "system", "content": "You are a helpful assistant."})
    messages += [{"role": "user", "content": message}]
    bot_response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=messages,
    )
    response = bot_response["choices"][0]["message"]["content"]
    messages += [{"role": "assistant", "content": response}]
    chat_log.insert(tk.END, "\nYou: " + message)
    chat_log.insert(tk.END, "\nBot: " + response)
    entry.delete(0, tk.END)

def clear_chat(chat_log, messages):
    chat_log.delete(1.0, tk.END)
    messages.clear()

def main():
    root = tk.Tk()
    root.title(f"KANU ({__version__})")
    root.geometry("800x700")

    header_font = font.Font(family="Arial", size=20)

    openai_container = tk.Frame(root)
    openai_container.pack()
    label = tk.Label(openai_container, text="OpenAI API Key", font=header_font)
    label.grid(row=0, column=0, columnspan=2)

    openai_api_key_entry = tk.Entry(openai_container)
    openai_api_key_entry.grid(row=1, column=1)

    openai_api_key_button = tk.Button(openai_container, text="Submit", command=lambda: get_input(openai_api_key_entry))
    openai_api_key_button.grid(row=1, column=2)

    # This container holds the chat log and the chat entry.
    chat_container = tk.Frame(root)
    chat_container.pack()
    chat_label = tk.Label(chat_container, text="Chat history", font=header_font)
    chat_label.grid(row=0, column=0, columnspan=2)
    custom_font = font.Font(family="Arial", size=12)
    messages = []
    chat_log = tk.Text(chat_container, width=70, height=20, font=custom_font)
    chat_log.grid(row=1, column=0, columnspan=2)
    chat_entry = tk.Entry(chat_container, width=70, font=custom_font)
    chat_entry.grid(row=2, column=0, columnspan=2)
    chat_send_button = tk.Button(chat_container, text="Send", command=lambda: send_message(chat_log, chat_entry, messages))
    chat_send_button.grid(row=3, column=0)
    chat_clear_butoon = tk.Button(chat_container, text="Clear", command=lambda: clear_chat(chat_log, messages))
    chat_clear_butoon.grid(row=3, column=1)

    root.mainloop()

if __name__ == "__main__":
    main()