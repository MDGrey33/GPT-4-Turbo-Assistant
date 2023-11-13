import time
from openai import OpenAI
from credentials import openai_key
import os


def initiate_client():
    client = OpenAI(api_key=openai_key)
    return client


def get_all_files_in_path(file_path):
    """
    Returns a list of all file paths within the specified directory and its subdirectories.
    Skips '.DS_Store' files common on macOS.

    Args:
    - directory (str): The path to the directory.

    Returns:
    - list: A list of file paths.
    """
    all_file_paths = []
    for root, _, files in os.walk(file_path):
        for file in files:
            if file != '.DS_Store':
                all_file_paths.append(os.path.join(root, file))
    return all_file_paths


class File:
    def __init__(self, client: OpenAI):
        self.client = client.files

    def create(self, file_path, purpose):
        with open(file_path, 'rb') as file_object:
            response = self.client.create(file=file_object, purpose=purpose)
            return response.id

    def list(self):
        files_data = self.client.list().data
        return {file.id: {"filename": file.filename, "purpose": file.purpose} for file in files_data}

    def delete(self, file_id):
        self.client.delete(file_id)
        return f"File with ID {file_id} has been deleted."


# Function outside the class to manage files
def manage_files(client: OpenAI):
    file_manager = File(client)
    files = file_manager.list()

    print("Available Files:")
    for file_id, file_data in files.items():
        print(f"ID: {file_id}, Filename: {file_data['filename']}, Purpose: {file_data['purpose']}")

    print("1. Delete file\n2. Cancel")
    choice = input("Select an option: ")
    if choice == '1':
        file_id_to_delete = input("Enter the ID of the file you want to delete: ")
        if file_id_to_delete in files:
            status = file_manager.delete(file_id_to_delete)
            print(status)
        else:
            print("Invalid File ID.")
    elif choice == '2':
        print("Canceling...")
        return
    else:
        print("Invalid option.")


def create_file(client: OpenAI, file_path, purpose):
    file_manager = File(client)
    file_id = file_manager.create(file_path, purpose)
    return file_id


class AssistantManager:
    def __init__(self, client):
        self.client = client.beta.assistants

    def create_assistant(self, model, name, instructions, tools, description=None, metadata=None):
        """
        Create an assistant without files.

        Args:
            model: ID of the model to use for the assistant.
            name (optional): The name of the assistant.
            instructions (optional): Instructions for the system using the assistant.
            description (optional): A descriptive text for the assistant.
            metadata (optional): Metadata in key-value format for the assistant.
            tools (optional): A list of tools enabled on the assistant.

        Returns:
            The newly created Assistant object.
        """
        response = self.client.create(
            model=model,
            name=name,
            instructions=instructions,
            description=description,
            metadata=metadata,
            tools=tools
        )
        return response

    def add_file_to_assistant(self, assistant_id, file_id):
        """
        Add a file to an assistant's list of files.

        Args:
            assistant_id: The ID of the assistant being updated.
            file_id: The ID of the file to add to the assistant.

        Returns:
            The updated Assistant object.
        """
        assistant = self.client.retrieve(assistant_id)
        # Use direct attribute access instead of the 'get' method
        existing_file_ids = assistant.file_ids if assistant.file_ids is not None else []
        updated_file_ids = existing_file_ids + [file_id]

        response = self.client.update(
            assistant_id=assistant_id,
            file_ids=updated_file_ids
        )
        return response

    def list_assistants(self):
        """
        List all assistants.

        Returns:
            A list of Assistant objects containing details about each assistant.
        """
        return self.client.list()

    def load_assistant(self, assistant_id):
        """
        Load an assistant's parameters by ID.

        Args:
            assistant_id: The unique identifier for the assistant.

        Returns:
            An Assistant object or details about the assistant.
        """
        return self.client.retrieve(assistant_id=assistant_id)

    def print_assistant_details(self, assistant_id):
        """
        Retrieve and display the parameters of a specific assistant by ID.

        Args:
            assistant_id: The unique identifier for the assistant.
        """
        assistant = self.load_assistant(assistant_id)
        assistant_details = assistant.model_dump()
        print(assistant_details)

    def delete_assistant(self, assistant_id):
        """
        Delete an assistant by ID.

        Args:
            assistant_id: The unique identifier for the assistant.

        Returns:
            A confirmation message indicating that the assistant was deleted.
        """
        response = self.client.delete(assistant_id=assistant_id)
        return ("Assistant deleted successfully.")


