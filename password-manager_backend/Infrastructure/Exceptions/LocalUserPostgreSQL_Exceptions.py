class PostgreSqlConnectionException(Exception):
    def __init__(self, message="PostgreSQL connection error occurred"):
        self.message = message
        super().__init__(self.message)

class PostgreSqlException(Exception):
    def __init__(self, message="PostgreSQL error occurred"):
        self.message = message
        super().__init__(self.message)


class LocalUserAlreadyExistsException(Exception):
    def __init__(self, message="LocalUser already exists"):
        self.message = message
        super().__init__(self.message)
        
class LocalUserCreationFailedException(Exception):
    def __init__(self, message="User creation failed"):
        self.message = message
        super().__init__(self.message)


class GetAllLocalUserByIdRetrivalException(Exception):
    def __init__(self, message="Error retrieving local users by ID"):
        self.message = message
        super().__init__(self.message)

class GetAllLocalUserByIdNotFoundException(Exception):
    def __init__(self, message="No local users found for the given main user ID"):
        self.message = message
        super().__init__(self.message)


class LocalUserNotFoundException(Exception):
    def __init__(self, message="Local user not found"):
        self.message = message
        super().__init__(self.message)

class LocalUserUpdatePasswordException(Exception):
    def __init__(self, message="Error updating local user password"):
        self.message = message
        super().__init__(self.message)


class LocalUserDeleteException(Exception):
    def __init__(self, message="Error deleting local user"):
        self.message = message
        super().__init__(self.message)