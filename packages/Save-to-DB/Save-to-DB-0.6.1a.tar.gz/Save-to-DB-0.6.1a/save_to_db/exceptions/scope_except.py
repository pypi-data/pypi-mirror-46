""" This module contains exceptions for :py:class:`~save_to_db.core.scope.Scope`
class.
"""

class ScopeException(Exception):
    """ General exception for :py:class:`~save_to_db.core.scope.Scope` class.
    """


class ItemClsAlreadyScoped(ScopeException):
    """ Raised when an already scoped item is scoped again. """


class ScopeIdCannotBeNone(ScopeException):
    """ Raised when trying to set Scope `collection_id` to `None`. """