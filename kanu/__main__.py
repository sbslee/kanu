import tkinter as tk
from tkinter import ttk
import importlib.util

from .version import __version__

class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25

        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")

        label = tk.Label(self.tooltip, text=self.text, background="#ffffe0", relief="solid", borderwidth=1)
        label.pack()

    def hide_tooltip(self, event):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

class KANU:
    def __init__(self, root):
        self.container = None
        self.root = root
        self.root.title(f"KANU ({__version__})")
        self.root.geometry("600x400")
        self.homepage()

    def homepage(self):
        if self.container is not None:
            self.container.pack_forget()
        self.container = tk.Frame(self.root)
        self.container.pack()
        l = tk.Message(self.container, width=350, text="Welcome to KANU, a minimalistic Python-based GUI for various chatbots! Please select a chatbot to begin.")
        l.pack()
        b = tk.Button(self.container, text="ChatGPT", command=lambda: self.config_chatgpt())
        b.pack()
        b = tk.Button(self.container, text="DocGPT", command=lambda: self.config_docgpt())
        b.pack()

    def config_chatgpt(self):
        self.container.pack_forget()
        self.container = tk.Frame(self.root)
        self.container.pack()
        l = tk.Label(self.container, text="ChatGPT")
        l.grid(row=0, column=0, columnspan=2)
        self.list_dependencies(2, ["openai"])
        self.model = tk.StringVar(self.container, value="gpt-3.5-turbo")
        l = tk.Label(self.container, text="Model:")
        l.grid(row=4, column=0, columnspan=2)
        b = tk.Radiobutton(self.container, variable=self.model, text="gpt-3.5-turbo", value="gpt-3.5-turbo")
        b.grid(row=5, column=0)
        b = tk.Radiobutton(self.container, variable=self.model, text="gpt-4", value="gpt-4")
        b.grid(row=5, column=1)
        l = tk.Label(self.container, text="OpenAI API key:")
        l.grid(row=6, column=0, columnspan=2)
        e = tk.Entry(self.container)
        e.grid(row=7, column=0, columnspan=2)
        b = tk.Button(self.container, text="Submit", command=lambda: self.deploy_agent("ChatGPT", e.get(), self.model.get()))
        b.grid(row=8, column=0)
        b = tk.Button(self.container, text="Go back", command=lambda: self.homepage())
        b.grid(row=8, column=1)

    def config_docgpt(self):
        self.container.pack_forget()
        self.container = tk.Frame(self.root)
        self.container.pack()
        l = tk.Label(self.container, text="DocGPT")
        l.grid(row=0, column=0, columnspan=2)
        self.list_dependencies(1, ["langchain", "chromadb", "tiktoken"])
        l = tk.Label(self.container, text="Optional packages:")
        l.grid(row=5, column=0, columnspan=2)
        name = tk.Label(self.container, text="pdfminer.six ⓘ")
        name.grid(row=6, column=0)
        tooltip = Tooltip(name, "Required for .pdf documents.")
        l = tk.Label(self.container, text="❌" if importlib.util.find_spec("pdfminer") is None else "✅")
        l.grid(row=6, column=1)
        name = tk.Label(self.container, text="unstructured ⓘ")
        name.grid(row=7, column=0)
        tooltip = Tooltip(name, "Required for .doc and .docx documents.")
        l = tk.Label(self.container, text="❌" if importlib.util.find_spec("unstructured") is None else "✅")
        l.grid(row=7, column=1)
        name = tk.Label(self.container, text="tabulate ⓘ")
        name.grid(row=8, column=0)
        tooltip = Tooltip(name, "Required for .doc and .docx documents.")
        l = tk.Label(self.container, text="❌" if importlib.util.find_spec("tabulate") is None else "✅")
        l.grid(row=8, column=1)
        self.model = tk.StringVar(self.container, value="gpt-3.5-turbo")
        l = tk.Label(self.container, text="Model:")
        l.grid(row=9, column=0, columnspan=2)
        b = tk.Radiobutton(self.container, variable=self.model, text="gpt-3.5-turbo", value="gpt-3.5-turbo")
        b.grid(row=10, column=0)
        b = tk.Radiobutton(self.container, variable=self.model, text="gpt-4", value="gpt-4")
        b.grid(row=10, column=1)
        l = tk.Label(self.container, text="OpenAI API key:")
        l.grid(row=11, column=0, columnspan=2)
        e = tk.Entry(self.container)
        e.grid(row=12, column=0, columnspan=2)
        b = tk.Button(self.container, text="Submit", command=lambda: self.deploy_agent("DocGPT", e.get(), self.model.get()))
        b.grid(row=13, column=0)
        b = tk.Button(self.container, text="Go back", command=lambda: self.homepage())
        b.grid(row=13, column=1)

    def deploy_agent(self, agent, *args, **kwargs):
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

    def list_dependencies(self, row, packages):
        l = tk.Label(self.container, text="Required packages:")
        l.grid(row=row, column=0, columnspan=2)
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