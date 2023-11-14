from openai import OpenAI
from credentials import openai_key


def initiate_client():
    client = OpenAI(api_key=openai_key)
    return client


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
