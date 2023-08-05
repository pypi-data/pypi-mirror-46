from Homevee.Exception import AbstractFunctionCallException


class Condition():
    def __init__(self):
        return

    def is_true(self):
        raise AbstractFunctionCallException("Condition.is_true() is abstract")