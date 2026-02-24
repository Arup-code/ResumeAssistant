import os
from google import genai
from google.genai import types
from src.service.fs_tools import read_file, list_files, write_file, search_in_file

# Check for API key
if not os.environ.get("GOOGLE_API_KEY"):
    print("Warning: GOOGLE_API_KEY environment variable not found. Please set it before running.")

class LLMFileAssistant:
    def __init__(self):
        self.client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))
        self.model_name = "gemini-2.0-flash"
        self.tools = [read_file, list_files, write_file, search_in_file]
        self.chat = self.client.chats.create(
            model=self.model_name,
            config=types.GenerateContentConfig(
                tools=self.tools,
                automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=False)
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
            return f"Error processing query: {str(e)}"

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
            break

        result = assistant.process_query(user_input)
        print(f"\nAssistant: {result}")
