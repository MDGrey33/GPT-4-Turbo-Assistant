from oai_assistants.openai_assistant import create_assistant, add_file_to_assistant, chat_with_assistant
from oai_assistants.utility import initiate_client
from oai_assistants.file_manager import FileManager
from oai_assistants.thread_manager import ThreadManager
from oai_assistants.assistant_manager import AssistantManager


def create_new_assistant():
    """
    Creates a new assistant with the specified parameters.
    """
    # initialize openai client
    client = initiate_client()

    # Define assistant parameters
    new_assistant = {
        "model": "gpt-4-1106-preview",
        "name": "Shams",
        "instructions": """You are the Q&A Assistant, 
        you know everything about the uploaded files
        and you review them and answer primarily from their content
        if you ever answer from outside the files, you will be penalized
        if you use your knowledge to explain some information from outside the file, you will clearly state that.
        """,
        "tools": [{"type": "code_interpreter"}, {"type": "retrieval"}],
        "description": "The ultimate librarian",
        "file_ids": []
    }

    # Creating assistant
    assistant = create_assistant(client, new_assistant)
    print(assistant)
    return assistant


def add_files_to_assistant(assistant, file_id):
    """
    Adds a file to an assistant's list of files.
    """
    # initialize openai client
    client = initiate_client()

    # Uploading file to Open AI
    chosen_file_path = f"/Users/roland/code/Nur/content/file_system/{file_id}.txt"
    purpose = "assistants"
    file_manager = FileManager(client)
    file_id = file_manager.create(chosen_file_path, purpose)
    print(f"File uploaded successfully with ID: {file_id}")

    # Adding file to assistant
    # Adding file to assistant
    assistant_manager = AssistantManager(client)
    assistant_manager.add_file_to_assistant(assistant.id, file_id)
    print(f"File {chosen_file_path} added to assistant {assistant.id}")


def ask_assistant(assistant, question):
    """
    Asks an assistant a question.
    """
    # initialize openai client
    client = initiate_client()

    # Creating a thread manager
    thread_manager = ThreadManager(client, assistant.id)
    thread_manager.create_thread()
    question = (f"You will answer the following question with a summary, then provide a comprehensive answer, "
                f"then provide the references aliasing them as Technical trace: {question}")
    messages = thread_manager.add_message_and_wait_for_reply(question, [])
    return messages


def get_response_from_assistant(question, page_ids):
    # Creating a new assistant
    assistant = create_new_assistant()

    # adding files to assistant
    add_files_to_assistant(assistant, page_ids)

    # Ask assistant
    messages = ask_assistant(assistant, question)
    print(messages)


if __name__ == "__main__":
    get_response_from_assistant("Do we support payment matching in our solution?", "458841")

