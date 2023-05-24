import tkinter as tk
from tkinter import messagebox, font

import openai

from .version import __version__

def _get_key(entry, container, root):
    openai.api_key = entry.get()
    container.pack_forget()
    chat_container = create_chat_container(root, container)

def create_config_container(root):
    container = tk.Frame(root)
    container.pack()
    label = tk.Label(container, text="OpenAI API Key")
    label.grid(row=0, column=0, columnspan=2)
    entry = tk.Entry(container)
    entry.grid(row=1, column=1)
    button = tk.Button(container, text="Submit", command=lambda: _get_key(entry, container, root))
    button.grid(row=1, column=2)
    return container

def _send_message(chat_log, entry, messages):
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

def _clear_session(session, messages):
    session.delete(1.0, tk.END)
    messages.clear()

def _go_back(current, previous):
    current.pack_forget()
    previous.pack()

def create_chat_container(root, previous):
    container = tk.Frame(root)
    container.pack()
    label = tk.Label(container, text="Chat session")
    label.grid(row=0, column=0, columnspan=3)
    messages = []
    session = tk.Text(container, width=70, height=20)
    session.grid(row=1, column=0, columnspan=3)
    entry = tk.Entry(container, width=70)
    entry.grid(row=2, column=0, columnspan=3)
    send_button = tk.Button(container, text="Send", command=lambda: _send_message(session, entry, messages))
    send_button.grid(row=3, column=0)
    clear_butoon = tk.Button(container, text="Clear", command=lambda: _clear_session(session, messages))
    clear_butoon.grid(row=3, column=1)
    back_button = tk.Button(container, text="Back", command=lambda: _go_back(container, previous))
    back_button.grid(row=3, column=2)
    return container

def main():
    root = tk.Tk()
    root.title(f"KANU ({__version__})")
    root.geometry("800x700")

    config_container = create_config_container(root)
    chat_container = create_chat_container(root, config_container)
    chat_container.pack_forget()

    root.mainloop()

if __name__ == "__main__":
    main()