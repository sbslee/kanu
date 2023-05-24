import tkinter as tk
from tkinter import messagebox

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

def main():
    root = tk.Tk()
    root.title(f"KANU ({__version__})")
    root.geometry("800x700")
    label = tk.Label(root, text="OpenAI API Key")
    label.pack()

    openai_api_key_entry = tk.Entry(root)
    openai_api_key_entry.pack()

    openai_api_key_button = tk.Button(root, text="Submit", command=lambda: get_input(openai_api_key_entry))
    openai_api_key_button.pack()

    messages = [{"role": "system", "content": "You are a helpful assistant."}]

    chat_log = tk.Text(root, width=70, height=20)
    chat_log.pack()

    chat_entry = tk.Entry(root, width=50)
    chat_entry.pack()

    chat_send_button = tk.Button(root, text="Send", command=lambda: send_message(chat_log, chat_entry, messages))
    chat_send_button.pack()

    root.mainloop()

if __name__ == "__main__":
    main()