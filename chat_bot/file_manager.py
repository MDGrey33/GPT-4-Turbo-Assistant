class FileManager:
    def __init__(self, client):
        self.client = client.files

    def create(self, file_path, purpose):
        with open(file_path, 'rb') as file_object:
            response = self.client.create(file=file_object, purpose=purpose)
            return response.id

    def list(self):
        files_data = self.client.list().data
        return {file.id: {"filename": file.filename, "purpose": file.purpose} for file in files_data}

    def delete(self, file_id):
        self.client.delete(file_id)
        return f"File with ID {file_id} has been deleted."
