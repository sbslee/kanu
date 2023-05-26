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
        label = tk.Label(self.kanu.container, text="DocGPT")
        label.grid(row=0, column=0, columnspan=3)
        back_button = tk.Button(self.kanu.container, text="Go back", command=lambda: self.kanu.docgpt_config())
        back_button.grid(row=1, column=0)
        back_button = tk.Button(self.kanu.container, text="Reload", command=lambda: self.run())
        back_button.grid(row=1, column=2)
        label = tk.Message(self.kanu.container, width=300, text="Option 1. Create a new database")
        label.grid(row=2, column=0, columnspan=3)
        f = tk.Label(self.kanu.container, text="Document:")
        f.grid(row=3, column=0) 
        self.document_file = tk.Label(self.kanu.container, text="Not selected", fg="red")
        self.document_file.grid(row=3, column=1)
        b = tk.Button(self.kanu.container, text="Browse", command=self.specify_document_file)
        b.grid(row=3, column=2)
        l = tk.Label(self.kanu.container, text="Database:")
        l.grid(row=4, column=0)       
        self.new_database_directory = tk.Label(self.kanu.container, text="Not selected", fg="red")
        self.new_database_directory.grid(row=4, column=1)
        b = tk.Button(self.kanu.container, text="Browse", command=self.specify_new_database_directory)
        b.grid(row=4, column=2)
        self.option1_button = tk.Button(self.kanu.container, text="Go with Option 1", command=self.ingest)
        self.option1_button.grid(row=5, column=0, columnspan=3)
        self.option1_button["state"] = tk.DISABLED
        label = tk.Message(self.kanu.container, width=300, text="Option 2. Use an existing database")
        label.grid(row=6, column=0, columnspan=3)
        f = tk.Label(self.kanu.container, text="Database:")
        f.grid(row=7, column=0)
        self.db_dir = tk.Label(self.kanu.container, text="Not selected", fg="red")
        self.db_dir.grid(row=7, column=1)
        open_button = tk.Button(self.kanu.container, text="Browse", command=self._open_dir)
        open_button.grid(row=7, column=2)
        self.option2_button = tk.Button(self.kanu.container, text="Go with Option 2", command=self.skip)
        self.option2_button.grid(row=8, column=0, columnspan=3)
        self.option2_button["state"] = tk.DISABLED

    def query(self):
        self.db = Chroma(persist_directory=self.db_entry.get(), embedding_function=OpenAIEmbeddings())
        self.qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=self.db.as_retriever())
        self.kanu.container.pack_forget()
        self.kanu.container = tk.Frame(self.kanu.root)
        self.kanu.container.pack()
        title_label = tk.Label(self.kanu.container, text="DocGPT")
        title_label.grid(row=0, column=0, columnspan=3)
        session_label = tk.Label(self.kanu.container, text="Chat session")
        session_label.grid(row=1, column=0, columnspan=3)
        self.session = tk.Text(self.kanu.container, width=70, height=20)
        self.session.grid(row=2, column=0, columnspan=3)
        entry = tk.Entry(self.kanu.container, width=54)
        entry.grid(row=3, column=0, columnspan=3)
        send_button = tk.Button(self.kanu.container, text="Send", command=lambda: self._send_message(entry))
        send_button.grid(row=4, column=0)
        clear_butoon = tk.Button(self.kanu.container, text="Clear", command=lambda: self._clear_session())
        clear_butoon.grid(row=4, column=1)
        back_button = tk.Button(self.kanu.container, text="Go back", command=lambda: self.run())
        back_button.grid(row=4, column=2)

    def _send_message(self, entry):
        self.session.insert(tk.END, "\nYou: " + entry.get())
        response = self.qa(entry.get())["result"]
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

    def specify_document_file(self):
        self.document_file.configure(text=filedialog.askopenfilename(), fg="lime green")

    def _open_dir(self):
        self.dir_path = filedialog.askdirectory()
        self.db_dir = self.db_dir.configure(text=self.dir_path, fg="lime green")
        self.option2_button["state"] = tk.NORMAL

    def _clear_session(self):
        self.session.delete(1.0, tk.END)

    def specify_new_database_directory(self):
        self.new_database_directory.configure(text=filedialog.askdirectory(), fg="lime green")
        self.option1_button["state"] = tk.NORMAL