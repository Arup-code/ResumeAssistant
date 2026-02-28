import os
from google import genai
from google.genai import types

from constants import ROOT_DIR
from src.service.fs_tools import read_file, list_files, write_file, search_in_file
from dotenv import load_dotenv

load_dotenv()
# Check for API key
if not os.getenv("GOOGLE_API_KEY"):
    print("Warning: GOOGLE_API_KEY environment variable not found. Please set it before running.")
    quit()

class LLMFileAssistant:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model_name = "gemini-2.5-flash"
        self.tools = [read_file, list_files, write_file, search_in_file]
        self.chat = self.client.chats.create(
            model=self.model_name,
            config=types.GenerateContentConfig(
                tools=self.tools,
                automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=False),
                system_instruction=[
                    load_prompt()
                ]
            )
        )

    def process_query(self, query: str):
        """
        Process a user query using the LLM and available tools.
        """
        try:
            response = self.chat.send_message(query)
            return response.text
        except Exception as e:
            print(f"Error processing query: {str(e)}")
            quit()



def load_prompt():
    return open(f'{ROOT_DIR}/src/model/PROMPT.md').read()

# Example usage
if __name__ == "__main__":
    assistant = LLMFileAssistant()

    # Example queries to test
    queries = [
        "List all files in the current directory",
        "Read all resumes in the src directory", # Assuming resumes might be there for test
        "Find files mentioning 'Python'",
    ]

    print("--- Starting LLM File Assistant ---")
    while True:
        user_input = input("\nEnter your query (or 'exit' to quit): ")
        if user_input.lower() in ['exit', 'quit']:
            print("Exiting Resume Assistant. Goodbye!")
            quit()
            break
        elif KeyboardInterrupt:
            print("Exiting Resume Assistant. Goodbye!")
            quit()
        result = assistant.process_query(user_input)
        print(f"\nAssistant: {result}")
