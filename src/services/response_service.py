"""Global Response Service To Handle Response

This Service Used to Handle Response Structure
and Create, Update and Send It Into JSON Format
"""

from typing_extensions import Self
from ..meta_classes.singleton import Singleton


class ResponseService(metaclass=Singleton):
    '''
    This Service Use to Standardize Our API Response
    '''

    def __init__(self) -> None:
        self.status = "success"
        self.status_code = 200
        self.status_message = "Request Success"
        self.data = {}
        self.message = ""

    def add_message(self, message: str) -> Self:
        '''
        Add Message String in the Response Payload
        '''
        self.message = message
        return self

    def add_status(self, status: str) -> Self:
        '''
        Add Status String in the response Payload
        '''
        self.status = status
        return self

    def add_status_code(self, status_code: int) -> Self:
        '''
        Add Status Code String in the response Payload
        '''
        self.status_code = status_code
        return self

    def add_data(self, data: dict) -> Self:
        '''
        Add Status String in the response Payload
        '''
        self.data = data
        return self

    def send_response(self) -> dict:
        '''
        Send The Final Response Payload
        '''
        return {
            "status_code": self.status_code,
            "status_message": self.status_message,
            "status": self.status,
            "data": self.data,
            "message": self.message
        }


response = ResponseService()
