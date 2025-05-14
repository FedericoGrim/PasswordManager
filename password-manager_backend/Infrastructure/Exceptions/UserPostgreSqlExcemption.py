class PostgreSqlConnectionException(Exception):
    def __init__(self, message="PostgreSQL connection error occurred"):
        self.message = message
        super().__init__(self.message)

class PostgreSqlException(Exception):
    def __init__(self, message="PostgreSQL error occurred"):
        self.message = message
        super().__init__(self.message)

class UserAlreadyExistsException(Exception):
    def __init__(self, message="User already exists"):
        self.message = message
        super().__init__(self.message)
        
class UserCreationFailedException(Exception):
    def __init__(self, message="User creation failed"):
        self.message = message
        super().__init__(self.message)

class UserRetrievalException(Exception):
    def __init__(self, message="Error during the retrieval of the user"):
        self.message = message
        super().__init__(self.message)

class UserUpdateException(Exception):
    def __init__(self, message="User update failed"):
        self.message = message
        super().__init__(self.message)

class UserNotFoundException(Exception):
    def __init__(self, message="User not found"):
        self.message = message
        super().__init__(self.message)

class UserDeletionException(Exception):
    def __init__(self, message="User deletion failed"):
        self.message = message
        super().__init__(self.message)
