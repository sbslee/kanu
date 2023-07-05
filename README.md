# README

[![PyPI](https://badge.fury.io/py/kanu.svg)](https://badge.fury.io/py/kanu)

Welcome to KANU, a minimalistic Python-based GUI for various chatbots.

There are currently four chatbots available in KANU:

- [ChatGPT](#chatgpt) harnesses the power of OpenAI's ChatGPT, bringing it directly to your local computer
- [DocGPT](#docgpt) allows you to effortlessly interact with your documents and ask questions about them
- [FuncGPT](#funcgpt) can answer your questions by making calls to external tools, APIs, or databases
- [ChatPaLM](#chatpalm) harnesses the power of Google's PaLM API, bringing it directly to your local computer

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

You can customize the chatbot parameters by directly editing the configuration file or by using the GUI. The configuration file is in the following format:

```
[DEFAULT]
model = gpt-3.5-turbo
temperature = 0.5
prompt = You are a helpful assistant.

[USER]
openai_key = 
```

<a id="docgpt"></a>
### DocGPT

![Alt Text](https://raw.githubusercontent.com/sbslee/kanu/main/images/docgpt.gif)

DocGPT currently supports the following document formats: `.csv`, `.doc`, `.docx`, `.pdf`, and `.txt`.

The following packages are required to run DocGPT:

```
openai       # Required.
langchain    # Required.
chromadb     # Required.
tiktoken     # Required.
pdfminer.six # Optional. Only required for .pdf documents.
unstructured # Optional. Only required for .doc and .docx documents.
tabulate     # Optional. Only required for .doc and .docx documents.
```

You can customize the chatbot parameters by directly editing the configuration file or by using the GUI. The configuration file is in the following format:

```
[DEFAULT]
model = gpt-3.5-turbo
temperature = 0.5
prompt = Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.
	
	{context}
	
	Question: {question}
	Helpful Answer:
chunk_size = 1000
chunk_overlap = 50

[USER]
openai_key = 

[OPTIONAL]
new_database_directory = 
document_directory = 
existing_database_directory = 
```

<a id="funcgpt"></a>
### FuncGPT

![Alt Text](https://raw.githubusercontent.com/sbslee/kanu/main/images/funcgpt.gif)

The following packages are required to run FuncGPT:

```
openai # Required.
```

There may be additional dependencies depending on the external tools, APIs, or databases you use. You are responsible for installing these dependencies.

You can customize the chatbot parameters by directly editing the configuration file or by using the GUI. The configuration file is in the following format:

```
[DEFAULT]
model = gpt-3.5-turbo-0613
temperature = 0.5
prompt = You are a helpful assistant.

[USER]
openai_key = 
function_script = 
```

Note that the script provided by the user must contain a dictionary variable defined as `functions`, which is imported by FuncGPT. Below is an example script:

```
import json

def get_current_weather(location, unit="fahrenheit"):
    weather_info = {
        "location": location,
        "temperature": "72",
        "unit": unit,
        "forecast": ["sunny", "windy"],
    }
    return json.dumps(weather_info)

get_current_weather_json = {
    "name": "get_current_weather",
    "description": "Get the current weather in a given location",
    "parameters": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "The city and state, e.g. San Francisco, CA",
            },
            "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
        },
        "required": ["location"],
    },
}

functions = {
    "get_current_weather": {
        "function": get_current_weather,
        "json": get_current_weather_json,
    }
}
```

<a id="chatpalm"></a>
### ChatPaLM

![Alt Text](https://raw.githubusercontent.com/sbslee/kanu/main/images/chatpalm.gif)

The following packages are required to run ChatPaLM:

```
google.generativeai # Required.
```

You can customize the chatbot parameters by directly editing the configuration file or by using the GUI. The configuration file is in the following format:

```
[DEFAULT]
model = chat-bison-001
temperature = 0.5
prompt = You are a helpful assistant.

[USER]
google_key = 
```

## Changelog

See the [CHANGELOG.md](https://github.com/sbslee/kanu/blob/main/CHANGELOG.md) file for details.