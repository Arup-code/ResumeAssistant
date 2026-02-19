from importlib.metadata import metadata
from pathlib import Path

def readFile(path: str) -> dict:
    with open(path, 'r') as f:
        data: str = f.read()
        metadata = Path(path).stat()
        filedata: dict[str,str] = {
            'data': data,
            "metadata": {
                "owner" : metadata.st_uid,
                "group": metadata.st_gid,
                "permissions": metadata.st_mode,
                "size": metadata.st_size,
                "last_accessed": metadata.st_atime,
                "last_modified": metadata.st_mtime,
                "created": metadata.st_ctime,
                "file_attributes":metadata.st_file_attributes,
            }
        }
    return fileData