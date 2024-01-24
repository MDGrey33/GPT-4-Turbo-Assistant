#!/bin/bash

# Install dependencies from requirements.txt
pip install -r requirements.txt

# Check if credentials.py already exists
if [ ! -f credentials.py ]; then
    # Enhanced prompt for the OpenAI API key
    echo -e "\033[1;32mPlease enter your OpenAI API key: \033[0m"
    read openai_api_key

    # Create credentials.py and add the API key
    echo "API_KEY='${openai_api_key}'" > credentials.py
else
    echo "credentials.py already exists. Skipping API key input."
fi

# Get the current directory using pwd and store it in a variable
current_directory=$(pwd)

# Set the PYTHONPATH environment variable
export PYTHONPATH="${PYTHONPATH}:${current_directory}"

# Run the openai_assistant module
python -m chat_bot.openai_assistant
