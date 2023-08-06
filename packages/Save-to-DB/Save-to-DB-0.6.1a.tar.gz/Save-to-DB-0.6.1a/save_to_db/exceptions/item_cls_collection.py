""" This module contains exceptions for
:py:class:`~save_to_db.core.utils.item_cls_collection.ItemClsCollection` class.
"""

class ItemClsCollectionException(Exception):
    """ General exception for
    :py:class:`~save_to_db.core.utils.item_cls_collection.ItemClsCollection`
    class.
    """


class CollectionDoesNotExist(ItemClsCollectionException):
    """ Raised when trying to get collection that does not exist using
    `collection_id`.
    """

class CollectionIdAlreadyInUse(ItemClsCollectionException):
    """ Raised when trying to create new item class collection with 
    `collection_id` value already taken.
    """