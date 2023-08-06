""" This module contains exceptions for
:py:class:`~save_to_db.core.merge_policy.MergePolicy` class.
"""

class MergePolicyException(Exception):
    """ General exception for
    :py:class:`~save_to_db.core.merge_policy.MergePolicy` class.
    """

class ModelClsAlreadyRegistered(MergePolicyException):
    """ Raised when trying to add ORM model class to a merge policu twice.
    """
    
class UnknownRelationFieldNames(MergePolicyException):
    """ Raised when trying to setup merge policy using unknown relation
    relationship field name.
    """

class UnknownModelDefaultKey(MergePolicyException):
    """ Raised when trying to set defaults for merge policy using unkown
    default key.
    """