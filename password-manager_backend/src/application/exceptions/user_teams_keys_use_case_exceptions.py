class UserTeamsKeyAdditionException(Exception):
    def __init__(self, message: str="Error adding user teams key"):
        self.message = message
        super().__init__(self.message)

class UserTeamsKeyRetrievalByIdException(Exception):
    def __init__(self, message: str="Error retrieving user teams key by ID"):
        self.message = message
        super().__init__(self.message)

class UserTeamsKeysRetrievalByTeamIdException(Exception):
    def __init__(self, message: str="Error retrieving user teams keys by Team ID"):
        self.message = message
        super().__init__(self.message)

class UserTeamsKeysRetrievalByUserIdException(Exception):
    def __init__(self, message: str="Error retrieving user teams keys by User ID"):
        self.message = message
        super().__init__(self.message)

class UserTeamsKeyUpdateException(Exception):
    def __init__(self, message: str="Error updating user teams key"):
        self.message = message
        super().__init__(self.message)

class UserTeamsKeyRemovalException(Exception):
    def __init__(self, message: str="Error removing user teams key"):
        self.message = message
        super().__init__(self.message)
