from save_to_db.exceptions.item_cls_collection import CollectionDoesNotExist


class ItemClsCollection(object):
    """ Class for managing collections of
    :py:class:`~save_to_db.core.item_base.ItemBase` sub-classes.
    
    :cvar collection:
        Set of all item classes in the collection.
    """
    collection_classes = {}
    
    def __init__(self, collection_id):
        self.collection = set()
        self.collection_id = collection_id
        self.collection_classes[collection_id] = self
    
    def add(self, *item_classes):
        """ Adds item classes to the collection.
        
        :param \*item_classes: List of item classes to add.
        """
        self.collection.update(item_classes)
    
    def remove(self, *item_classes):
        """ Removes item classes from the collection.
        
        :param \*item_classes: List of item classes to remove.
        """
        self.collection -= set(item_classes)
    
    def clear(self):
        """ Removes all item classes from the collection. """
        self.collection.clear()
    
    def get_all_item_classes(self):
        """ Returns all item classes in the collection.
        
        :returns: All item classes in the collection.
        """
        return self.collection
    
    #--- managing collections --------------------------------------------------
    
    @classmethod
    def get_collection_by_id(cls, collection_id):
        """ Returns item collection with the given id.
        
        :param collection_id: Item class collection ID.
        :returns: Item class collection instance with the given ID.
        """
        if collection_id not in cls.collection_classes:
            raise CollectionDoesNotExist(collection_id)
        return cls.collection_classes[collection_id]
