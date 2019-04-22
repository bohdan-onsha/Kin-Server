class InvalidEmailError(Exception):
    def __init__(self):
        message = "Email are invalid or doesn't exist"

        super().__init__(message)


class InvalidPasswordError(Exception):
    def __init__(self):
        message = "Password is invalid\n" \
                  "Make sure these requirements are satisfied:\n" \
                  " - At least 8 characters\n" \
                  " - Consists of letters (upper/lowercase), numbers and/or any of the special characters: @#$%^&+=\n"

        super().__init__(message)


class AccountNotFoundError(Exception):
    def __init__(self):
        message = "Account with that uid does not exists"

        super().__init__(message)
