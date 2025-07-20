class LocalUserCreationException(Exception):
    """
    Exception raised when there is an error creating a local user.
    """
    def __init__(self, message="Error creating local user."):
        self.message = message
        super().__init__(self.message)

class LocalUserRetrievalException(Exception):
    """
    Exception raised when there is an error retrieving a local user.
    """
    def __init__(self, message="Error retrieving local user."):
        self.message = message
        super().__init__(self.message)

class LocalUserUpdateException(Exception):
    """
    Exception raised when there is an error updating a local user.
    """
    def __init__(self, message="Error updating local user."):
        self.message = message
        super().__init__(self.message)

class LocalUserDeletionException(Exception):
    """
    Exception raised when there is an error deleting a local user.
    """
    def __init__(self, message="Error deleting local user."):
        self.message = message
        super().__init__(self.message)