class SubAccountAlreadyExistsException(Exception):
    """
    Exception raised when a subaccount already exists in the database.
    This exception is typically raised when trying to create a subaccount with a name that already exists in the database. It can be used to handle conflicts during subaccount creation.
    It can also be used to indicate that a subaccount with the same user ID and title already exists, preventing duplicate entries.
    This can include errors related to unique constraints or primary key violations.

    Args:
        message (str): Explanation of the error. Defaults to "SubAccount already exists".
    """
    def __init__(self, message="SubAccount already exists"):
        self.message = message
        super().__init__(self.message)

class SubAccountCreationFailedException(Exception):
    """
    Exception raised when the creation of a subaccount fails.
    This exception is typically raised when there is an error during the creation process of a subaccount in the database.
    It can be used to handle errors that occur during the creation of a subaccount, such as database errors or validation failures.
    This can include errors related to missing required fields, invalid data formats, or other issues that prevent successful creation.
    
    Args:
        message (str): Explanation of the error. Defaults to "SubAccount creation failed".
    """
    def __init__(self, message="SubAccount creation failed"):
        self.message = message
        super().__init__(self.message)

class GetAllSubAccountsByUserIdNotFoundException(Exception):
    """
    Exception raised when no subaccounts are found for a given user ID.
    This exception is typically raised when the retrieval process does not find any subaccounts associated with the specified user ID. It can be used to handle cases where a user tries to access subaccounts that do not exist.
    It can also be used to indicate that the user ID provided does not have any associated subaccounts, preventing further operations on non-existent data.
    This can include errors related to empty result sets or missing associations.
    
    Args:
        message (str): Explanation of the error. Defaults to "No subaccounts found for the given user ID".
    """
    def __init__(self, message="No subaccounts found for the given user ID"):
        self.message = message
        super().__init__(self.message)

class SubAccountNotFoundException(Exception):
    """
    Exception raised when a subaccount is not found in the database.
    This exception is typically raised when trying to retrieve or update a subaccount that does not exist in the database.
    It can be used to handle cases where a user tries to access a subaccount that has been deleted or never existed.
    It can also be used to indicate that the subaccount ID provided does not correspond to any existing subaccount, preventing further operations on non-existent data.

    Args:
        message (str): Explanation of the error. Defaults to "SubAccount not found".
    """
    def __init__(self, message="SubAccount not found"):
        self.message = message
        super().__init__(self.message)

class SubAccountUpdateException(Exception):
    """
    Exception raised when there is an error updating a subaccount.
    This exception is typically raised when the update process encounters an issue, such as a database error or a failure to find the subaccount.
    It can be used to handle cases where a user tries to update a subaccount that does not exist or when the update operation fails due to validation errors or other issues.
    
    Args:
        message (str): Explanation of the error. Defaults to "Error updating subaccount".
    """
    def __init__(self, message="Error updating subaccount"):
        self.message = message
        super().__init__(self.message)

class SubAccountDeletionException(Exception):
    """
    Exception raised when there is an error deleting a subaccount.
    This exception is typically raised when the deletion process encounters an issue, such as a database error or a failure to find the subaccount.
    It can be used to handle cases where a user tries to delete a subaccount that does not exist or when the deletion operation fails due to constraints or other issues.

    Args:
        message (str): Explanation of the error. Defaults to "Error deleting subaccount".
    """
    def __init__(self, message="Error deleting subaccount"):
        self.message = message
        super().__init__(self.message)

class SubAccountRetrievalException(Exception):
    """
    Exception raised when there is an error retrieving subaccounts.
    This exception is typically raised when the retrieval process encounters an issue, such as a database error or a failure to find any subaccounts.
    It can be used to handle cases where a user tries to access subaccounts but the retrieval operation fails due to validation errors, connection issues, or other problems.

    Args:
        message (str): Explanation of the error. Defaults to "Error retrieving subaccounts".
    """
    def __init__(self, message="Error retrieving subaccounts"):
        self.message = message
        super().__init__(self.message)