class ThreadManager:
    def __init__(self, client, assistant_id):
        """
        Initializes the ThreadManager with an OpenAI client and an assistant ID.

        Args:
            client: The OpenAI client object.
            assistant_id: The ID of the assistant to use for the chat.
        """
        self.client = client
        self.assistant_id = assistant_id
        self.thread_id = None

    def create_thread(self):
        """
        Creates a new thread.
        """
        thread = self.client.beta.threads.create()
        self.thread_id = thread.id

    def add_message_and_wait_for_reply(self, message_content):
        """
        Adds a message to the thread and waits for a reply from the assistant.

        Args:
            message_content: The content of the user's message.
        """
        # Add the user's message to the thread
        self.client.beta.threads.messages.create(
            thread_id=self.thread_id,
            role="user",
            content=message_content
        )

        # Request the assistant to process the message
        run = self.client.beta.threads.runs.create(
            thread_id=self.thread_id,
            assistant_id=self.assistant_id,
        )

        # Wait for a response from the assistant
        run_status = self.check_run_status(run.id)
        while run_status.status != "completed":
            print("Waiting for assistant...")
            time.sleep(2)
            run_status = self.check_run_status(run.id)

        # Retrieve and display the messages
        messages = self.retrieve_messages()
        self.display_messages(messages)

    def check_run_status(self, run_id):
        """
        Checks the status of a run in the thread.

        Args:
            run_id: The ID of the run to check.
        """
        return self.client.beta.threads.runs.retrieve(
            thread_id=self.thread_id,
            run_id=run_id
        )

    def retrieve_messages(self):
        """
        Retrieves messages from the thread.
        """
        return self.client.beta.threads.messages.list(
            thread_id=self.thread_id
        )

    def display_messages(self, messages):
        """
        Displays messages from the assistant in the thread.
        """
        for message in messages.data:
            if message.role == "assistant":
                print(f"Assistant: {message.content[0].text.value}")

    def chat(self):
        """
        Manages the chat interaction between the user and the assistant.
        """
        print("Welcome to the Assistant Chat!")
        self.create_thread()

        while True:
            user_input = input("You: ")
            if user_input.lower() == 'quit':
                break
            self.add_message_and_wait_for_reply(user_input)


new_assistant = {
    "model": "gpt-4-1106-preview",
    "name": "Laura",
    "instructions": """You are the ultimate librarian, you know everything about the files attached to you
     and you review them and answer primarily from their content""",
    "tools": [{"type": "code_interpreter"}, {"type": "retrieval"}],
    "description": "The ultimate librarian",
    "file_ids": []
}

new_file = {
    "file_path": "context/context.txt",
    "purpose": "assistants"
}


def manage_assistants(client: OpenAI):
    assistant_manager = AssistantManager(client)

    # List assistants
    print("Available Assistants:")
    assistants = assistant_manager.list_assistants().data
    for index, assistant in enumerate(assistants, start=1):
        print(f"{index}. {assistant.name} (ID: {assistant.id})")

    assistant_index = input("Enter the number of the assistant you want to manage or 'c' to cancel: ")
    if assistant_index.lower() == 'c':
        print("Operation canceled.")
        return
    assistant_index = int(assistant_index) - 1

    if 0 <= assistant_index < len(assistants):
        selected_assistant = assistants[assistant_index]
        assistant_id = selected_assistant.id
        assistant_manager.print_assistant_details(assistant_id)

        # Update numbered options
        print("\n1. Chat with this assistant")
        print("2. Add file to assistant")
        print("3. Delete this assistant")
        print("4. Cancel")
        action = input("Choose an option: ")

        if action == '1':
            thread_manager = ThreadManager(client, assistant_id)
            thread_manager.chat()
        elif action == '2':
            # List files
            file_manager = File(client)
            files = file_manager.list()
            print("Available Files:")
            for file_id, file_data in files.items():
                print(f"ID: {file_id}, Filename: {file_data['filename']}, Purpose: {file_data['purpose']}")

            file_id_to_add = input("Enter the ID of the file you want to add or 'c' to cancel: ")
            if file_id_to_add.lower() == 'c':
                print("Operation canceled.")
            elif file_id_to_add in files:
                assistant_manager.add_file_to_assistant(assistant_id, file_id_to_add)
                print("File added successfully.")
                assistant_manager.print_assistant_details(assistant_id)
            else:
                print("Invalid File ID.")
        elif action == '3':
            # Delete the assistant
            delete_message = assistant_manager.delete_assistant(assistant_id)
            print(delete_message)
        elif action == '4':
            print("Operation canceled.")
        else:
            print("Invalid action.")
    else:
        print("Invalid assistant number.")


