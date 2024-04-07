class FileError(Exception):
    def __init__(self, msg):
        self.msg = msg
        super().__init__(self.msg)


class EmailInvalidError(Exception):
    def __init__(self, msg):
        self.msg = msg
        super().__init__(self.msg)


class PhoneInvalidError(Exception):
    def __init__(self, msg):
        self.msg = msg
        super().__init__(self.msg)
        

class ShowError(Exception):
    def __init__(self, msg):
        self.msg = msg
        super().__init__(self.msg)


class MovieError(Exception):
    def __init__(self, msg):
        self.msg = msg
        super().__init__(self.msg)


class ReservationError(Exception):
    def __init__(self, msg):
        self.msg = msg
        super().__init__(self.msg)


class CinemahallError(Exception):
    def __init__(self, msg):
        self.msg = msg
        super().__init__(self.msg)


class FeedbackError(Exception):
    def __init__(self, msg):
        self.msg = msg
        super().__init__(self.msg)
