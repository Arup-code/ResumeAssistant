from pathlib import Path
from pypdf import PdfReader
from docx import Document
from src.utils.helpers import get_file_metadata
import os

from constants import ROOT_DIR, DATA_DIR, OUTPUT_DIR


def _resolve_path(raw: str) -> str:
    """
    Translate virtual or relative paths to absolute paths.

    Rules (applied in order):
    1. Paths starting with /data/ or data/ → mapped to DATA_DIR
    2. Paths starting with /output/ or output/ → mapped to OUTPUT_DIR
    3. Already-absolute paths → returned as-is
    4. Any other relative path → joined with ROOT_DIR
    """
    p = raw.replace("\\", "/").strip()

    # Strip leading slash for comparison
    p_lower = p.lstrip("/").lower()

    if p_lower.startswith("data/") or p_lower == "data":
        relative_part = p.lstrip("/")[len("data"):].lstrip("/")
        return os.path.join(DATA_DIR, relative_part) if relative_part else DATA_DIR

    if p_lower.startswith("output/") or p_lower == "output":
        relative_part = p.lstrip("/")[len("output"):].lstrip("/")
        return os.path.join(OUTPUT_DIR, relative_part) if relative_part else OUTPUT_DIR

    # Already absolute (Windows or Unix style)
    if os.path.isabs(raw):
        return raw

    # Relative path — anchor to project root
    return os.path.join(ROOT_DIR, raw)


def read_file(filepath: str) -> dict:
    """
    Read resume files (PDF, TXT, DOCX) and extract text content.
    Returns structured response with content and metadata.
    Supports virtual paths like /data/<filename> and /output/<filename>.
    """
    try:
        filepath = _resolve_path(filepath)
        path = Path(filepath)
        if not path.exists():
            return {"error": f"File not found: {filepath}"}

        content = ""
        extension = path.suffix.lower()

        if extension == '.pdf':
            reader = PdfReader(filepath)
            for page in reader.pages:
                content += page.extract_text() + "\n"
        elif extension == '.docx':
            doc = Document(filepath)
            for para in doc.paragraphs:
                content += para.text + "\n"
        elif extension == '.txt':
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        else:
            return {"error": f"Unsupported file extension: {extension}"}

        metadata = get_file_metadata(filepath)
        return {
            "content": content.strip(),
            "metadata": metadata,
            "filepath": filepath
        }
    except Exception as e:
        return {"error": f"Error reading file: {str(e)}"}


def list_files(directory: str, extension: str = None) -> list:
    """
    List all files in a directory.
    Filter by extension (e.g., .pdf, .txt).
    Return file metadata (name, size, modified date).
    Supports virtual paths like /data/ and /output/.
    """
    try:
        directory = _resolve_path(directory)
        path = Path(directory)
        if not path.exists() or not path.is_dir():
            return [{"error": f"Directory not found: {directory}"}] # Returning list to match return type hint, though maybe exception is better. Sticking to list.

        files_list = []
        for file in path.glob('*'):
            if file.is_file():
                if extension:
                    if not extension.startswith('.'):
                        ext_check = '.' + extension
                    else:
                        ext_check = extension
                    if file.suffix.lower() != ext_check.lower():
                        continue

                try:
                    metadata = get_file_metadata(str(file))
                    # Enhance metadata with name and path as requested
                    file_info = {
                         "name": file.name,
                         "path": str(file),
                         "size": metadata.get("metadata", {}).get("size"),
                         "modified": metadata.get("metadata", {}).get("last_modified")
                    }
                    files_list.append(file_info)
                except Exception as e:
                    continue # Skip files we can't read metadata for
        return files_list

    except Exception as e:
         return [{"error": f"Error listing files: {str(e)}"}]


def write_file(filepath: str, content: str) -> dict:
    """
    Write content to file.
    Create directories if needed.
    Return success/failure status.
    Supports virtual paths like /output/<filename>.
    """
    try:
        filepath = _resolve_path(filepath)
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        return {"status": "success", "filepath": filepath, "message": "File written successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def search_in_file(filepath: str, keyword: str) -> dict:
    """
    Search for keywords in file content.
    Return matches with context (surrounding text).
    Case-insensitive search.
    """
    try:
        # Reuse read_file to get content
        read_result = read_file(filepath)
        if "error" in read_result:
            return read_result # Propagate error

        content = read_result.get("content", "")
        matches = []
        content_lower = content.lower()
        keyword_lower = keyword.lower()

        if not keyword_lower:
             return {"filepath": filepath, "matches_count": 0, "matches": []}

        start_index = 0
        while True:
            idx = content_lower.find(keyword_lower, start_index)
            if idx == -1:
                break

            # Extract context (e.g., 50 chars before and after)
            context_start = max(0, idx - 50)
            context_end = min(len(content), idx + len(keyword) + 50)
            context = content[context_start:context_end].replace('\n', ' ')

            matches.append({
                "match": content[idx:idx+len(keyword)],
                "context": f"...{context}...",
                "index": idx
            })

            start_index = idx + 1 # Move past this match

        return {
            "filepath": filepath,
            "matches_count": len(matches),
            "matches": matches
        }

    except Exception as e:
        return {"error": f"Error searching in file: {str(e)}"}
