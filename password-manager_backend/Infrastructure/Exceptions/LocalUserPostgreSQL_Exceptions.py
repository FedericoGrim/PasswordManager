class PostgreSqlConnectionException(Exception):
    """
    Exception raised for errors in the PostgreSQL connection.
    This exception is typically raised when there is an issue connecting to the PostgreSQL database.
    It can be used to handle connection errors specifically in the context of PostgreSQL operations.

    Args:
        message (str): Explanation of the error. Defaults to "PostgreSQL connection error occurred".
    """
    def __init__(self, message="PostgreSQL connection error occurred"):
        self.message = message
        super().__init__(self.message)

class PostgreSqlException(Exception):
    """
    Exception raised for general PostgreSQL errors.
    This exception is typically raised when there is an error during PostgreSQL operations.

    Args:
        message (str): Explanation of the error. Defaults to "PostgreSQL error occurred".
    """
    def __init__(self, message="PostgreSQL error occurred"):
        self.message = message
        super().__init__(self.message)


class LocalUserAlreadyExistsException(Exception):
    """
    Exception raised when a local user already exists in the database.
    This exception is typically raised when trying to create a user with a Keycloak ID that already exists in the database.

    Args:
        message (str): Explanation of the error. Defaults to "LocalUser already exists".
    """
    def __init__(self, message="LocalUser already exists"):
        self.message = message
        super().__init__(self.message)
        
class LocalUserCreationFailedException(Exception):
    """
    Exception raised when the creation of a local user fails.
    This exception is typically raised when there is an error during the creation process of a local user in the database.

    Args:
        message (str): Explanation of the error. Defaults to "User creation failed".
    """
    def __init__(self, message="User creation failed"):
        self.message = message
        super().__init__(self.message)


class GetAllLocalUserByIdRetrivalException(Exception):
    """
    Exception raised when there is an error retrieving local users by their ID.
    This exception is typically raised when the retrieval process encounters an issue, such as a database error or a failure to find the user.

    Args:
        message (str): Explanation of the error. Defaults to "Error retrieving local users by ID
    """
    def __init__(self, message="Error retrieving local users by ID"):
        self.message = message
        super().__init__(self.message)

class GetAllLocalUserByIdNotFoundException(Exception):
    """
    Exception raised when no local users are found for a given main user ID.
    This exception is typically raised when the retrieval process does not find any local users associated with the specified main user ID.

    Args:
        message (str): Explanation of the error. Defaults to "No local users found for the given main user ID".
    """
    def __init__(self, message="No local users found for the given main user ID"):
        self.message = message
        super().__init__(self.message)


class LocalUserNotFoundException(Exception):
    """
    Exception raised when a local user is not found in the database.
    This exception is typically raised when trying to retrieve or update a user that does not exist in the database.

    Args:
        message (str): Explanation of the error. Defaults to "Local user not found".
    """
    def __init__(self, message="Local user not found"):
        self.message = message
        super().__init__(self.message)

class LocalUserUpdatePasswordException(Exception):
    """
    Exception raised when there is an error updating the password of a local user.
    This exception is typically raised when the update process encounters an issue, such as a database error or a failure to find the user.

    Args:
        message (str): Explanation of the error. Defaults to "Error updating local user password".
    """
    def __init__(self, message="Error updating local user password"):
        self.message = message
        super().__init__(self.message)


class LocalUserDeleteException(Exception):
    """
    Exception raised when there is an error deleting a local user.
    This exception is typically raised when the deletion process encounters an issue, such as a database error or a failure to find the user.

    Args:
        message (str): Explanation of the error. Defaults to "Error deleting local user".
    """
    def __init__(self, message="Error deleting local user"):
        self.message = message
        super().__init__(self.message)