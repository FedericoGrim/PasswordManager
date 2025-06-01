class CreateSubaccountException(Exception):
    def __init__(self, message: str):
        super().__init__(message)

class SubaccountRetrievalException(Exception):
    def __init__(self, message: str):
        super().__init__(message)

class SubaccountUpdateException(Exception):
    def __init__(self, message: str):
        super().__init__(message)

class SubaccountDeletionException(Exception):
    def __init__(self, message: str):
        super().__init__(message)