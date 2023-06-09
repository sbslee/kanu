# README

[![PyPI](https://badge.fury.io/py/kanu.svg)](https://badge.fury.io/py/kanu)

Welcome to KANU, a minimalistic Python-based GUI for various chatbots.

<a id="chatbots"></a>
## Chatbots

### ChatGPT

![Alt Text](https://raw.githubusercontent.com/sbslee/kanu/main/images/chatgpt.gif)

The following packages are required to run ChatGPT:

```
openai
```

### DocGPT

![Alt Text](https://raw.githubusercontent.com/sbslee/kanu/main/images/docgpt.gif)

The following packages are required to run DocGPT:

```
langchain
chromadb
tiktoken
pdfminer.six # Required for .pdf documents
unstructured # Required for .doc and .docx documents
tabulate     # Required for .doc and .docx documents
```

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

## Changelog

See the [CHANGELOG.md](https://github.com/sbslee/kanu/blob/main/CHANGELOG.md) file for details.