def user_interaction(client):
    while True:
        print("\nUser Interaction Menu:")
        print("1. Manage files")
        print("2. Manage assistants")
        print("3. Create a new assistant")
        print("4. Exit")

        try:
            choice = int(input("Enter the number of the operation you want to perform: "))
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            continue

        if choice == 1:
            manage_files(client)
        elif choice == 2:
            manage_assistants(client)
        elif choice == 3:
            assistant_manager = AssistantManager(client)
            created_assistant = assistant_manager.create_assistant(
                new_assistant['model'],
                new_assistant['name'],
                new_assistant['instructions'],
                new_assistant['tools'],
                new_assistant['description']
            )
            print(f"New assistant created with ID: {created_assistant.id}")
        elif choice == 4:
            break
        else:
            print("Invalid choice. Please select a valid option.")


def test_file_creation():
    file_id = create_file(client, new_file['file_path'], new_file['purpose'])
    print(file_id)
    file_to_delete = File(client)
    file_to_delete.delete(file_id)


def test_assistant_manager(client, new_assistant, file_id):
    assistant_manager = AssistantManager(client)

    # 1. Create an assistant
    print("Creating an assistant...")
    returned_assistant = assistant_manager.create_assistant(
        model=new_assistant['model'],
        name=new_assistant['name'],
        instructions=new_assistant['instructions'],
        description=new_assistant['description'],
        tools=new_assistant['tools']
    )
    assistant_id = returned_assistant.id
    print(f"Assistant created with ID: {assistant_id}")

    # 2. List assistants
    print("\nListing assistants...")
    all_assistants = assistant_manager.list_assistants()
    print("Here are the available assistants:")
    for idx, assistant in enumerate(all_assistants.data):
        print(f"{idx + 1}. {assistant.name} (ID: {assistant.id})")

    # 3. Load the assistant
    print(f"\nLoading assistant {assistant_id}...")
    assistant_loaded = assistant_manager.load_assistant(assistant_id)
    print("Assistant details:")
    assistant_manager.print_assistant_details(assistant_id)

    # 4. Add a file to the assistant
    print(f"\nAdding file {file_id} to assistant {assistant_id}...")
    assistant_manager.add_file_to_assistant(assistant_id, file_id)

    # 5. Print the assistant details again
    print(f"\nAssistant {assistant_id} details after adding file:")
    assistant_manager.print_assistant_details(assistant_id)

    # 6. Delete the assistant
    print(f"\nDeleting assistant {assistant_id}...")
    delete_message = assistant_manager.delete_assistant(assistant_id)
    print(delete_message)

    # 7. List all assistants to confirm deletion
    print("\nListing assistants after deletion...")
    all_assistants_after_deletion = assistant_manager.list_assistants()
    print("Here are the available assistants:")
    for idx, assistant in enumerate(all_assistants_after_deletion.data):
        print(f"{idx + 1}. {assistant.name} (ID: {assistant.id})")


if __name__ == "__main__":
    client = initiate_client()
    # test_file_creation()
    # manage_files(client)
    # test_assistant_manager(client, new_assistant, "file-ODu0UuYbrx5ech6lKbHWvol4")
    # manage_assistants(client)
    user_interaction(client)
