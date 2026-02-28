from src.model.llm_file_assistant import LLMFileAssistant
import sys

def main():
    print("Welcome to Resume Assistant (LLM Powered)")
    print("Type 'exit' or 'quit' to stop.")

    assistant = LLMFileAssistant()

    while True:
        try:
            query = input("\nUser: ")
            if query.lower() in ('exit', 'quit'):
                print("Exiting Resume Assistant. Goodbye!")
                quit()
                break

            response = assistant.process_query(query)
            print(f"Assistant: {response}")

        except KeyboardInterrupt:
            print("Exiting Resume Assistant. Goodbye!")
            quit()
        except Exception as e:
            print(f"Error: {e}")
            quit()

if __name__ == "__main__":
    main()

