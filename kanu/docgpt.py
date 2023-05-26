import os
import tkinter as tk
from tkinter import filedialog

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.llms import OpenAI
from langchain.document_loaders import TextLoader
from langchain.chains import RetrievalQA

class DocGPT:
    def __init__(self, kanu, openai_key):
        self.kanu = kanu
        os.environ["OPENAI_API_KEY"] = openai_key

    def run(self):
        self.kanu.container.pack_forget()
        self.kanu.container = tk.Frame(self.kanu.root)
        self.kanu.container.pack()
        title_label = tk.Label(self.kanu.container, text="DocGPT Ingest")
        title_label.grid(row=0, column=0, columnspan=3)
        open_button = tk.Button(self.kanu.container, text="Browse", command=self._open_file)
        open_button.grid(row=1, column=0, columnspan=2)
        db_label = tk.Label(self.kanu.container, text="Database:")
        db_label.grid(row=2, column=1)
        self.db_entry = tk.Entry(self.kanu.container)
        self.db_entry.grid(row=2, column=2)
        ingest_button = tk.Button(self.kanu.container, text="Ingest", command=self.ingest)
        ingest_button.grid(row=3, column=0)
        skip_butoon = tk.Button(self.kanu.container, text="Skip", command=self.skip)
        skip_butoon.grid(row=3, column=1)
        back_button = tk.Button(self.kanu.container, text="Back", command=lambda: self.kanu.docgpt_config())
        back_button.grid(row=3, column=2)

    def query(self):
        self.db = Chroma(persist_directory=self.db_entry.get(), embedding_function=OpenAIEmbeddings())
        self.qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=self.db.as_retriever())
        self.kanu.container.pack_forget()
        self.kanu.container = tk.Frame(self.kanu.root)
        self.kanu.container.pack()
        title_label = tk.Label(self.kanu.container, text="DocGPT Query")
        title_label.grid(row=0, column=0, columnspan=3)
        session_label = tk.Label(self.kanu.container, text="Chat Session")
        session_label.grid(row=1, column=0, columnspan=3)
        self.session = tk.Text(self.kanu.container, width=70, height=20)
        self.session.grid(row=2, column=0, columnspan=3)
        entry = tk.Entry(self.kanu.container, width=54)
        entry.grid(row=3, column=0, columnspan=3)
        send_button = tk.Button(self.kanu.container, text="Send", command=lambda: self._send_message(entry))
        send_button.grid(row=4, column=0)
        clear_butoon = tk.Button(self.kanu.container, text="Clear", command=lambda: self._clear_session())
        clear_butoon.grid(row=4, column=1)
        back_button = tk.Button(self.kanu.container, text="Back", command=lambda: self.run())
        back_button.grid(row=4, column=2)

    def _send_message(self, entry):
        self.session.insert(tk.END, "\nYou: " + entry.get())
        response = self.qa(entry.get())['result']
        self.session.insert(tk.END, "\nBot: " + response)
        entry.delete(0, tk.END)

    def skip(self):
        self.query()

    def ingest(self):
        loader = TextLoader(self.file_path)
        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        docs = text_splitter.split_documents(documents)
        embeddings = OpenAIEmbeddings()
        db = Chroma.from_documents(docs, embeddings, persist_directory=self.db_entry.get())
        db.persist()
        db = None
        self.query()

    def _open_file(self):
        self.file_path = filedialog.askopenfilename()

    def _clear_session(self):
        self.session.delete(1.0, tk.END)
        self.messages.clear()