class ServiceDeskError(Exception):
    """Base class for every custom exception in this application."""
    pass

class DuplicateRequestError(ServiceDeskError):
    """Raised when a Request ID that already exists is created again."""
    pass

class RequestNotFoundError(ServiceDeskError):
    """Raised when a Request ID is searched/resolved but does not exist."""
    pass

class InvalidPriorityError(ServiceDeskError):
    """Raised when priority is not one of LOW, MEDIUM, HIGH."""
    pass

class AlreadyResolvedError(ServiceDeskError):
    """Raised when trying to resolve a request that is already RESOLVED."""
    pass