from pprint import pprint


class ModelDeleter(object):
    """ This class keeps track of new items and is able to find those items
    in database that are not new in order to delete or unrefrence them
    (from x-to-many relationships).
    
    :param model_cls: ORM model class used by items that instance of this class
        deals with.
    :param selector_fields: List of fields that are collected from items. The
        values are used later to pull models from database.
    :param keeper_fields: Similar to `selector_fields`. If  a model can be
        pulled from database using values from `keeper_fields`, then this model
        is ignored by this class. 
    """

    def __init__(self, model_cls, selector_fields, keeper_fields):
        self.model_cls = model_cls
        self.selector_fields = selector_fields
        self.keeper_fields = keeper_fields

        self.reset()
    
    def reset(self):
        """ Resets `selectors` and `keepers`. """
        self.selectors = []
        self.keepers = []
    
    def collect_model(self, model):
        """ Saves `selector_fields` from `model`.
        
        :param model: ORM Model to collect field values from.
        """
        filters = self.__collect_filters(model, self.selector_fields)
        if filters not in self.selectors:
            self.selectors.append(filters)
            
        filters = self.__collect_filters(model, self.keeper_fields)
        if filters not in self.keepers:
            self.keepers.append(filters)

    def __collect_filters(self, model, fields):
        filters = {}
        for field in fields:
            if not hasattr(model, field):
                filters[field] = None
            else:
                filters[field] = getattr(model, field)
        return filters
    
    def execute_delete(self, db_adapter):
        """ Deletes rows from database that can be selected (pulled from
        database) using values from `selectors` but excluding those that can
        be selected by `keepers`.
        
        :param db_adapter: Database adapter.
        """
        db_adapter.execute_delete(self.model_cls,
                                  self.selectors, self.keepers)
        self.reset()
    
    def execute_unref(self, parent_model, fkey, db_adapter):
        """ Removes x-to-many references in database from x-to-many
        relationship from `parent_model` to child model through `fkey`
        if refrenced models can be selected using `selectors` values,
        exluding those that can be selected by `keepers`.
        
        :param parent_model: Parent ORM model.
        :param fkey: Foreign key field of `parent_model`.
        :param db_adapter: Database adapter.
        """
        db_adapter.execute_unref(parent_model, fkey,
                                 self.selectors, self.keepers)
        self.reset()
    
    def pprint(self):
        """ Pretty-prints an instance data to console. """
        pprint({
            'selectors': self.selectors,
            'keepers': self.keepers,
            'selector_fields': self.selector_fields,
            'keeper_fields': self.keeper_fields,
        })
        
        