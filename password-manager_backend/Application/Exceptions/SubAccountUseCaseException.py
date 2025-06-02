class CreateSubAccountException(Exception):
    def __init__(self, message: str):
        super().__init__(message)

class SubAccountRetrievalException(Exception):
    def __init__(self, message: str):
        super().__init__(message)

class SubAccountUpdateException(Exception):
    def __init__(self, message: str):
        super().__init__(message)

class SubAccountDeletionException(Exception):
    def __init__(self, message: str):
        super().__init__(message)
