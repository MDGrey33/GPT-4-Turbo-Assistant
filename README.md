# GPT-4-Turbo-Assistant 

This is an implementation of GPT-4-Turbo assistant on Python.

[Ask this GPT any questions you have about this code.](https://chat.openai.com/g/g-yJoNW6R47-gpt-4-turbo-assistants-python-dev)

## Getting Started with GPT-4-Turbo-Assistant

### In a hurry?
Let me do the job for you : )

put the following code in a file called Install_GPT-4-Turbo-Assistant.sh
```bash
#!/bin/bash

# Define the Git repository URL
git_repo_url="https://github.com/MDGrey33/GPT-4-Turbo-Assistant.git"

# Define the directory name of the cloned repository
repo_dir_name="GPT-4-Turbo-Assistant"

# Clone the Git repository
git clone $git_repo_url

# Change directory to the cloned repository
cd $repo_dir_name

# Install dependencies from requirements.txt
pip install -r requirements.txt

# Ask the user for the OpenAI API key
echo -e "\033[1;32mPlease enter your OpenAI API key: \033[0m"
read openai_api_key

# Create credentials.py and add the API key
echo "openai_key='${openai_api_key}'" > credentials.py

# Get the current directory using pwd and store it in a variable
current_directory=$(pwd)

# Set the PYTHONPATH environment variable
export PYTHONPATH="${PYTHONPATH}:${current_directory}"

# Run the openai_assistant module
python -m chat_bot.openai_assistant

```
run chmod +x Install_GPT-4-Turbo-Assistant.sh

./Install_GPT-4-Turbo-Assistant.sh

This will download the repo set the variable and get you up and running.

### Want to know whats happening?

This guide will help you set up and start using the GPT-4-Turbo-Assistant.

#### Step 1: Clone the Repository
```bash
git clone https://github.com/MDGrey33/GPT-4-Turbo-Assistant
cd GPT-4-Turbo-Assistant
```

#### Step 2: Install Requirements
```bash
pip install -r requirements.txt
```

#### Step 3: Set Up Credentials
Replace 'your_openai_api_key' with your actual OpenAI API key in credentials.py.
```
"API_KEY='your_openai_api_key'"
```

#### Step 4: Run the Assistant Script in your favorite interpreter
```
./chat_bot/openai_assistant.py
```

#### Step 5: Create an Assistant
Follow the menu prompts to create a new assistant.

#### Step 6: Chat with an Assistant
Choose an assistant from the list
Select the option to chat with the assistant.

## What is GPT-4-Turbo-Assistant

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
