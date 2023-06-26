# README

[![PyPI](https://badge.fury.io/py/kanu.svg)](https://badge.fury.io/py/kanu)

Welcome to KANU, a minimalistic Python-based GUI for various chatbots.

There are currently two chatbots available in KANU:

- [ChatGPT](#chatgpt) harnesses the power of ChatGPT, bringing it directly to your local computer
- [DocGPT](#docgpt) allows you to effortlessly interact with your documents and ask questions about them
- [FuncGPT](#funcgpt) can answer your questions by making calls to external tools, APIs, or databases

Other features of KANU inclde:

- Customize chatbot parameters (e.g. prompt, temperature, and chunk size) by directly using the GUI or uploading a configuration file
- Customize chat settings (e.g. font size and background color)
- Display token counter and price monitor in chat window

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

DocGPT currently supports the following document formats: `.csv`, `.doc`, `.docx`, `.pdf`, and `.txt`.

The following packages are required to run DocGPT:

```
langchain    # Required.
chromadb     # Required.
tiktoken     # Required.
pdfminer.six # Optional. Only required for .pdf documents.
unstructured # Optional. Only required for .doc and .docx documents.
tabulate     # Optional. Only required for .doc and .docx documents.
```

<a id="funcgpt"></a>
### FuncGPT

![Alt Text](https://raw.githubusercontent.com/sbslee/kanu/main/images/funcgpt.gif)

The following packages are required to run FuncGPT:

```
openai # Required.
```

## Changelog

See the [CHANGELOG.md](https://github.com/sbslee/kanu/blob/main/CHANGELOG.md) file for details.