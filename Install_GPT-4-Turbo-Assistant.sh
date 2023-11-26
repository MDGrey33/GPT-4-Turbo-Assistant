#!/bin/bash

# Function to check if Conda is installed
check_conda_installed() {
    which conda >/dev/null
}

# Function to install Miniconda
install_miniconda() {
    echo "Downloading Miniconda..."
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh
    echo "Installing Miniconda..."
    bash miniconda.sh -b -p $HOME/miniconda
    rm miniconda.sh
    echo "Miniconda installed."
}

# Function to create and activate virtual environment
setup_environment() {
    local env_name=$1
    echo "Creating and activating environment '$env_name'..."
    conda create -n "$env_name" python=3.8 -y
    source activate "$env_name"
    echo "Environment '$env_name' is ready."
}

# Main script execution for Miniconda and environment setup
if check_conda_installed; then
    echo "Conda is already installed."
else
    install_miniconda
    eval "$($HOME/miniconda/bin/conda shell.bash hook)"
fi

ENV_NAME="gpt4-turbo-env"
setup_environment "$ENV_NAME"

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
