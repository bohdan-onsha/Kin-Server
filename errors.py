class InvalidEmailError(Exception):
    def __init__(self):
        message = "Email are invalid or doesn't exist"

        super().__init__(message)


class InvalidPasswordError(Exception):
    def __init__(self):
        message = "Password is too short (less than 8 characters)"

        super().__init__(message)


class ItemNotFoundError(Exception):
    def __init__(self):
        message = "There is no such items in database"

        super().__init__(message)


class InsufficientFundsError(Exception):
    def __init__(self):
        message = "Insufficient funds on server wallet to complete the transaction"

        super().__init__(message)


class ExcessLimitError(Exception):
    def __init__(self):
        message = "Wallet operations limit exceeded"

        super().__init__(message)


class InvalidTokenError(Exception):
    def __init__(self):
        message = "Provided token is invalid"

        super().__init__(message)
