import time
from openai import OpenAI
from credentials import openai_key
from chat_bot.files import File, manage_files, chose_and_upload_file
from chat_bot.assistants import AssistantManager


def initiate_client():
    client = OpenAI(api_key=openai_key)
    return client


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

    def add_message_and_wait_for_reply(self, user_message, message_files):
        """
        Adds a message to the thread and waits for a reply from the assistant.

        Args:
            message_content: The content of the user's message.
        """
        # Add the user's message to the thread
        self.client.beta.threads.messages.create(
            thread_id=self.thread_id,
            role="user",
            content=user_message,
            file_ids=message_files
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
        # update the loop to be multiline
        while True:
            user_message = ""
            message_files = []
            print("You: \nWrite your message, or write 'DONE' to finish the message, or 'QUIT' to abort the chat.")
            user_input = input()
            if user_input.lower() == 'quit':
                break
            else:
                while user_input.lower() != "done":
                    user_message = (user_message + user_input + "\n")
                    user_input = ""
                    user_input = input()
                while True:
                    action = input("If you want add a file type 1 else type 2")
                    if action == "1":
                        file_id = chose_and_upload_file(client, file_path='context_update')
                        message_files.append(file_id)
                    elif action == "2":
                        break
            self.add_message_and_wait_for_reply(user_message, message_files)


new_assistant = {
    "model": "gpt-4-1106-preview",
    "name": "Laura",
    "instructions": """You are the ultimate librarian, you know everything about the files attached to you
     and you review them and answer primarily from their content""",
    "tools": [{"type": "code_interpreter"}, {"type": "retrieval"}],
    "description": "The ultimate librarian",
    "file_ids": []
}


def list_assistants(assistant_manager):
    # List assistants
    print("Available Assistants:")
    assistants = assistant_manager.list_assistants().data
    for index, assistant in enumerate(assistants, start=1):
        print(f"{index}. {assistant.name} (ID: {assistant.id})")
    return assistants


def chose_assistant(assistant_manager, assistants):
    assistant_index = input("Enter the number of the assistant you want to manage or 'c' to cancel: ")
    if assistant_index.lower() == 'c':
        print("Operation canceled.")
        return
    assistant_index = int(assistant_index) - 1

    if 0 <= assistant_index < len(assistants):
        selected_assistant = assistants[assistant_index]
        assistant_id = selected_assistant.id
        assistant_manager.print_assistant_details(assistant_id)
    else:
        print("Invalid assistant number.")
    return assistant_id


def chose_assistant_action():
    print("\n1. Chat with this assistant")
    print("2. Add file to assistant")
    print("3. Update this assistant")
    print("4. Delete this assistant")
    print("5. Cancel")
    action = input("Choose an option: ")
    return action


def add_file_to_assistant(assistant_manager, assistant_id):
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


def manage_assistants(client: OpenAI):
    assistant_manager = AssistantManager(client)
    assistants = list_assistants(assistant_manager)
    assistant_id = chose_assistant(assistant_manager, assistants)
    action = chose_assistant_action()
    if action == '1':
        # Chat with assistant
        thread_manager = ThreadManager(client, assistant_id)
        thread_manager.chat()
    elif action == '2':
        # Add file to assistant
        add_file_to_assistant(assistant_manager, assistant_id)
    elif action == '3':
        # Update assistant parameters
        # Call the interactive update method from AssistantManager
        assistant_manager.update_assistant_interactively(assistant_id)
        print("Assistant updated successfully.")
    elif action == '4':
        # Delete the assistant
        delete_message = assistant_manager.delete_assistant(assistant_id)
        print(delete_message)
    elif action == '5':
        # exit menu
        print("Operation canceled.")
    else:
        print("Invalid action.")


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
