import os
import uuid

UPLOAD_DIR = "data/uploads/"

def save_file(file):
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # generate unique filename
    file_extension = file.filename.split(".")[-1]
    unique_name = f"{uuid.uuid4()}.{file_extension}"

    file_path = os.path.join(UPLOAD_DIR, unique_name)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    return file_path