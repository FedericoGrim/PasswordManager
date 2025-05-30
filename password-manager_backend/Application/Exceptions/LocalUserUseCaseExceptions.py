class LocalUserCreationException(Exception):
    def __init__(self, message="Error creating local user."):
        self.message = message
        super().__init__(self.message)

class LocalUserRetrievalException(Exception):
    def __init__(self, message="Error retrieving local user."):
        self.message = message
        super().__init__(self.message)

class LocalUserUpdateException(Exception):
    def __init__(self, message="Error updating local user."):
        self.message = message
        super().__init__(self.message)

class LocalUserDeletionException(Exception):
    def __init__(self, message="Error deleting local user."):
        self.message = message
        super().__init__(self.message)