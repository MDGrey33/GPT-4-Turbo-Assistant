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
echo "Please enter your OpenAI API key:"
read openai_api_key

# Create credentials.py and add the API key
echo "openai_key='${openai_api_key}'" > credentials.py

# Get the current directory using pwd and store it in a variable
current_directory=$(pwd)

# Set the PYTHONPATH environment variable
export PYTHONPATH="${PYTHONPATH}:${current_directory}"

# Run the openai_assistant module
python -m chat_bot.openai_assistant