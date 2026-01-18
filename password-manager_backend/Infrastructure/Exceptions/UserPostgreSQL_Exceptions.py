class UserAlreadyExistsException(Exception):
    def __init__(self, message="User already exists"):
        self.message = message
        super().__init__(self.message)
        
class UserCreationFailedException(Exception):
    def __init__(self, message="User creation failed"):
        self.message = message
        super().__init__(self.message)


class GetAllUserByIdRetrivalException(Exception):
    def __init__(self, message="Error retrieving local users by ID"):
        self.message = message
        super().__init__(self.message)

class GetAllUserByIdNotFoundException(Exception):
    def __init__(self, message="No local users found for the given main user ID"):
        self.message = message
        super().__init__(self.message)


class UserNotFoundException(Exception):
    def __init__(self, message="Local user not found"):
        self.message = message
        super().__init__(self.message)

class UserUpdatePasswordException(Exception):
    def __init__(self, message="Error updating local user password"):
        self.message = message
        super().__init__(self.message)


class UserDeleteException(Exception):
    def __init__(self, message="Error deleting local user"):
        self.message = message
        super().__init__(self.message)