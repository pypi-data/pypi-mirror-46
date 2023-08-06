import copy
from inspect import isclass
from save_to_db.exceptions.scope_except import (ItemClsAlreadyScoped,
                                                ScopeIdCannotBeNone)
from save_to_db.exceptions.item_cls_collection import CollectionIdAlreadyInUse
from .item_base import ItemBase
from .item_cls_manager import item_cls_manager
from .utils.item_cls_collection import ItemClsCollection


class Scope(ItemClsCollection):
    """ Class for scoping :py:class:`~.item.Item` classes.
    
    :param fixes: a dictionary whose keys are item classes (or `None`
        for all classes not in the dictionary) and values are class
        attributes to be replaced.
    :param collection_id: Scope ID, can be value of any type.
    
        .. seealso::
            :py:meth:`~.item_base.ItemBase.get_collection_id` method of
            :py:class:`~.item_base.ItemBase` class.
    
    Example usage:
        
        .. code:: Python
        
            class TestItem(Item):
                model_cls = SomeModel
            
            scope = Scope({
                TestItem: {
                    'conversions': {
                        'date_formats': '%m/%d/%Y',
                    },
                },
                # for item classes not listed
                None: {
                    'conversions': {
                        'date_formats': '%d.%m.%Y',
                    },
                },
                # for all item classes
                True: 'conversions': {
                    'datetime_formats': '%Y-%m-%d %H:%M:%S.%f',
                }, 
            })
            
            ScopedTestItem = scope[TestItem]  # or `scope.get(TestItem)`
    
    When an item is scoped other items that use the original item in
    relations are also scoped and their relation data fixed.
    """
    
    def __init__(self, fixes, collection_id):
        if collection_id is None:
            raise ScopeIdCannotBeNone()
        if collection_id in Scope.collection_classes:
            raise CollectionIdAlreadyInUse(collection_id)
        super().__init__(collection_id=collection_id)
        
        self.none_cls_fixes = {}
        self._classes = {}
        item_cls_manager.autocomplete_item_classes()
        
        # injecting from `True`
        if True in fixes:
            for item_cls, item_fixes in fixes.items():
                if item_cls is True:
                    continue
                item_fixes = self.__merge_fixes(item_fixes, fixes[True])
                
            if None not in fixes:
                fixes[None] = fixes[True]
        
        # fixing classes
        for item_cls, item_fixes in fixes.items():
            if item_cls is None or item_cls is True:
                continue
            self.__prepare_scoped_item_cls(item_cls, item_fixes)
        
        # `None` class
        if None in fixes:
            self.none_cls_fixes = copy.deepcopy(fixes[None])
            for item_cls in item_cls_manager.get_all_item_classes():
                if item_cls in self._classes:
                    continue
                self.__prepare_scoped_item_cls(item_cls, fixes[None])
        
        self.__fix_relations()
        
    
    def __fix_relations(self, item_fixes=None):
        if item_fixes is None:
            item_fixes = {}
        # fixing relations
        do_continue = True
        while do_continue:
            do_continue = False
            #--- first scoping items that need to be scoped ---
            for item_cls in item_cls_manager.get_all_item_classes():
                if item_cls in self._classes:
                    continue
                
                item_cls.complete_setup()
                for rel_data in item_cls.relations.values():
                    if rel_data['item_cls'] in self._classes:
                        self.__prepare_scoped_item_cls(item_cls,
                                                       item_fixes=item_fixes)
                        break
            
            #--- updating relations if needed ---
            for scoped_item_cls in self._classes.values():
                relations = scoped_item_cls.relations
                for key, rel_data in relations.items():
                    rel_item_cls = rel_data['item_cls']
                    if rel_item_cls not in self._classes:
                        continue
                    
                    relations[key]['item_cls'] = self._classes[rel_item_cls]
                    do_continue = True
    
    
    def __merge_fixes(self, extened, merged):
        merged_is_item = isclass(merged) and issubclass(merged, ItemBase)
        if merged_is_item:
            keys = list(extened.keys())
        else:
            keys = list(merged.keys())
        
        for key in keys:
            if merged_is_item:
                merging_value = getattr(merged, key)
            else:
                merging_value = merged[key]
            merging_value = copy.deepcopy(merging_value)
            
            if key not in extened:
                extened[key] = merging_value
                continue
            
            if key in ['defaults', 'conversions']:
                merging_value.update(extened[key])
                extened[key] = merging_value 

        return extened
        
    
    def __prepare_scoped_item_cls(self, item_cls, item_fixes):
        if item_cls.metadata['collection_id'] != None:
            raise ItemClsAlreadyScoped(item_cls)

        item_cls.complete_setup()
        item_fixes = copy.deepcopy(item_fixes)
        item_fixes['relations'] = copy.deepcopy(item_cls.relations)
        item_fixes['metadata'] = {}
        for key, value in item_cls.metadata.items():
            if key not in ('collection_id', 'model_deleter', 'model_unrefs',
                           'setup_completed'):
                item_fixes['metadata'][key] = value
        item_fixes['metadata']['collection_id'] = self.collection_id
        
        class_name = item_cls.__name__
        scoped_item_cls = type('Scoped{}'.format(class_name), (item_cls,),
                               self.__merge_fixes(item_fixes, item_cls))
        self._classes[item_cls] = scoped_item_cls
        super().add(scoped_item_cls)
    
    
    def __getitem__(self, item_cls):
        if item_cls not in self._classes:
            item_cls.complete_setup()
            item_cls_manager.autocomplete_item_classes()
            self.__prepare_scoped_item_cls(item_cls, self.none_cls_fixes)
            self.__fix_relations(self.none_cls_fixes)
        return self._classes[item_cls]
    
    
    def get(self, *item_classes):
        """ Excepts non-scoped items and returns corresponding scoped items or
        original items for items not present in the scope.
        
        :param item_classes: Items for which scoped item versions going to be
            returned.
        :returns: List of scoped items. If scope does not have corresponding
            scoped version of an item class, original class is used.
        """
        return [self[item_cls] for item_cls in item_classes]
    
    #--- managing scopes -------------------------------------------------------
    
    @classmethod
    def delete_all_scopes(cls):
        """ Removes all scopes. """
        for key in list(cls.collection_classes.keys()):
            if key is not None:
                del cls.collection_classes[key]
