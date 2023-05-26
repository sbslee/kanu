import os
import tkinter as tk
from tkinter import filedialog

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.document_loaders import TextLoader

class DocGPT:
    def __init__(self, kanu, openai_key):
        self.kanu = kanu
        self.kanu.container.pack_forget()
        self.kanu.container = tk.Frame(self.kanu.root)
        self.kanu.container.pack()
        os.environ["OPENAI_API_KEY"] = openai_key

    def run(self):
        title_label = tk.Label(self.kanu.container, text="DocGPT Ingest")
        title_label.grid(row=0, column=0, columnspan=3)
        open_button = tk.Button(self.kanu.container, text="Browse", command=self._open_file)
        open_button.grid(row=1, column=0, columnspan=2)
        db_label = tk.Label(self.kanu.container, text="Database:")
        db_label.grid(row=2, column=1)
        self.db_entry = tk.Entry(self.kanu.container)
        self.db_entry.grid(row=2, column=2)
        ingest_button = tk.Button(self.kanu.container, text="Ingest", command=self._ingest)
        ingest_button.grid(row=3, column=0, columnspan=2)
        # query = "What did the president say about Ketanji Brown Jackson"
        # docs = db.similarity_search(query)
        # print(docs[0].page_content)

    def _ingest(self):
        loader = TextLoader(self.file_path)
        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        docs = text_splitter.split_documents(documents)
        embeddings = OpenAIEmbeddings()
        db = Chroma.from_documents(docs, embeddings, persist_directory=self.db_entry.get())
        db.persist()
        db = None

    def _open_file(self):
        self.file_path = filedialog.askopenfilename()