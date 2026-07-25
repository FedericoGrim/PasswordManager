class UserTeamsKeysPostgreSQL_Exception(Exception):
    pass

class UserTeamsKeyAdditionException(UserTeamsKeysPostgreSQL_Exception):
    def __init__(self, message: str="Error adding user teams key"):
        self.message = message
        super().__init__(self.message)

class UserTeamsKeyRetrievalException(UserTeamsKeysPostgreSQL_Exception):
    def __init__(self, message: str="Error retrieving user teams keys"):
        self.message = message
        super().__init__(self.message)

class UserTeamsKeyUpdateException(UserTeamsKeysPostgreSQL_Exception):
    def __init__(self, message: str="Error updating user teams key"):
        self.message = message
        super().__init__(self.message)

class UserTeamsKeyRemovalException(UserTeamsKeysPostgreSQL_Exception):
    def __init__(self, message: str="Error removing user teams key"):
        self.message = message
        super().__init__(self.message)
