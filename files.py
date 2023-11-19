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


# Additional function to select a file for upload
def select_file_for_upload(file_path):
    all_files = get_all_files_in_path(file_path)
    print("Please select a file to upload:")
    for idx, file_name in enumerate(all_files):
        print(f"{idx + 1}. {file_name}")
    selected_index = int(input("Enter the number of the file you want to upload: ")) - 1
    if 0 <= selected_index < len(all_files):
        return all_files[selected_index]
    else:
        print("Invalid selection.")
        return None


def chose_and_upload_file(client, file_path='context_update'):
    file_manager = File(client)
    chosen_file_path = select_file_for_upload(file_path)
    if chosen_file_path:
        print("Select the purpose of the file:")
        print("1. Fine-tune")
        print("2. Assistants")
        print("3. Fine-tune results")
        print("4. Assistants output")
        purpose_choice = input("Enter the number for the purpose (1, 2, 3 or 4):")
        if purpose_choice == "1":
            purpose = "fine-tune"
        elif purpose_choice == "2":
            purpose = "assistants"
        elif purpose_choice == "3":
            purpose = "fine-tune-results"
        elif purpose_choice == "4":
            purpose = "assistants_output"
        else:
            print("Invalid option.")
            return
        file_id = file_manager.create(chosen_file_path, purpose)
        print(f"File uploaded successfully with ID: {file_id}")
        return file_id


# Function outside the class to manage files
def manage_files(client: OpenAI):
    file_manager = File(client)
    files = file_manager.list()

    print("Available Files:")
    for file_id, file_data in files.items():
        print(f"ID: {file_id}, Filename: {file_data['filename']}, Purpose: {file_data['purpose']}")

    print("1. Delete file\n2. Upload file \n3. Cancel")
    choice = input("Select an option: ")
    if choice == '1':
        file_id_to_delete = input("Enter the ID of the file you want to delete: ")
        if file_id_to_delete in files:
            status = file_manager.delete(file_id_to_delete)
            print(status)
        else:
            print("Invalid File ID.")
    elif choice == '2':
        file_id = chose_and_upload_file(client)
        return file_id
    elif choice == '3':
        print("Canceling...")
        return
    else:
        print("Invalid option.")


def create_file(client: OpenAI, file_path, purpose):
    file_manager = File(client)
    file_id = file_manager.create(file_path, purpose)
    return file_id


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


new_file = {
    "file_path": "context/context.txt",
    "purpose": "assistants"
}


def test_file_creation():
    client = initiate_client()
    file_id = create_file(client, new_file['file_path'], new_file['purpose'])
    print(file_id)
    file_to_delete = File(client)
    file_to_delete.delete(file_id)
