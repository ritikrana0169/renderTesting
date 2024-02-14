from flask import jsonify

class EventException(Exception):
    def __init__(self, message="", status_code=400):
        self.message = message
        self.status_code = status_code
        super().__init__()

    def to_response(self):
        return jsonify(message=self.message), self.status_code


class UserException(Exception):
    def __init__(self, message="", status_code=400):
        self.message = message
        self.status_code = status_code
        super().__init__()

    def to_response(self):
        return jsonify(message=self.message), self.status_code
    
class OrganizationException(Exception):
    def __init__(self, message="", status_code=400):
        self.message = message
        self.status_code = status_code
        super().__init__()

    def to_response(self):
        return jsonify(message=self.message), self.status_code

class EmailException(Exception):
    def __init__(self, message="", status_code=400):
        self.message = message
        self.status_code = status_code
        super().__init__()

    def to_response(self):
        return jsonify(message=self.message), self.status_code
    
class PhoneException(Exception):
    def __init__(self, message="", status_code=400):
        self.message = message
        self.status_code = status_code
        super().__init__()

    def to_response(self):
        return jsonify(message=self.message), self.status_code
    
class GenericException(Exception):
    def __init__(self, message="Internal Server Error.", status_code=500):
        self.message = message
        self.status_code = status_code
        super().__init__()

    def to_response(self):
        return jsonify(message=self.message), self.status_code
