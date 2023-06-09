# README

[![PyPI](https://badge.fury.io/py/kanu.svg)](https://badge.fury.io/py/kanu)

Welcome to KANU, a minimalistic Python-based GUI for various chatbots.

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

### ChatGPT

![Alt Text](https://raw.githubusercontent.com/sbslee/kanu/main/images/chatgpt.gif)

The following packages are required to run ChatGPT:

```
openai # Required.
```

### DocGPT

![Alt Text](https://raw.githubusercontent.com/sbslee/kanu/main/images/docgpt.gif)

The follwing file formats are supported by DocGPT:

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