import tkinter as tk

import openai

from .version import __version__

class KANU:
    def __init__(self, root):
        self.root = root
        self.root.title(f"KANU ({__version__})")
        self.root.geometry("800x700")
        self.create_home_container()

    def display(self, f, *args, **kwargs):
        self.container.pack_forget()
        f(*args, **kwargs)

    def create_home_container(self):
        self.container = tk.Frame(self.root)
        self.container.pack()
        label = tk.Label(self.container, text="Welcome to KANU, a Pythonic minimalistic chatbot GUI!")
        label.pack()
        chatgpt_button = tk.Button(self.container, text="ChatGPT", command=lambda: self.display(self.create_chatgpt_config_container))
        chatgpt_button.pack()
        docgpt = tk.Button(self.container, text="DocGPT", command=lambda: self.display(self.create_docgpt_config_container))
        docgpt.pack()

    def clear_session(self):
        self.session.delete(1.0, tk.END)
        self.messages.clear()

    def create_chatgpt_config_container(self):
        self.container = tk.Frame(self.root)
        self.container.pack()
        label = tk.Label(self.container, text="OpenAI API Key:")
        label.grid(row=0, column=0)
        entry = tk.Entry(self.container)
        entry.grid(row=0, column=1)
        button = tk.Button(self.container, text="Submit", command=lambda: self.display(self.create_chatgpt_session_container, entry.get()))
        button.grid(row=1, column=0)
        back_button = tk.Button(self.container, text="Back", command=lambda: self.display(self.create_home_container))
        back_button.grid(row=1, column=1)

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

    def _send_message(self, entry):
        if not self.messages:
            self.messages.append({"role": "system", "content": "You are a helpful assistant."})
        self.messages += [{"role": "user", "content": entry.get()}]
        bot_response = openai.ChatCompletion.create(
            model=self.model.get(),
            messages=self.messages,
        )
        response = bot_response["choices"][0]["message"]["content"]
        self.messages += [{"role": "assistant", "content": response}]
        self.session.insert(tk.END, "\nYou: " + entry.get())
        self.session.insert(tk.END, f"\nBot ({self.model.get()}): " + response)
        entry.delete(0, tk.END)

    def create_chatgpt_session_container(self, openai_key):
        openai.api_key = openai_key
        self.container = tk.Frame(self.root)
        self.container.pack()

        self.model = tk.StringVar(self.container, value="gpt-3.5-turbo")
        model_label = tk.Label(self.container, text="Model:")
        model_label.grid(row=0, column=0)
        model1_button = tk.Radiobutton(self.container, variable=self.model, text="gpt-3.5-turbo", value="gpt-3.5-turbo")
        model2_button = tk.Radiobutton(self.container, variable=self.model, text="gpt-4", value="gpt-4")
        model1_button.grid(row=0, column=1)
        model2_button.grid(row=0, column=2)

        session_label = tk.Label(self.container, text="Chat session")
        session_label.grid(row=1, column=0, columnspan=3)
        self.session = tk.Text(self.container, width=70, height=20)
        self.session.grid(row=2, column=0, columnspan=3)
        entry = tk.Entry(self.container, width=70)
        entry.grid(row=3, column=0, columnspan=3)
        self.messages = []
        send_button = tk.Button(self.container, text="Send", command=lambda: self._send_message(entry))
        send_button.grid(row=4, column=0)
        clear_butoon = tk.Button(self.container, text="Clear", command=lambda: self.clear_session())
        clear_butoon.grid(row=4, column=1)
        back_button = tk.Button(self.container, text="Back", command=lambda: self.display(self.create_chatgpt_config_container))
        back_button.grid(row=4, column=2)

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