class UserCreationException(Exception):
    def __init__(self, message="User creation failed."):
        self.message = message
        super().__init__(self.message)
        
class UserRetrievalException(Exception):
    def __init__(self, message="User retrieval failed."):
        self.message = message
        super().__init__(self.message)
        
class UserUpdateException(Exception):
    def __init__(self, message="User update failed."):
        self.message = message
        super().__init__(self.message)
        
class UserDeletionException(Exception):
    def __init__(self, message="User deletion failed."):
        self.message = message
        super().__init__(self.message)

class UserCreationException(Exception):
    def __init__(self, message="User creation failed."):
        self.message = message
        super().__init__(self.message)
        
class UserRetrievalException(Exception):
    def __init__(self, message="User retrieval failed."):
        self.message = message
        super().__init__(self.message)
        
class UserUpdateException(Exception):
    def __init__(self, message="User update failed."):
        self.message = message
        super().__init__(self.message)
        
class UserDeletionException(Exception):
    def __init__(self, message="User deletion failed."):
        self.message = message
        super().__init__(self.message)
