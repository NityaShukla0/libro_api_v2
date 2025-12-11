from fastapi import HTTPException

class BookNotAvailableException(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Book is not available")