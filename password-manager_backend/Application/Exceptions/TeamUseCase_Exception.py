class TeamCreationException(Exception):
    def __init__(self, message="Error creating team"):
        self.message = message
        super().__init__(self.message)

class TeamRetrievalByIdException(Exception):
    def __init__(self, message="Error retrieving team by ID"):
        self.message = message
        super().__init__(self.message)

class TeamsRetrievalByUserIdException(Exception):
    def __init__(self, message="Error retrieving teams by User ID"):
        self.message = message
        super().__init__(self.message)

class TeamUpdateException(Exception):
    def __init__(self, message="Error updating team"):
        self.message = message
        super().__init__(self.message)

class TeamDeleteException(Exception):
    def __init__(self, message="Error deleting team"):
        self.message = message
        super().__init__(self.message)

class TeamNotFoundException(Exception):
    def __init__(self, message="Team not found"):
        self.message = message
        super().__init__(self.message)

class TeamAlreadyExistsException(Exception):
    def __init__(self, message="Team already exists"):
        self.message = message
        super().__init__(self.message)