class NotDataStringException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message
        
class PingPongException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message
        
class EncryptionMessageException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

