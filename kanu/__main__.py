import configparser
import tkinter as tk
from tkinter import filedialog
import importlib.util

from .version import __version__
from .utils import Tooltip

CHATGPT_PROMPT = """You are a helpful assistant."""
DOCGPT_PROMPT = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.

{context}

Question: {question}
Helpful Answer:"""

class KANU:
    def __init__(self, root):
        self.container = None
        self.root = root
        self.root.title(f"KANU ({__version__})")
        self.root.geometry("600x620")
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
        l = tk.Label(self.container, text="Required packages:")
        l.grid(row=1, column=0, columnspan=2)
        self.display_required_dependency(2, "openai")
        m = tk.Message(self.container, width=300, text="Option 1. Upload a configuration file")
        m.grid(row=3, column=0, columnspan=2)
        b = tk.Button(self.container, text="Browse", command=self.parse_chatgpt_config)
        b.grid(row=4, column=0)
        b = tk.Button(self.container, text="Template", command=self.template_chatgpt_config)
        b.grid(row=4, column=1)
        m = tk.Message(self.container, width=300, text="Option 2. Configure manually")
        m.grid(row=5, column=0, columnspan=2)
        self.model = tk.StringVar(self.container, value="gpt-3.5-turbo")
        l = tk.Label(self.container, text="Model:")
        l.grid(row=6, column=0, columnspan=2)
        b = tk.Radiobutton(self.container, variable=self.model, text="gpt-3.5-turbo", value="gpt-3.5-turbo")
        b.grid(row=7, column=0)
        b = tk.Radiobutton(self.container, variable=self.model, text="gpt-4", value="gpt-4")
        b.grid(row=7, column=1)
        l = tk.Label(self.container, text="System message ⓘ:")
        Tooltip(l, "The system message helps set the behavior of the chatbot.")
        l.grid(row=8, column=0, columnspan=2)
        self.prompt = tk.Text(self.container, height=9, width=42)
        sb = tk.Scrollbar(self.container, command=self.prompt.yview)
        self.prompt.insert("1.0", CHATGPT_PROMPT)
        self.prompt.grid(row=9, column=0, columnspan=2, sticky="nsew")
        sb.grid(row=9, column=2, sticky="ns")
        self.prompt["yscrollcommand"] = sb.set
        l = tk.Label(self.container, text="Temperature ⓘ:")
        Tooltip(l, "The randomness in generating responses, which ranges between 0 and 1, with 0 indicating almost deterministic behavior.")
        l.grid(row=10, column=0, columnspan=2)
        self.temperature = tk.DoubleVar(self.container, value=0.5)
        e = tk.Entry(self.container, textvariable=self.temperature)
        e.grid(row=11, column=0, columnspan=2)
        l = tk.Label(self.container, text="OpenAI API key:")
        l.grid(row=12, column=0, columnspan=2)
        e = tk.Entry(self.container)
        e.grid(row=13, column=0, columnspan=2)
        b = tk.Button(self.container, text="Submit", command=lambda: self.deploy_agent("ChatGPT", e.get(), self.model.get(), self.temperature.get(), self.prompt.get("1.0", "end-1c")))
        b.grid(row=14, column=0)
        b = tk.Button(self.container, text="Go back", command=lambda: self.homepage())
        b.grid(row=14, column=1)

    def parse_chatgpt_config(self):
        config = configparser.ConfigParser()
        config.read(filedialog.askopenfilename())
        self.deploy_agent("ChatGPT", config["USER"]["openai_key"], config["DEFAULT"]["model"], float(config["DEFAULT"]["temperature"]), config["DEFAULT"]["prompt"])

    def template_chatgpt_config(self):
        config = configparser.ConfigParser()
        config["DEFAULT"] = {"model": "gpt-3.5-turbo", "temperature": "0.5", "prompt": CHATGPT_PROMPT}
        config["USER"] = {"openai_key": ""}
        with open(filedialog.asksaveasfilename(), "w") as f:
            config.write(f)

    def config_docgpt(self):
        self.container.pack_forget()
        self.container = tk.Frame(self.root)
        self.container.pack()
        l = tk.Label(self.container, text="DocGPT")
        l.grid(row=0, column=0, columnspan=2)
        l = tk.Label(self.container, text="Required packages:")
        l.grid(row=1, column=0, columnspan=2)
        self.display_required_dependency(2, "langchain")
        self.display_required_dependency(3, "chromadb")
        self.display_required_dependency(4, "tiktoken")
        l = tk.Label(self.container, text="Optional packages:")
        l.grid(row=5, column=0, columnspan=2)        
        self.display_optional_dependency(6, "pdfminer.six", "pdfminer", "Required for .pdf documents.")
        self.display_optional_dependency(7, "unstructured", "unstructured", "Required for .doc and .docx documents.")
        self.display_optional_dependency(8, "tabulate", "tabulate", "Required for .doc and .docx documents.")
        m = tk.Message(self.container, width=300, text="Option 1. Upload a configuration file")
        m.grid(row=9, column=0, columnspan=2)
        b = tk.Button(self.container, text="Browse", command=self.parse_docgpt_config)
        b.grid(row=10, column=0)
        b = tk.Button(self.container, text="Template", command=self.template_docgpt_config)
        b.grid(row=10, column=1)
        m = tk.Message(self.container, width=300, text="Option 2. Configure manually")
        m.grid(row=11, column=0, columnspan=2)
        self.model = tk.StringVar(self.container, value="gpt-3.5-turbo")
        l = tk.Label(self.container, text="Model:")
        l.grid(row=12, column=0, columnspan=2)
        rb = tk.Radiobutton(self.container, variable=self.model, text="gpt-3.5-turbo", value="gpt-3.5-turbo")
        rb.grid(row=13, column=0)
        rb = tk.Radiobutton(self.container, variable=self.model, text="gpt-4", value="gpt-4")
        rb.grid(row=13, column=1)
        l = tk.Label(self.container, text="System message ⓘ:")
        Tooltip(l, "The system message helps set the behavior of the chatbot.")
        l.grid(row=14, column=0, columnspan=2)
        self.prompt = tk.Text(self.container, height=9, width=42)
        sb = tk.Scrollbar(self.container, command=self.prompt.yview)
        self.prompt.insert("1.0", DOCGPT_PROMPT)
        self.prompt.grid(row=15, column=0, columnspan=2, sticky="nsew")
        sb.grid(row=15, column=2, sticky="ns")
        self.prompt["yscrollcommand"] = sb.set
        l = tk.Label(self.container, text="Temperature ⓘ:")
        Tooltip(l, "The randomness in generating responses, which ranges between 0 and 1, with 0 indicating almost deterministic behavior.")
        l.grid(row=16, column=0, columnspan=2)
        self.temperature = tk.DoubleVar(self.container, value=0.5)
        e = tk.Entry(self.container, textvariable=self.temperature)
        e.grid(row=17, column=0, columnspan=2)
        l = tk.Label(self.container, text="OpenAI API key:")
        l.grid(row=18, column=0, columnspan=2)
        e = tk.Entry(self.container)
        e.grid(row=19, column=0, columnspan=2)
        b = tk.Button(self.container, text="Submit", command=lambda: self.deploy_agent("DocGPT", e.get(), self.model.get(), self.prompt.get("1.0", "end-1c"), self.temperature.get()))
        b.grid(row=20, column=0)
        b = tk.Button(self.container, text="Go back", command=lambda: self.homepage())
        b.grid(row=20, column=1)

    def parse_docgpt_config(self):
        config = configparser.ConfigParser()
        config.read(filedialog.askopenfilename())
        self.deploy_agent("DocGPT", config["USER"]["openai_key"], config["DEFAULT"]["model"], float(config["DEFAULT"]["temperature"]), config["DEFAULT"]["prompt"])

    def template_docgpt_config(self):
        config = configparser.ConfigParser()
        config["DEFAULT"] = {"model": "gpt-3.5-turbo", "temperature": "0.5", "prompt": DOCGPT_PROMPT}
        config["USER"] = {"openai_key": ""}
        with open(filedialog.asksaveasfilename(), "w") as f:
            config.write(f)

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
        
    def display_required_dependency(self, row, package_name):
        l = tk.Label(self.container, text=package_name)
        l.grid(row=row, column=0)
        l = tk.Label(self.container, text="❌" if importlib.util.find_spec(package_name) is None else "✅")
        l.grid(row=row, column=1) 

    def display_optional_dependency(self, row, package_name, package_import, tooltip):
        l = tk.Label(self.container, text=f"{package_name} ⓘ")
        Tooltip(l, tooltip)
        l.grid(row=row, column=0)
        l = tk.Label(self.container, text="❌" if importlib.util.find_spec(package_import) is None else "✅")
        l.grid(row=row, column=1)

def main():
    root = tk.Tk()
    kanu = KANU(root)
    root.mainloop()

if __name__ == "__main__":
    main()