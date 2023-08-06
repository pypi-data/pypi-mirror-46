""" This module contains exceptions for
:py:class:`~save_to_db.adapters.adapter_base.AdapterBase` class.
"""

class AdapterException(Exception):
    """ General exception for
    :py:class:`~save_to_db.adapters.adapter_base.AdapterBase` class.
    """


class CannotMergeModels(AdapterException):
    """ Raised when merging two or more ORM models into one is impossible. """


class MergeModelsNotAllowed(AdapterException):
    """ Raised when merging ORM models is forbidden. """