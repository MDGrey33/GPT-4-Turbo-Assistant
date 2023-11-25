import time


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
