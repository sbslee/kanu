import tkinter as tk
import importlib.util

from .version import __version__

class KANU:
    def __init__(self, root):
        self.container = None
        self.root = root
        self.root.title(f"KANU ({__version__})")
        self.root.geometry("800x700")
        self.create_home_container()

    def create_home_container(self):
        if self.container is not None:
            self.container.pack_forget()
        self.container = tk.Frame(self.root)
        self.container.pack()
        label = tk.Label(self.container, text="Welcome to KANU, a minimalistic Python-based chatbot GUI")
        label.pack()
        chatgpt_button = tk.Button(self.container, text="ChatGPT", command=lambda: self.create_chatgpt_config_container())
        chatgpt_button.pack()
        docgpt = tk.Button(self.container, text="DocGPT", command=lambda: self.display(self.create_docgpt_config_container))
        docgpt.pack()

    def create_chatgpt_config_container(self):
        self.container.pack_forget()
        self.container = tk.Frame(self.root)
        self.container.pack()
        title_label = tk.Label(self.container, text="ChatGPT Configuration")
        title_label.grid(row=0, column=0, columnspan=2)
        dependency_label = tk.Label(self.container, text="Required Packages:")
        dependency_label.grid(row=1, column=0, columnspan=2)
        package1_label = tk.Label(self.container, text="openai")
        package1_label.grid(row=2, column=0)
        install1_label = tk.Label(self.container, text="❌" if importlib.util.find_spec("openai") is None else "✅")
        install1_label.grid(row=2, column=1)
        key_label = tk.Label(self.container, text="OpenAI API Key:")
        key_label.grid(row=3, column=0, columnspan=2)
        key_entry = tk.Entry(self.container)
        key_entry.grid(row=4, column=0, columnspan=2)
        submit_button = tk.Button(self.container, text="Submit", command=lambda: self.create_chatgpt_session_container(key_entry.get()))
        submit_button.grid(row=5, column=0)
        back_button = tk.Button(self.container, text="Back", command=lambda: self.create_home_container())
        back_button.grid(row=5, column=1)

    def create_chatgpt_session_container(self, openai_key):
        from .chatgpt import ChatGPT
        chatgpt = ChatGPT(self, openai_key)
        chatgpt.run()

    def create_docgpt_config_container(self):
        self.container = tk.Frame(self.root)
        self.container.pack()
        openai_label = tk.Label(self.container, text="OpenAI API Key:")
        openai_label.grid(row=0, column=0)
        huggingface_label = tk.Label(self.container, text="Hugging Face Write Token:")
        huggingface_label.grid(row=1, column=0)
        openai_key = tk.Entry(self.container)
        openai_key.grid(row=0, column=1)
        huggingface_key = tk.Entry(self.container)
        huggingface_key.grid(row=1, column=1)
        submit_button = tk.Button(self.container, text="Submit", command=lambda: self.display(self.create_docgpt_session_container, openai_key.get(), huggingface_key.get()))
        submit_button.grid(row=2, column=0)
        back_button = tk.Button(self.container, text="Back", command=lambda: self.display(self.create_home_container))
        back_button.grid(row=2, column=1)

    def create_docgpt_session_container(self, openai_key, huggingface_key):
        openai.api_key = openai_key
        model_id = "sentence-transformers/all-MiniLM-L6-v2"
        api_url = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{model_id}"
        headers = {"Authorization": f"Bearer {huggingface_key}"}
        self.container = tk.Frame(self.root)
        self.container.pack()

        def query(texts):
            response = requests.post(api_url, headers=headers, json={"inputs": texts, "options":{"wait_for_model":True}})
            return response.json()

def main():
    root = tk.Tk()
    kanu = KANU(root)
    root.mainloop()

if __name__ == "__main__":
    main()