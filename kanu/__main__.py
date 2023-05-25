import tkinter as tk

import openai

from .version import __version__

class KANU:
    def __init__(self, root):
        self.root = root
        self.root.title(f"KANU ({__version__})")
        self.root.geometry("800x700")
        self.create_config_container()

    def go_back(self):
        self.current.pack_forget()
        self.previous.pack()
        self.current = self.previous

    def clear_session(self):
        self.session.delete(1.0, tk.END)
        self.messages.clear()

    def _get_key(self, entry):
        openai.api_key = entry.get()
        self.current.pack_forget()
        self.previous = self.current
        self.create_chat_container()

    def create_config_container(self):
        self.current = tk.Frame(self.root)
        self.current.pack()
        label = tk.Label(self.current, text="OpenAI API Key")
        label.grid(row=0, column=0, columnspan=2)
        entry = tk.Entry(self.current)
        entry.grid(row=1, column=1)
        button = tk.Button(self.current, text="Submit", command=lambda: self._get_key(entry))
        button.grid(row=1, column=2)

    def _send_message(self, entry):
        if not self.messages:
            self.messages.append({"role": "system", "content": "You are a helpful assistant."})
        self.messages += [{"role": "user", "content": entry.get()}]
        bot_response = openai.ChatCompletion.create(
            model=self.model.get(),
            messages=self.messages,
        )
        print(f"used {self.model.get()}")
        response = bot_response["choices"][0]["message"]["content"]
        self.messages += [{"role": "assistant", "content": response}]
        self.session.insert(tk.END, "\nYou: " + entry.get())
        self.session.insert(tk.END, f"\nBot ({self.model.get()}): " + response)
        entry.delete(0, tk.END)

    def create_chat_container(self):
        self.current = tk.Frame(self.root)
        self.current.pack()

        self.model = tk.StringVar(self.current, value="gpt-3.5-turbo")
        model_label = tk.Label(self.current, text="Model:")
        model_label.grid(row=0, column=0)
        model1_button = tk.Radiobutton(self.current, variable=self.model, text="gpt-3.5-turbo", value="gpt-3.5-turbo")
        model2_button = tk.Radiobutton(self.current, variable=self.model, text="gpt-4", value="gpt-4")
        model1_button.grid(row=0, column=1)
        model2_button.grid(row=0, column=2)

        session_label = tk.Label(self.current, text="Chat session")
        session_label.grid(row=1, column=0, columnspan=3)
        self.session = tk.Text(self.current, width=70, height=20)
        self.session.grid(row=2, column=0, columnspan=3)
        entry = tk.Entry(self.current, width=70)
        entry.grid(row=3, column=0, columnspan=3)
        self.messages = []
        send_button = tk.Button(self.current, text="Send", command=lambda: self._send_message(entry))
        send_button.grid(row=4, column=0)
        clear_butoon = tk.Button(self.current, text="Clear", command=lambda: self.clear_session())
        clear_butoon.grid(row=4, column=1)
        back_button = tk.Button(self.current, text="Back", command=lambda: self.go_back())
        back_button.grid(row=4, column=2)


def main():
    root = tk.Tk()
    kanu = KANU(root)
    root.mainloop()

if __name__ == "__main__":
    main()