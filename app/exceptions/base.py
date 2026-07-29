

class AppError(Exception):
    """Base exception for all domain-level errors."""
    pass 


class NotFoundError(AppError):
    """Entity not found."""
    pass 


class ConflictError(AppError):
    """Conflict with existing data (duplicated, etc)."""
    pass 


class ValidationError(AppError):
    """Bussiness rule validation failed."""
    pass 