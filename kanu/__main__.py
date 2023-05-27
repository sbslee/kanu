import tkinter as tk
import importlib.util

from .version import __version__

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
        self.model = tk.StringVar(self.container, value="gpt-3.5-turbo")
        l = tk.Label(self.container, text="Model:")
        l.grid(row=5, column=0, columnspan=2)
        b = tk.Radiobutton(self.container, variable=self.model, text="gpt-3.5-turbo", value="gpt-3.5-turbo")
        b.grid(row=6, column=0)
        b = tk.Radiobutton(self.container, variable=self.model, text="gpt-4", value="gpt-4")
        b.grid(row=6, column=1)
        l = tk.Label(self.container, text="OpenAI API key:")
        l.grid(row=7, column=0, columnspan=2)
        e = tk.Entry(self.container)
        e.grid(row=8, column=0, columnspan=2)
        b = tk.Button(self.container, text="Submit", command=lambda: self.deploy_agent("DocGPT", e.get(), self.model.get()))
        b.grid(row=9, column=0)
        b = tk.Button(self.container, text="Go back", command=lambda: self.homepage())
        b.grid(row=9, column=1)

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