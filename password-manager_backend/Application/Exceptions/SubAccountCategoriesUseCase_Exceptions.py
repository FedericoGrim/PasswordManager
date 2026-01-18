class CreateSubAccountCategoryException(Exception):
    def __init__(self, message="Failed to create subacc category."):
        self.message = message
        super().__init__(self.message)

class SubAccountCategoryRetrievalException(Exception):
    def __init__(self, message="Failed to retrieve subacc categories."):
        self.message = message
        super().__init__(self.message)

class SubAccountCategoryUpdateException(Exception):
    def __init__(self, message="Failed to update subacc category."):
        self.message = message
        super().__init__(self.message)

class SubAccountCategoryDeletionException(Exception):
    def __init__(self, message="Failed to delete subacc category."):
        self.message = message
        super().__init__(self.message)

