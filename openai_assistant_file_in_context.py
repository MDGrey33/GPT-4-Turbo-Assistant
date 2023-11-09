import time
from openai import OpenAI
from credentials import openai_key


class AssistantChat:
    def __init__(self, api_key, assistant_name, assistant_instructions, model, file_path):
        self.client = OpenAI(api_key=api_key)
        self.assistant_name = assistant_name
        self.assistant_instructions = assistant_instructions
        self.model = model
        self.assistant_id = None
        self.thread_id = None
        self.file_path = file_path
        self.file_id = None

    def upload_file(self):
        with open(self.file_path, 'rb') as file:
            # Create a file with the purpose 'assistants'
            response = self.client.files.create(
                file=file,
                purpose='assistants'
            )
            self.file_id = response.id

    def create_assistant(self):
        if self.file_id is None:
            self.upload_file()

        assistant = self.client.beta.assistants.create(
            name=self.assistant_name,
            instructions=self.assistant_instructions,
            tools=[{"type": "code_interpreter"}, {"type": "retrieval"}],
            model=self.model,
            file_ids=[self.file_id]  # Attach the file by its ID
        )
        self.assistant_id = assistant.id

    def list_assistants(self):
        return self.client.beta.assistants.list()

    def load_assistant(self, assistant_id):
        try:
            assistant = self.client.beta.assistants.retrieve(assistant_id=assistant_id)
            self.assistant_id = assistant.id
            print(f"Loaded assistant '{assistant.name}' with ID: {assistant.id}")
        except Exception as e:
            print(f"An error occurred while loading the assistant: {e}")

    def create_thread(self):
        thread = self.client.beta.threads.create()
        self.thread_id = thread.id

    def add_message(self, user_role, message_content):
        return self.client.beta.threads.messages.create(
            thread_id=self.thread_id,
            role=user_role,
            content=message_content
        )

    def run_thread(self):
        return self.client.beta.threads.runs.create(
            thread_id=self.thread_id,
            assistant_id=self.assistant_id,
        )

    def check_run_status(self, run_id):
        return self.client.beta.threads.runs.retrieve(
            thread_id=self.thread_id,
            run_id=run_id
        )

    def retrieve_messages(self):
        return self.client.beta.threads.messages.list(
            thread_id=self.thread_id
        )

    def display_messages(self, messages):
        for message in messages.data:
            if message.role == "assistant":
                print(f"Assistant: {message.content[0].text.value}")

    def chat(self):
        print("Welcome to Assistant Chat!")
        print("1. Create a new assistant")
        print("2. Load an existing assistant")

        try:
            choice = int(input("Select an option (1 or 2): "))
        except ValueError:
            print("Invalid input. Please enter a number (1 or 2).")
            return

        if choice == 1:
            self.create_assistant()
            self.create_thread()
        elif choice == 2:
            assistants_list = self.list_assistants()
            print("Here are the available assistants:")
            for idx, assistant in enumerate(assistants_list.data):
                print(f"{idx + 1}. {assistant.name} (ID: {assistant.id})")

            try:
                selected_idx = int(input("Enter the number of the assistant you want to load: ")) - 1
                if 0 <= selected_idx < len(assistants_list.data):
                    selected_assistant = assistants_list.data[selected_idx]
                    self.load_assistant(selected_assistant.id)
                    self.create_thread()
                else:
                    print("Invalid selection. Exiting the program.")
                    return
            except ValueError:
                print("Invalid input. Please enter a number.")
                return
            except Exception as e:
                print(f"An error occurred while loading the assistant: {e}")
                return
        else:
            print("Invalid option. Exiting the program.")
            return

        while True:
            user_input = input("You: ")
            if user_input.lower() == 'quit':
                break
            self.add_message("user", user_input)
            run = self.run_thread()

            # Loop to check the response status of the assistant
            counter = 0
            while True:
                run_status = self.check_run_status(run.id)
                if run_status.status == "completed":
                    messages = self.retrieve_messages()
                    self.display_messages(messages)
                    break
                else:
                    print("...")
                    time.sleep(2)
                    counter += 1
                    if counter > 10:
                        print("Please check the API status on https://status.openai.com/")
                        counter = 0


if __name__ == "__main__":
    assistant_chat = AssistantChat(
        api_key=openai_key,
        model="gpt-4-1106-preview",
        assistant_name="Laura",
        assistant_instructions="""You are the ultimate librarian, you know everything about the files attached to you 
        and you review them and answer primarily from their content""",
        file_path="context/context.txt"
    )
    assistant_chat.chat()
