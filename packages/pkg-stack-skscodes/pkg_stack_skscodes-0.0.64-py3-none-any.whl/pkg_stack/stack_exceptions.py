class StackError(Exception):
    pass

class StackFullError(StackError):
    def __init__(self):
        super().__init__("stack is full.")

class StackEmptyError(StackError):
    def __init__(self):
        super().__init__("stack is empty.")