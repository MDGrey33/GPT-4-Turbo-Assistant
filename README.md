# GPT-4-Turbo-Assistant 

This is an implementation of GPT-4-Turbo assistant on Python.

## Getting Started with GPT-4-Turbo-Assistant

This guide will help you set up and start using the GPT-4-Turbo-Assistant.

### Step 1: Clone the Repository
```bash
git clone https://github.com/MDGrey33/GPT-4-Turbo-Assistant
cd GPT-4-Turbo-Assistant
```

### Step 2: Install Requirements
```bash
pip install -r requirements.txt
```

### Step 3: Set Up Credentials
Replace 'your_openai_api_key' with your actual OpenAI API key in credentials.py.
```
"API_KEY='your_openai_api_key'"
```

### Step 4: Run the Assistant Script in your favorite interpreter
```
./chat_bot/openai_assistant.py
```

### Step 5: Create an Assistant
Follow the menu prompts to create a new assistant.

### Step 6: Chat with an Assistant
Choose an assistant from the list
Select the option to chat with the assistant.

## What is GPT-4-Turbo-Assistant

[Ask this GPT any questions you have about this code.](https://chat.openai.com/g/g-yJoNW6R47-gpt-4-turbo-assistants-python-dev)

[YouTube video showing how it works kind of recorded QA](https://youtu.be/4KgEMO4Ufis)

[Video showing how I added a file to the assistant context](https://youtu.be/34IfrpEQMMA)

I will go into more detail about it as I explore more, feel free to contribute.

For now, it implements the conversation with the extended context and code interpreter.


## Current functionality:

* Create assistant
* List existing assistants
* Load existing assistant
* Associate a file in the assistant knowledge
* Associate multiple files in the assistant knowledge
* Update assistant parameters
* Uploading a file and assigning its purpose
* Getting a list of uploaded files
* Deleting a file
* Chat with GPT-4 Turbo with long context
* Loading files in messages
* Auto clean up deleted files from an assistant on file add and update.

## Todo list
This is an implementation of GPT-4-Turbo assistant on Python.  
I will elaborate on it as I explore more, feel free to request features or contribute For now it implements the conversation with the extended context and code interpreter.

Todo list

* ~~Loading existing assistant~~
* ~~Loading a file in the assistants' conversation context~~
* ~~Deleting existing assistant~~
* ~~Uploading multiple files~~
* ~~Deleting a file from the Assistants conversation context~~
* ~~Editing existing assistant~~
* ~~Loading files in messages~~
* Loading existing conversation
* Downloading files from the code interpreter
* Loading images in conversation
* Generating Images with Dali3
