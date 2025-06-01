class PostgreSqlConnectionException(Exception):
    def __init__(self, message="PostgreSQL connection error occurred"):
        self.message = message
        super().__init__(self.message)

class PostgreSqlException(Exception):
    def __init__(self, message="PostgreSQL error occurred"):
        self.message = message
        super().__init__(self.message)

class SubAccountAlreadyExistsException(Exception):
    def __init__(self, message="SubAccount already exists"):
        self.message = message
        super().__init__(self.message)

class SubAccountCreationFailedException(Exception):
    def __init__(self, message="SubAccount creation failed"):
        self.message = message
        super().__init__(self.message)

class GetAllSubAccountsByUserIdNotFoundException(Exception):
    def __init__(self, message="No subaccounts found for the given user ID"):
        self.message = message
        super().__init__(self.message)

class SubAccountNotFoundException(Exception):
    def __init__(self, message="SubAccount not found"):
        self.message = message
        super().__init__(self.message)

class SubAccountUpdateException(Exception):
    def __init__(self, message="Error updating subaccount"):
        self.message = message
        super().__init__(self.message)

class SubAccountDeletionException(Exception):
    def __init__(self, message="Error deleting subaccount"):
        self.message = message
        super().__init__(self.message)

class SubAccountRetrievalException(Exception):
    def __init__(self, message="Error retrieving subaccounts"):
        self.message = message
        super().__init__(self.message)