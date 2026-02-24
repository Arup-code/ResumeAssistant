from pathlib import Path

def get_file_metadata(filepath: str) -> dict | None:
    try:
        metadata = Path(filepath).stat()
        return {
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
    except Exception as e:
        print(f"Error getting file metadata: {e}")


