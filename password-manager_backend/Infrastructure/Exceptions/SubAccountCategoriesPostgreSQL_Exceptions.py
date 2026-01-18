class SubAccauntCategoryAlreadyExistsException(Exception):
    def __init__(self, message="SubAccauntCategory with the same subaccount and category already exists."):
        self.message = message
        super().__init__(self.message)

class SubAccauntCategoryCreationFailedException(Exception):
    def __init__(self, message="Failed to create subacc category."):
        self.message = message
        super().__init__(self.message)

class GetAllCategoriesBySubAccountIdNotFoundException(Exception):
    def __init__(self, message="No categories found for the given subaccount ID."):
        self.message = message
        super().__init__(self.message) 

class SubAccauntCategoryRetrievalException(Exception):
    def __init__(self, message="Failed to retrieve subacc categories."):
        self.message = message
        super().__init__(self.message)

class SubAccauntCategoryNotFoundException(Exception):
    def __init__(self, message="SubAccauntCategory not found."):
        self.message = message
        super().__init__(self.message)

class SubAccauntCategoryUpdateFailedException(Exception):
    def __init__(self, message="Failed to update subacc category."):
        self.message = message
        super().__init__(self.message)

class SubAccauntCategoryDeletionFailedException(Exception):
    def __init__(self, message="Failed to delete subacc category."):
        self.message = message
        super().__init__(self.message)