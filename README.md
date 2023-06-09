# README

[![PyPI](https://badge.fury.io/py/kanu.svg)](https://badge.fury.io/py/kanu)

Welcome to KANU, a minimalistic Python-based GUI for various chatbots.

There are currently two chatbots available in KANU:

- [ChatGPT](#chatgpt): This chatbot harnesses the power of ChatGPT, bringing it directly to your local computer.
- [DocGPT](#docgpt): This chatbot enables seamless interaction with your documents. Ask questions about your documents and receive answers in real-time.

Other features of KANU inclde:

- Customize chat settings (e.g. font size and background color)
- Customize chatbot parameters (e.g. prompt, temperature, and chunk size) by directly using the GUI or uploading a configuration file

## Installation

The recommended way is via pip:

```
$ pip install kanu
```

KANU requires a different set of dependencies for each chatbot. You can find the dependencies specific to each chatbot in the [Chatbots](#chatbots) section.

## Running

```
$ kanu
```

<a id="chatbots"></a>
## Chatbots

<a id="chatgpt"></a>
### ChatGPT

![Alt Text](https://raw.githubusercontent.com/sbslee/kanu/main/images/chatgpt.gif)

The following packages are required to run ChatGPT:

```
openai # Required.
```

<a id="docgpt"></a>
### DocGPT

![Alt Text](https://raw.githubusercontent.com/sbslee/kanu/main/images/docgpt.gif)

The following document formats are supported by DocGPT:

- .txt
- .pdf
- .doc and .docx
- .csv

The following packages are required to run DocGPT:

```
langchain    # Required.
chromadb     # Required. 
tiktoken     # Required.
pdfminer.six # Optional. Only required for .pdf documents.
unstructured # Optional. Only required for .doc and .docx documents.
tabulate     # Optional. Only required for .doc and .docx documents.
```

## Changelog

See the [CHANGELOG.md](https://github.com/sbslee/kanu/blob/main/CHANGELOG.md) file for details.