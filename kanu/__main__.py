import tkinter as tk
import importlib.util

from .version import __version__

class KANU:
    def __init__(self, root):
        self.container = None
        self.root = root
        self.root.title(f"KANU ({__version__})")
        self.root.geometry("600x400")
        self.home_page()

    def home_page(self):
        if self.container is not None:
            self.container.pack_forget()
        self.container = tk.Frame(self.root)
        self.container.pack()
        title_label = tk.Message(self.container, width=350, text="Welcome to KANU, a minimalistic Python-based GUI for various chatbots! Please select a chatbot to begin.")
        title_label.pack()
        chatgpt_button = tk.Button(self.container, text="ChatGPT", command=lambda: self.chatgpt_config())
        chatgpt_button.pack()
        docgpt_button = tk.Button(self.container, text="DocGPT", command=lambda: self.docgpt_config())
        docgpt_button.pack()

    def chatgpt_config(self):
        self.container.pack_forget()
        self.container = tk.Frame(self.root)
        self.container.pack()
        title_label = tk.Label(self.container, text="ChatGPT")
        title_label.grid(row=0, column=0, columnspan=2)
        self._list_dependencies(1, ["openai"])
        key_label = tk.Label(self.container, text="OpenAI API key:")
        key_label.grid(row=3, column=0, columnspan=2)
        key_entry = tk.Entry(self.container)
        key_entry.grid(row=4, column=0, columnspan=2)
        submit_button = tk.Button(self.container, text="Submit", command=lambda: self._deploy("ChatGPT", key_entry.get()))
        submit_button.grid(row=5, column=0)
        back_button = tk.Button(self.container, text="Go back", command=lambda: self.home_page())
        back_button.grid(row=5, column=1)

    def docgpt_config(self):
        self.container.pack_forget()
        self.container = tk.Frame(self.root)
        self.container.pack()
        title_label = tk.Label(self.container, text="DocGPT")
        title_label.grid(row=0, column=0, columnspan=2)
        self._list_dependencies(1, ["langchain", "chromadb", "tiktoken"])
        key_label = tk.Label(self.container, text="OpenAI API key:")
        key_label.grid(row=5, column=0, columnspan=2)
        key_entry = tk.Entry(self.container)
        key_entry.grid(row=6, column=0, columnspan=2)
        submit_button = tk.Button(self.container, text="Submit", command=lambda: self._deploy("DocGPT", key_entry.get()))
        submit_button.grid(row=7, column=0)
        back_button = tk.Button(self.container, text="Go back", command=lambda: self.home_page())
        back_button.grid(row=7, column=1)

    def _deploy(self, agent, *args, **kwargs):
        if agent == "ChatGPT":
            from .chatgpt import ChatGPT
            chatgpt = ChatGPT(self, *args, **kwargs)
            chatgpt.run()
        elif agent == "DocGPT":
            from .docgpt import DocGPT
            docgpt = DocGPT(self, *args, **kwargs)
            docgpt.run()
        else:
            raise ValueError(f"Unknown agent {agent}")

    def _list_dependencies(self, row, packages):
        title = tk.Label(self.container, text="Required packages:")
        title.grid(row=row, column=0, columnspan=2)
        for i, package in enumerate(packages, row+1):
            name = tk.Label(self.container, text=package)
            name.grid(row=i, column=0)
            status = tk.Label(self.container, text="❌" if importlib.util.find_spec(package) is None else "✅")
            status.grid(row=i, column=1)

def main():
    root = tk.Tk()
    kanu = KANU(root)
    root.mainloop()

if __name__ == "__main__":
    main()