# 📄 ResumeAssistant

An AI-powered resume analysis tool that uses **Google Gemini** as the LLM backbone combined with a custom file-system toolset to read, search, list, and summarize resumes stored locally.

---

## 🗂️ Project Structure

```
ResumeAssistant/
├── main.py                        # Application entry point (interactive CLI)
├── constants.py                   # Project-wide path constants (ROOT_DIR, DATA_DIR, OUTPUT_DIR)
├── requirements.txt               # Python dependencies
├── run_manual_tests.py            # Convenience script to run unit tests
├── data/                          # 📥 INPUT — place resume files here (.pdf, .docx, .txt)
├── output/                        # 📤 OUTPUT — generated summaries & reports land here
├── src/
│   ├── service/
│   │   └── fs_tools.py            # Core file-system tools (read, list, write, search)
│   ├── model/
│   │   ├── llm_file_assistant.py  # LLM integration layer (Google Gemini + tool calling)
│   │   └── PROMPT.md              # System prompt that governs the assistant's behaviour
│   └── utils/
│       └── helpers.py             # Utility helpers (file metadata extraction)
└── test/
    └── test_fs_tools.py           # Unit tests for fs_tools.py
```

---

## ✨ Features

| Feature | Description |
|---|---|
| **Multi-format Resume Reading** | Parses PDF, DOCX, and TXT resume files |
| **Directory Listing** | Lists files in any directory with optional extension filter |
| **File Writing** | Writes AI-generated summaries / reports to the `output/` folder |
| **Keyword Search** | Case-insensitive full-text keyword search with surrounding context |
| **LLM-Powered Chat** | Natural-language interface backed by Google Gemini with automatic function calling |
| **Smart Path Resolution** | Virtual paths like `/data/` and `/output/` are automatically resolved to correct absolute paths |
| **HR-Focused Prompting** | System prompt tuned for HR workflows: candidate search, skill matching, and resume summarisation |

---

## ⚙️ Prerequisites

- Python **3.10+**
- A **Google AI Studio API key** with access to the Gemini model

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone <repository-url>
cd ResumeAssistant
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

> **dependencies**: `google-genai`, `python-docx`, `pypdf`, `python-dotenv`

### 3. Configure Environment Variables

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_google_api_key_here
```

### 4. Add Resume Files

Drop your resume files (`.pdf`, `.docx`, or `.txt`) into the `data/` folder:

```
data/
├── john_doe.pdf
├── jane_smith.docx
└── robert_cooper.pdf
```

### 5. Run the Assistant

```bash
python main.py
```

You will be dropped into an interactive CLI session:

```
Welcome to Resume Assistant (LLM Powered)
Type 'exit' or 'quit' to stop.

User: List all resumes in the data folder
Assistant: ...

User: Find resumes mentioning Python experience
Assistant: ...

User: Create a summary file for robert_cooper.pdf
Assistant: ...
```

---

## 🛠️ File System Tools (`src/service/fs_tools.py`)

These tools are exposed directly to the LLM via Gemini's automatic function-calling feature.

### `read_file(filepath: str) → dict`
Reads a resume file and returns its full text content along with file metadata.

- **Supported formats:** `.pdf`, `.docx`, `.txt`
- **Supports virtual paths:** `data/filename.pdf`, `/data/filename.pdf`
- **Returns:** `{ "content": str, "metadata": dict, "filepath": str }` or `{ "error": str }`

### `list_files(directory: str, extension: str = None) → list`
Lists all files in a directory with optional extension filtering.

- **Example:** `list_files("data", ".pdf")`
- **Returns:** list of `{ "name", "path", "size", "modified" }` dicts

### `write_file(filepath: str, content: str) → dict`
Writes text content to a file, creating parent directories as needed.

- **Intended for writing to:** `output/`
- **Returns:** `{ "status": "success"|"error", "filepath": str, "message": str }`

### `search_in_file(filepath: str, keyword: str) → dict`
Performs a case-insensitive keyword search through a file's text content.

- **Returns:** `{ "keyword": str, "matches_count": int, "matches": [ { "match", "context", "line_number" } ] }`

---

## 🤖 LLM Integration (`src/model/llm_file_assistant.py`)

- **Model:** `gemini-2.5-flash` (Google Gemini)
- **Tool Calling:** All four `fs_tools` functions are registered as callable tools; Gemini invokes them automatically based on user intent.
- **Session Memory:** Uses a persistent chat session (`client.chats.create`) so the LLM retains context across the conversation.
- **System Prompt:** Loaded from `src/model/PROMPT.md` — enforces strict directory rules (`/data/` for input, `/output/` for output) and HR-focused output formatting.

### Path Resolution Logic

The `_resolve_path()` helper in `fs_tools.py` translates virtual/relative paths into absolute OS paths:

| Input path | Resolved to |
|---|---|
| `data/resume.pdf` | `<ROOT>/data/resume.pdf` |
| `/data/resume.pdf` | `<ROOT>/data/resume.pdf` |
| `output/summary.txt` | `<ROOT>/output/summary.txt` |
| `/output/summary.txt` | `<ROOT>/output/summary.txt` |
| Absolute path | Used as-is |
| Other relative path | Joined with `ROOT_DIR` |

---

## 🧪 Running Tests

### Unit Tests (automated)

```bash
python run_manual_tests.py
```

Or directly with `unittest`:

```bash
python -m unittest discover -s test -v
```

### What is Tested

| Test | Description |
|---|---|
| `test_read_file` | Reads a `.txt` file and validates content + metadata |
| `test_list_files` | Lists files with and without extension filter |
| `test_write_file` | Writes a file to a nested subdirectory |
| `test_search_in_file` | Searches for a keyword and validates match count |

---

## 💬 Example Queries

```
"List all files in the data folder"
"Read the resume robert_cooper.pdf"
"Find all resumes mentioning Python"
"Find resumes with machine learning experience"
"Create a summary for john_doe.pdf and save it to the output folder"
"Read all resumes and give me an overview"
```

---

## 📋 Constants (`constants.py`)

| Constant | Value |
|---|---|
| `ROOT_DIR` | Absolute path to the project root |
| `DATA_DIR` | `<ROOT_DIR>/data` |
| `OUTPUT_DIR` | `<ROOT_DIR>/output` |

---

## 📦 Dependencies

| Package | Purpose |
|---|---|
| `google-genai` | Google Gemini LLM client with tool-calling support |
| `pypdf` | PDF text extraction |
| `python-docx` | DOCX text extraction |
| `python-dotenv` | Loading `.env` API keys |

---

## 📝 License

This project is for educational purposes as part of the Airtribe curriculum.

