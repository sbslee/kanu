import os
import glob
import tkinter as tk
from tkinter import filedialog

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA

from langchain.document_loaders import (
    TextLoader,
    PDFMinerLoader,
    UnstructuredWordDocumentLoader
)

DOCUMENT_LOADERS = {
    ".txt": TextLoader,
    ".pdf": PDFMinerLoader,
    ".doc": UnstructuredWordDocumentLoader,
    ".docx": UnstructuredWordDocumentLoader,
}

class DocGPT:
    def __init__(self, kanu, openai_key, model):
        self.kanu = kanu
        self.model = model
        os.environ["OPENAI_API_KEY"] = openai_key

    def run(self):
        self.kanu.container.pack_forget()
        self.kanu.container = tk.Frame(self.kanu.root)
        self.kanu.container.pack()
        label = tk.Label(self.kanu.container, text="DocGPT")
        label.grid(row=0, column=0, columnspan=3)
        back_button = tk.Button(self.kanu.container, text="Go back", command=lambda: self.kanu.config_docgpt())
        back_button.grid(row=1, column=0)
        back_button = tk.Button(self.kanu.container, text="Reload", command=lambda: self.run())
        back_button.grid(row=1, column=2)
        label = tk.Message(self.kanu.container, width=300, text="Option 1. Create a new database")
        label.grid(row=2, column=0, columnspan=3)
        f = tk.Label(self.kanu.container, text="Document:")
        f.grid(row=3, column=0) 
        self.document_label = tk.Label(self.kanu.container, text="No directory selected", fg="red")
        self.document_label.grid(row=3, column=1)
        b = tk.Button(self.kanu.container, text="Browse", command=self.specify_document_directory)
        b.grid(row=3, column=2)
        l = tk.Label(self.kanu.container, text="Database:")
        l.grid(row=4, column=0)       
        self.new_database_label = tk.Label(self.kanu.container, text="No directory selected", fg="red")
        self.new_database_label.grid(row=4, column=1)
        b = tk.Button(self.kanu.container, text="Browse", command=self.specify_new_database_directory)
        b.grid(row=4, column=2)
        self.option1_button = tk.Button(self.kanu.container, text="Go with Option 1", command=self.go_with_option1)
        self.option1_button.grid(row=5, column=0, columnspan=3)
        self.option1_button["state"] = tk.DISABLED
        label = tk.Message(self.kanu.container, width=300, text="Option 2. Use an existing database")
        label.grid(row=6, column=0, columnspan=3)
        f = tk.Label(self.kanu.container, text="Database:")
        f.grid(row=7, column=0)
        self.old_database_label = tk.Label(self.kanu.container, text="No directory selected", fg="red")
        self.old_database_label.grid(row=7, column=1)
        open_button = tk.Button(self.kanu.container, text="Browse", command=self.specify_old_database_directory)
        open_button.grid(row=7, column=2)
        self.option2_button = tk.Button(self.kanu.container, text="Go with Option 2", command=self.go_with_option2)
        self.option2_button.grid(row=8, column=0, columnspan=3)
        self.option2_button["state"] = tk.DISABLED

    def query(self):
        self.db = Chroma(persist_directory=self.database_directory, embedding_function=OpenAIEmbeddings())
        self.qa = RetrievalQA.from_chain_type(llm=ChatOpenAI(model_name=self.model), chain_type="stuff", retriever=self.db.as_retriever())
        self.kanu.container.pack_forget()
        self.kanu.container = tk.Frame(self.kanu.root)
        self.kanu.container.pack()
        l = tk.Label(self.kanu.container, text="DocGPT")
        l.grid(row=0, column=0, columnspan=3)    
        self.session = tk.Text(self.kanu.container, width=70, height=20)
        self.session.grid(row=1, column=0, columnspan=3)
        e = tk.Entry(self.kanu.container, width=54)
        e.grid(row=2, column=0, columnspan=3)
        b = tk.Button(self.kanu.container, text="Send", command=lambda: self.send_message(e))
        b.grid(row=3, column=0)
        b = tk.Button(self.kanu.container, text="Clear", command=lambda: self.clear_session())
        b.grid(row=3, column=1)
        b = tk.Button(self.kanu.container, text="Go back", command=lambda: self.run())
        b.grid(row=3, column=2)

    def send_message(self, entry):
        self.session.insert(tk.END, "You: " + entry.get() + "\n")
        response = self.qa(entry.get())["result"]
        self.session.insert(tk.END, "Bot:" + response + "\n")
        entry.delete(0, tk.END)

    def go_with_option1(self):
        documents = []
        for root, dirs, files in os.walk(self.document_directory):
            for file in files:
                file_path = os.path.join(root, file)
                file_ext = os.path.splitext(file_path)[1]
                if file_ext not in DOCUMENT_LOADERS:
                    continue
                loader = DOCUMENT_LOADERS[file_ext](file_path)
                document = loader.load()[0]
                documents.append(document)
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
        texts = text_splitter.split_documents(documents)
        db = Chroma.from_documents(texts, OpenAIEmbeddings(), persist_directory=self.database_directory)
        db.add_documents(texts)    
        db.persist()
        db = None
        self.query()

    def go_with_option2(self):
        self.query()

    def specify_document_directory(self):
        directory_path = filedialog.askdirectory()
        if not directory_path:
            return
        self.document_directory = directory_path
        self.document_label.configure(text=os.path.basename(directory_path), fg="lime green")
        if self.new_database_label["text"] != "No directory selected":
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
        self.session.delete(1.0, tk.END)

