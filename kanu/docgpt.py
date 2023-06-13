import os
import tkinter as tk
from tkinter import filedialog

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.callbacks import get_openai_callback

from langchain.document_loaders import (
    TextLoader,
    PDFMinerLoader,
    UnstructuredWordDocumentLoader,
    CSVLoader,
)

from .utils import Tooltip, Settings, tokens2price, text2tokens

DOCUMENT_LOADERS = {
    ".txt": (TextLoader, {"encoding": "utf8"}),
    ".pdf": (PDFMinerLoader, {}),
    ".doc": (UnstructuredWordDocumentLoader, {}),
    ".docx": (UnstructuredWordDocumentLoader, {}),
    ".csv": (CSVLoader, {}),
}

class DocGPT:
    def __init__(self, kanu, openai_key, model, temperature, prompt, default_chunk_size, default_chunk_overlap):
        self.kanu = kanu
        self.model = model
        self.temperature = temperature
        self.prompt = prompt
        self.default_chunk_size = default_chunk_size
        self.default_chunk_overlap = default_chunk_overlap
        os.environ["OPENAI_API_KEY"] = openai_key
        self.settings = Settings(self)
        self.tokens = 0
        self.price = 0

    def run(self):
        self.kanu.container.pack_forget()
        self.kanu.container = tk.Frame(self.kanu.root)
        self.kanu.container.pack()
        l = tk.Label(self.kanu.container, text="DocGPT")
        l.grid(row=0, column=0, columnspan=3)
        b = tk.Button(self.kanu.container, text="Go back", command=lambda: self.kanu.config_docgpt())
        b.grid(row=1, column=0)
        b = tk.Button(self.kanu.container, text="Reload", command=lambda: self.run())
        b.grid(row=1, column=2)
        m = tk.Message(self.kanu.container, width=300, text="Option 1. Create a new database")
        m.grid(row=2, column=0, columnspan=3)
        l = tk.Label(self.kanu.container, text="Document ⓘ:")
        Tooltip(l, "Directory containing documents for the database.")
        l.grid(row=3, column=0) 
        self.document_label = tk.Label(self.kanu.container, text="Not selected", fg="red")
        self.document_label.grid(row=3, column=1)
        b = tk.Button(self.kanu.container, text="Browse", command=self.specify_document_directory)
        b.grid(row=3, column=2)
        l = tk.Label(self.kanu.container, text="Database ⓘ:")
        Tooltip(l, "Directory where the database will be stored.")
        l.grid(row=4, column=0)       
        self.new_database_label = tk.Label(self.kanu.container, text="Not selected", fg="red")
        self.new_database_label.grid(row=4, column=1)
        b = tk.Button(self.kanu.container, text="Browse", command=self.specify_new_database_directory)
        b.grid(row=4, column=2)
        l = tk.Label(self.kanu.container, text="Chunk size ⓘ:")
        Tooltip(l, "The maximum number of characters in each chunk.")
        l.grid(row=5, column=0)
        self.chunk_size = tk.IntVar(self.kanu.container, value=self.default_chunk_size)
        e = tk.Entry(self.kanu.container, textvariable=self.chunk_size)
        e.grid(row=5, column=1, columnspan=2)
        l = tk.Label(self.kanu.container, text="Chunk overlap ⓘ:")
        Tooltip(l, "The number of overlapping characters between adjacent chunks.")
        l.grid(row=6, column=0)
        self.chunk_overlap = tk.IntVar(self.kanu.container, value=self.default_chunk_overlap)
        e = tk.Entry(self.kanu.container, textvariable=self.chunk_overlap)
        e.grid(row=6, column=1, columnspan=2)
        self.option1_button = tk.Button(self.kanu.container, text="Go with Option 1", command=self.go_with_option1)
        self.option1_button.grid(row=7, column=0, columnspan=3)
        self.option1_button["state"] = tk.DISABLED
        m = tk.Message(self.kanu.container, width=300, text="Option 2. Use an existing database")
        m.grid(row=8, column=0, columnspan=3)
        l = tk.Label(self.kanu.container, text="Database ⓘ:")
        Tooltip(l, "Directory where the database is stored.")
        l.grid(row=9, column=0)
        self.old_database_label = tk.Label(self.kanu.container, text="Not selected", fg="red")
        self.old_database_label.grid(row=9, column=1)
        b = tk.Button(self.kanu.container, text="Browse", command=self.specify_old_database_directory)
        b.grid(row=9, column=2)
        self.option2_button = tk.Button(self.kanu.container, text="Go with Option 2", command=self.go_with_option2)
        self.option2_button.grid(row=10, column=0, columnspan=3)
        self.option2_button["state"] = tk.DISABLED

    def query(self):
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        self.db = Chroma(persist_directory=self.database_directory, embedding_function=OpenAIEmbeddings())
        self.qa = ConversationalRetrievalChain.from_llm(
            llm=ChatOpenAI(model_name=self.model, temperature=self.temperature),
            retriever=self.db.as_retriever(),
            memory=self.memory,
            chain_type="stuff",
            combine_docs_chain_kwargs={"prompt": PromptTemplate(template=self.prompt, input_variables=["context", "question"])}
        )
        self.kanu.container.pack_forget()
        self.kanu.container = tk.Frame(self.kanu.root)
        self.kanu.container.pack()
        l = tk.Label(self.kanu.container, text="DocGPT")
        l.grid(row=0, column=0, columnspan=4)
        self.system = tk.Text(self.kanu.container, width=80, height=7)
        self.system.tag_configure("system", **self.settings.get_system_kwargs())
        if self.existing:
            self.system.insert(tk.END, "System: Using existing database. No tokens were used.\n", "system")
        else:
            self.system.insert(tk.END, f"System: Creating new database. Embedding used {self.tokens:,} tokens or ${self.price:.6f}.\n", "system")
        self.system.insert(tk.END, "System: A new chat session has been created.\n", "system")
        self.system.grid(row=1, column=0, columnspan=4)
        self.session = tk.Text(self.kanu.container, width=80, height=20)
        self.session.grid(row=2, column=0, columnspan=4)
        self.session.tag_config("user", **self.settings.get_user_kwargs())
        self.session.tag_config("bot", **self.settings.get_bot_kwargs())
        user_input = tk.Entry(self.kanu.container, width=62)
        user_input.grid(row=3, column=0, columnspan=4)
        b = tk.Button(self.kanu.container, text="Send", command=lambda: self.send_message(user_input))
        b.grid(row=4, column=0)
        b = tk.Button(self.kanu.container, text="Clear", command=lambda: self.clear_session())
        b.grid(row=4, column=1)
        b = tk.Button(self.kanu.container, text="Go back", command=lambda: self.run())
        b.grid(row=4, column=2)
        b = tk.Button(self.kanu.container, text="Settings", command=lambda: self.settings.page())
        b.grid(row=4, column=3)

    def send_message(self, entry):
        self.session.insert(tk.END, "You: " + entry.get() + "\n", "user")
        with get_openai_callback() as cb:
            response = self.qa(entry.get())
            usage = self.calculate_usage(cb)
        self.session.insert(tk.END, "Bot: " + response["answer"] + "\n", "bot")
        self.system.insert(tk.END, f"{usage}\n", "system")
        entry.delete(0, tk.END)

    def calculate_usage(self, cb):
        prompt_price = tokens2price(cb.prompt_tokens, self.model, "prompt")
        completion_price = tokens2price(cb.completion_tokens, self.model, "completion")
        self.price += prompt_price + completion_price
        self.tokens += cb.total_tokens
        message = f"System: Used {cb.prompt_tokens:,} prompt + {cb.completion_tokens:,} completion = {cb.total_tokens:,} tokens (total: {self.tokens:,} or ${self.price:.6f})."
        return message

    def go_with_option1(self):
        self.tokens = self.price = 0
        documents = []
        for root, dirs, files in os.walk(self.document_directory):
            for file in files:
                file_path = os.path.join(root, file)
                file_ext = os.path.splitext(file_path)[1]
                if file_ext not in DOCUMENT_LOADERS:
                    continue
                loader_class, loader_kwargs = DOCUMENT_LOADERS[file_ext]
                loader = loader_class(file_path, **loader_kwargs)
                document = loader.load()
                documents.extend(document)
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=self.chunk_size.get(), chunk_overlap=self.chunk_overlap.get())
        texts = text_splitter.split_documents(documents)
        for text in texts:
            self.tokens += text2tokens("text-embedding-ada-002", text.page_content)
        self.price = tokens2price(self.tokens, "text-embedding-ada-002", "embedding")
        db = Chroma.from_documents(texts, OpenAIEmbeddings(model="text-embedding-ada-002"), persist_directory=self.database_directory)
        db.add_documents(texts)
        db.persist()
        db = None
        self.existing = False
        self.query()

    def go_with_option2(self):
        self.tokens = self.price = 0
        self.existing = True
        self.query()

    def specify_document_directory(self):
        directory_path = filedialog.askdirectory()
        if not directory_path:
            return
        self.document_directory = directory_path
        self.document_label.configure(text=os.path.basename(directory_path), fg="lime green")
        if self.new_database_label["text"] != "Not selected":
            self.option1_button["state"] = tk.NORMAL

    def specify_new_database_directory(self):
        directory_path = filedialog.askdirectory()
        if not directory_path:
            return
        self.database_directory = directory_path
        self.new_database_label.configure(text=os.path.basename(directory_path), fg="lime green")
        if self.document_label["text"] != "No file selected":
            self.option1_button["state"] = tk.NORMAL

    def specify_old_database_directory(self):
        directory_path = filedialog.askdirectory()
        if not directory_path:
            return
        self.database_directory = directory_path
        self.old_database_label.configure(text=os.path.basename(directory_path), fg="lime green")
        self.option2_button["state"] = tk.NORMAL

    def clear_session(self):
        self.existing = True
        self.tokens = self.price = 0
        self.query()
