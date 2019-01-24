from db import FileDB

if __name__ == "__main__":
    file_db = FileDB()
    file_db.load_db()
    file_db.commit()