import pickle
import struct
from .item_cls_manager import item_cls_manager
from .merge_policy import MergePolicy
from .utils.item_cls_collection import ItemClsCollection



class Persister(object):
    """ This class is used to persist items to database or save and load them
    from files.
    
    :param db_adapter: Instance of a subclass of
        :py:class:`~save_to_db.adapters.utils.adapter_base.AdapterBase` used
        to deal with items and ORM models.
    :param autocommit: If `True` commits changes to database each time an
        item is persisted.
    """
    
    def __init__(self, db_adapter, autocommit=False):
        self.db_adapter = db_adapter
        self.autocommit = autocommit
    
    
    #--- database adapter facade -----------------------------------------------
    
    def persist(self, item, commit=None):
        """ Saves item data into a database by creating or update appropriate
        database records.
        
        :param item: an instance of :py:class:`~.item_base.ItemBase` to persist.
        :param commit: If `True` commits changes to database. If `None` then
            `autocommit` value (initially set at creation time) is used.
            
        :returns: Item list and corresponding list of ORM  model lists.
        """
        result = self.db_adapter.persist(item)
        self.__commit_if_needed(commit)
        return result
    
    
    def merge_models(self, models, commit=None,
                     merge_policy=None, ignore_fields=None):
        """ Calls
        :py:meth:`~save_to_db.adapters.utils.adapter_base.AdapterBase.merge_models`
        method of
        :py:class:`~save_to_db.adapters.utils.adapter_base.AdapterBase`
        internal instance.
        
        :param commit: If `True` commits changes to database. If `None` then
            `autocommit` value (initially set at creation time) is used.
        :returns: First model from `models` into which all other models merged.
        """
        result_model = self.db_adapter.merge_models(
            models, merge_policy=merge_policy, ignore_fields=ignore_fields)
        self.__commit_if_needed(commit)
        return result_model
    
        
    def __commit_if_needed(self, commit):
        try:
            if commit or (commit is None and self.autocommit):
                self.commit()
        except:
            if commit or (commit is None and self.autocommit):
                self.rollback()
            raise
        

    def commit(self):
        """ Commits persisted items to database. """
        self.db_adapter.commit()
        
    
    def rollback(self):
        """ Rolls back current transaction. """
        self.db_adapter.rollback()
        
    
    def pprint(self, *models):
        """ Pretty prints `model` to console.
        
        :param \*models: List of models to print.
        """
        self.db_adapter.pprint(*models)

    
    #--- interface for working with files --------------------------------------
    
    def dumps(self, item):
        """ Converts an item into bytes.
        
        :param item: An instance of :py:class:`~.item_base.ItemBase` class.
        :returns: Encoded item as `bytes`.
        """
        item.process()
        model_cls = item.model_cls
        return pickle.dumps({
            'table_fullname': self.db_adapter.get_table_fullname(model_cls),
            'is_bulk_item': item.is_bulk_item(),
            'dict_wrapper': item.to_dict(),
            'collection_id': item.get_collection_id(),
        })
    
    
    def loads(self, data):
        """ Decodes `bytes` data into an instance of
        :py:class:`~.item_base.ItemBase`.
        
        :param data: Encoded item as `bytes`.
        :returns: An instance of :py:class:`~.item_base.ItemBase`.
        """
        result_data = pickle.loads(data)
        
        model_cls = self.db_adapter.get_model_cls_by_table_fullname(
            result_data['table_fullname'])
        item_cls = item_cls_manager.get_by_model_cls(
            model_cls, collection_id=result_data['collection_id'])[0]
        
        item = item_cls.Bulk() if result_data['is_bulk_item'] else item_cls()
        item = item.load_dict(result_data['dict_wrapper'])
        
        return item
    
        
    def dump(self, item, fp):
        """ Saves an item into a file.
        
        .. note::
            This method also saves the size of encoded item. So it is possible
            to save multiple items one after another into the same file and
            load them later.
        
        :param item: An item to be saved.
        :param fp: File-like object to save `item` into.
        """
        item_data = self.dumps(item)
        fp.write(struct.pack('>I', len(item_data)))
        fp.write(item_data)
        
    
    def load(self, fp):
        """ Loads and decodes one item from a file-like object.
        
        :param fp: File-like object to read from.
        :return: One item read from `fp` or `None` if there are no data to read
            anymore.
        """
        int_as_bytes = fp.read(4)
        if not int_as_bytes:
            return None
        l = struct.unpack('>I', int_as_bytes)[0]
        return self.loads(fp.read(l))
    
    #---model deleter ----------------------------------------------------------

    def execute_deleter(self, item_cls, commit=None):
        """ Deletes models according to `deleter_selectors`
        and `deleter_keepers`. See their description in
        :py:class:`~.item.Item` configuration.
        
        :param item_cls: :py:class:`~.item.Item` instance for which deletion
            must be executed.
        :param commit: If `True` commits changes to database. If `None` then
            `autocommit` value (initially set at creation time) is used.
        """
        if not item_cls.metadata['model_deleter']:
            return
        item_cls.metadata['model_deleter'].execute_delete(self.db_adapter)
        self.__commit_if_needed(commit)
    
    
    def execute_scope_deleter(self, collection_id, commit=None):
        """ Calls :py:meth:`~execute_deleter` method for all item classes in
        scope.
        
        :param collection_id: An ID of an
            :py:class:`~utils.item_cls_collection.ItemClsCollection`
            (:py:class:`~.scope.Scope` is a subclass of it).
        :param commit: If `True` commits changes to database. If `None` then
            `autocommit` value (initially set at creation time) is used.
        """
        collection = ItemClsCollection.get_collection_by_id(collection_id)
        
        for item_cls in collection.get_all_item_classes():
            self.execute_deleter(item_cls, commit=False)
        
        self.__commit_if_needed(commit)
        
    #---merge policy -----------------------------------------------------------
    
    def create_merge_policy(self, policy, defaults=None):
        """ Creates an instance of :py:class:`~.merge_policy.MergePolicy`
        class.
        
        :param policy: *policy* argument for
            :py:class:`~.merge_policy.MergePolicy` class constructor.
        :param defaults: *defaults* argument for
            :py:class:`~.merge_policy.MergePolicy` class constructor.
        :returns: An instance of :py:class:`~.merge_policy.MergePolicy` class.
        """
        return MergePolicy(self.db_adapter, policy, defaults)
    
    
    