class PostgreSqlConnectionException(Exception):
    def __init__(self, message="PostgreSQL connection error occurred"):
        self.message = message
        super().__init__(self.message)

class PostgreSqlException(Exception):
    def __init__(self, message="PostgreSQL error occurred"):
        self.message = message
        super().__init__(self.message)

class SubaccountAlreadyExistsException(Exception):
    def __init__(self, message="Subaccount already exists"):
        self.message = message
        super().__init__(self.message)

class SubaccountCreationFailedException(Exception):
    def __init__(self, message="Subaccount creation failed"):
        self.message = message
        super().__init__(self.message)

class GetAllSubAccountsByUserIdNotFoundException(Exception):
    def __init__(self, message="No subaccounts found for the given user ID"):
        self.message = message
        super().__init__(self.message)

class SubaccountNotFoundException(Exception):
    def __init__(self, message="Subaccount not found"):
        self.message = message
        super().__init__(self.message)

class SubaccountUpdateException(Exception):
    def __init__(self, message="Error updating subaccount"):
        self.message = message
        super().__init__(self.message)

class SubaccountDeletionException(Exception):
    def __init__(self, message="Error deleting subaccount"):
        self.message = message
        super().__init__(self.message)

class SubaccountRetrievalException(Exception):
    def __init__(self, message="Error retrieving subaccounts"):
        self.message = message
        super().__init__(self.message)