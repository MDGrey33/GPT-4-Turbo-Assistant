import time
from openai import OpenAI


class AssistantChat:
    def __init__(self, api_key, assistant_name, assistant_instructions, model):
        self.client = OpenAI(api_key=api_key)
        self.assistant_name = assistant_name
        self.assistant_instructions = assistant_instructions
        self.model = model
        self.assistant_id = None
        self.thread_id = None

    def create_assistant(self):
        assistant = self.client.beta.assistants.create(
            name=self.assistant_name,
            instructions=self.assistant_instructions,
            tools=[{"type": "code_interpreter"}],
            model=self.model
        )
        self.assistant_id = assistant.id

    def summon_assistant(self, assistant_id):
        self.assistant_id = assistant_id

    def create_thread(self):
        thread = self.client.beta.threads.create()
        self.thread_id = thread.id

    def add_message(self, user_role, message_content):
        return self.client.beta.threads.messages.create(
            thread_id=self.thread_id,
            role=user_role,
            content=message_content
        )

    def run_assistant(self):
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
        self.create_assistant()
        self.create_thread()

        while True:
            user_input = input("You: ")
            if user_input.lower() == 'quit':
                break
            self.add_message("user", user_input)
            run = self.run_assistant()

            # Loop to check the response status of the assistant
            while True:
                run_status = self.check_run_status(run.id)
                if run_status.status == "completed":
                    messages = self.retrieve_messages()
                    self.display_messages(messages)
                    break
                else:
                    print("...")
                    time.sleep(2)


if __name__ == "__main__":
    open_ai_key = #your api key here
    assistant_chat = AssistantChat(
        api_key=open_ai_key,
        assistant_name="Sam",
        assistant_instructions="""You are a sarcastic agent who will make fun of anything""",
        model="gpt-4-1106-preview"
    )
    assistant_chat.chat()
