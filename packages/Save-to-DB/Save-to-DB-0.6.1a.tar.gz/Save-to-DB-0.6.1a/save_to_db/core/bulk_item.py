from copy import copy
from .item import ItemBase
from .item_contructor import complete_item_structure
from save_to_db.exceptions import BulkItemOnetoXDefaultError


class BulkItem(ItemBase):
    """ This class deals with instances of :py:class:`~.item.Item` in chunks.
    It can create or update multiple database rows using single query, e.g. it
    can persist multiple items at once.
    
    .. note::
        You get items values from a bulk item like this:
        
            - `bulk[number]` return item at a given index `number`;
            - `bulk[string]` return default value for a key `string`;
            - `bulk[slice]` (e.g. `bulk[1:2]`) returns copy of the bulk
              containing specified items.
              
    .. note::
        Defaults order is based on the number of '__' the key contains,
        shorter keys are prioritized. This is due to the fact that default
        values can be another items.
    
    :param item_cls: A subclass of :py:class:`~.item.Item` that
        this class deals with.
    :param \*\*kwargs: Values that will be saved as **default** item data.
    """
    
    #--- special methods -------------------------------------------------------
    
    def __init__(self, item_cls, **kwargs):
        self.item_cls = item_cls
        self.bulk = []
        
        self.data = {}
        for key, value in kwargs.items():
            self[key] = value  # this will trigger `__setitem__` function
        
    
    def __setitem__(self, key, value):
        real_key = self.item_cls._get_real_keys(key)
        real_key_str = '__'.join(real_key)
        
        # value x-to-one must not be an item
        if isinstance(value, ItemBase):
            # getting last relation type
            item_cls = self.item_cls
            for key in real_key:
                if key not in item_cls.relations:
                    break
                relation = item_cls.relations[key]
                item_cls = relation['item_cls']
            
            if relation['relation_type'].is_one_to_x():
                raise BulkItemOnetoXDefaultError(self.item_cls, key,
                                                 real_key_str)
        
        self.data[real_key_str] = value
        
    
    def __getitem__(self, key):
        if isinstance(key, int):
            return self.bulk[key]
        
        if isinstance(key, slice):
            new_bulk = self.item_cls.Bulk()
            new_bulk.data = copy(self.data)
            new_bulk.add(*self.bulk[key])
            return new_bulk
        
        real_keys = self.item_cls._get_real_keys(key)
        return self._get_direct(real_keys)
    
    
    def _get_direct(self, real_keys):
        real_key_str = '__'.join(real_keys)
        if real_key_str in self.data:
            return self.data[real_key_str]
        
        item_cls = self.item_cls
        previous_cls = None
        for real_key in real_keys:
            previous_cls = item_cls
            if real_key in item_cls.relations:
                item_cls = item_cls.relations[real_key]['item_cls']
            else:
                raise KeyError(real_key)
        
        self[real_key_str] = previous_cls._genitem(real_keys[-1])
        return self.data[real_key_str]
    
    
    def __delitem__(self, key):
        real_key = self.item_cls._get_real_keys(key, as_string=True)
        del self.data[real_key]
    
    
    def __contains__(self, key):
        try:
            real_keys = self.item_cls._get_real_keys(key)
        except KeyError:
            return False
        return self._contains_direct(real_keys)
    
    
    def _contains_direct(self, real_keys):
        return '__'.join(real_keys) in self.data
    
    
    def __iter__(self):
        for item in self.bulk:
            yield item
    
    
    def __len__(self):
        return len(self.bulk)
        
    
    #--- utility methods -------------------------------------------------------
    
    def to_dict(self, revert=False):
        return self._to_dict(revert=revert,
                             _item_to_dict={}, _address_to_item={})
        
        
    def _to_dict(self, revert, _item_to_dict, _address_to_item):
        self_address = id(self)
        if self_address in _item_to_dict:
            if self_address not in _address_to_item:
                _address_to_item[self_address] = len(_address_to_item) + 1
            self_id = _address_to_item[self_address]
            _item_to_dict[self_address]['id'] = self_id
            return {
                'id': self_id,
            }
        
        result = {
            'defaults': {},
            'bulk': [],
        }
        _item_to_dict[self_address] = result
        
        # defaults first in `_load_dict()` as well
        defaults = result['defaults']
        for key, value in self.data.items():
            if not isinstance(value, ItemBase):
                if revert:
                    value = self.item_cls.revert_field(key, value,
                                                       aliased=False)
                defaults[key] = value
            else:
                defaults[key] = value._to_dict(revert=revert,
                                               _item_to_dict=_item_to_dict,
                                               _address_to_item=_address_to_item)
        
        bulk = result['bulk']
        for item in self.bulk:
            bulk.append(item._to_dict(revert=revert,
                                      _item_to_dict=_item_to_dict,
                                      _address_to_item=_address_to_item))
        
        return result
    
    
    def load_dict(self, data):
        return self._load_dict(data, _id_to_item={})
    

    def _load_dict(self, data, _id_to_item):
        if 'id' in data:
            if data['id'] not in _id_to_item:
                _id_to_item[data['id']] = self.item_cls.Bulk()
                
            bulk = _id_to_item[data['id']]
            if 'defaults' not in data:
                return _id_to_item[data['id']]
        else:
            bulk = self.item_cls.Bulk()
        
        # defaults first in `_to_dict()` as well
        for key, value in data['defaults'].items():
            # getting relation class
            cur_cls = bulk.item_cls
            for cur_key in key.split('__'):
                if cur_key in cur_cls.relations:
                    cur_cls = cur_cls.relations[cur_key]['item_cls']
                else:
                    cur_cls = None
                    break
            
            if cur_cls:  # relation
                bulk[key] = bulk[key]._load_dict(value, _id_to_item)
            else:
                bulk[key] = value
        
        # bulk
        for dict_wrapper in data['bulk']:
            bulk.add(bulk.item_cls()._load_dict(dict_wrapper, _id_to_item))
        
        return bulk
    
    
    #--- properties ------------------------------------------------------------
    
    @property
    def model_cls(self):
        """ Property that returns `model_cls` attribute of the `item_cls`
        class.
        """
        return self.item_cls.model_cls
    
    def get_item_cls(self):
        return self.item_cls
    
    def is_scoped(self):
        return self.item_cls.metadata['collection_id'] != None
    
    def get_collection_id(self):
        return self.item_cls.metadata['collection_id']
    
    
    #--- main methods ----------------------------------------------------------
    
    def add(self, *items):
        """ Adds `item` to the bulk.
        
        :param \*item: List of instances of :py:class:`~.item_base.ItemBase`
            class to be added to the bulk.
        """
        for item in items:
            if item not in self.bulk:
                self.bulk.append(item)
    
    
    def gen(self, *args, **kwargs):
        """ Creates a :py:class:`~.item.Item` instance and adds it to the bulk.
        
        :param \*args: Positional arguments that are passed to the item
            constructor.
        :param \*\*kwargs: Keyword arguments that are passed to the item
            constructor.
        :returns: :py:class:`~.item.Item` instance.
        """
        item = self.item_cls(*args, **kwargs)
        self.add(item)
        return item
    
    
    def remove(self, *items):
        """ Removes `item` from the bulk.
        
        :param \*items: List of instances of :py:class:`~.item_base.ItemBase`
            class to be removed from the bulk.
        """
        for item in items:
            if item in self.bulk:
                self.bulk.remove(item)
    
    
    def as_list(self):
        return self.bulk
    
    
    def is_single_item(self):
        return False
    
    
    def is_bulk_item(self):
        return True
    
    
    def revert(self):
        return self._revert(_procesed_items=[])
    
    
    def _revert(self, _procesed_items=[]):
        if self in _procesed_items:
            return
        _procesed_items.append(self)
        
        for key, value in self.data.items():
            if not isinstance(value, ItemBase):
                self.data[key] = self.item_cls.revert_field(key, value,
                                                            aliased=False)
            else:
                self.data[key]._revert(_procesed_items=_procesed_items)
        
        for item in self.bulk:
            item._revert(_procesed_items=_procesed_items)
    
    
    def process(self):
        self._process(_procesed_items=[])
        return complete_item_structure(self)
    

    def _process(self, _procesed_items, d=True):
        if self in _procesed_items:
            return
        _procesed_items.append(self)
        
        keys = list(self.data.keys())
        keys.sort(key=lambda key: key.count('__'))
        for key in keys:
            value = self.data[key]
            
            end_item_cls = self.item_cls
            end_relation = None
            for subkey in key.split('__'):
                if subkey in end_item_cls.relations:
                    end_relation = end_item_cls.relations[subkey]
                    end_item_cls = end_relation['item_cls']
                else:
                    end_relation = None
            
            if not end_relation:  # not a relations
                self.data[key] = self.item_cls.process_field(key, value,
                                                             aliased=False)
            else:
                if not isinstance(value, list) or \
                        not end_relation['relation_type'].is_x_to_many():
                    value._process(_procesed_items=_procesed_items)
                    self.data[key] = value
                else:
                    bulk_item = self.item_cls.relations[key]['item_cls'].Bulk()
                    bulk_item.add(*value)
                    bulk_item._process(_procesed_items=_procesed_items)
                    self.data[key] = bulk_item
            
            for item in self.bulk:
                if key in item:
                    continue
                
                if not isinstance(self.data[key], ItemBase) or \
                        not self.data[key].is_bulk_item():
                    item[key] = self.data[key]
                else:
                    item[key] = self.data[key][:]  # a copy
        
        for item in self.bulk:
            item._process(_procesed_items=_procesed_items)
        
        