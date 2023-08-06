from save_to_db.exceptions import (ModelClsAlreadyRegistered,
                                   UnknownRelationFieldNames,
                                   UnknownModelDefaultKey,)


class MergePolicy(dict):
    """ Merge model policy defines how model conflicts should be resolved
    when using
    :py:meth:`~save_to_db.adapters.utils.adapter_base.AdapterBase.merge_models`
    method of
    :py:class:`~save_to_db.adapters.utils.adapter_base.AdapterBase` class.
    
    There are conflicts of two types:
    
        - Meging models have x-to-one relationship with other model class, but
          point to diffent model instances.
        - Meging models have x-to-many relationship with other model class, but
          assing all the many models to one merged models breaks one or more
          unique constraints.
          
    :param db_adapter: An instance of
        :py:class:`~save_to_db.adapters.utils.adapter_base.AdapterBase`
        subclass.
    :param policy:
        A dictionary that looks like this:
        
            .. code-block:: Python
            
                merge_policy = {
                    OrmModelClass_1: {
                        x_to_1_field_1: resolve_x_to_1_field_1,
                        x_to_1_field_2: resolve_x_to_1_field_2,
                        1_to_many_field_1: resolve_1_to_many_field_1,
                        1_to_many_field_2: False,  # merge not allowed
                        ...
                    },
                    ...
                }
                
            **Where:**
        
                - *OrmModelClass_1* is a reference to an ORM model class.
                - *x_to_1_field_1* and *x_to_1_field_2* are x-to-one foreign
                  key field names from the class.
                - *1_to_many_field_1* and *1_to_many_field_2* are one-to-may
                  foreign key field names from the class.
                - *resolve_x_to_1_field_1* and *resolve_x_to_1_field_2* are
                  merge functions for the fields, function arguments:
                      
                    - *model* is model into which other model is merged.
                    - *merged_model* is a model that is in the process of being
                      merged.
                    - *child_model* is a model that *model* points to with
                      *forward_foreign_key*.
                      
                      *Here we refer to the model being
                      pointed to as "child", although in reality it can be
                      different.*
                    - *merged_child_model* is a model that *merged_model* points
                      to with *forward_foreign_key*.
                    - *forward_foreign_key* is a name of a parent field that
                      points to child.
                    - *reverse_foreign_key* is a name of a child field that
                      points parent.
                
                  *child_model* and *merged_child_model* are not the same, but
                  being pointed to by parent models from `models` argment using
                  the same key.
                  
                  The function must return one child model to be used.
                  
                  .. note::
                      *merged_child_model* is not deleted after the merging, for
                      x-to-one relationships it can be left unchanged.
                
                - *resolve_1_to_many_field_1* is a merge function for
                  the field. Conflicts in one-to-many fields may arise when
                  there is a unique constraint that is going to be broken if two
                  child models start to point to the same parent model.
                  The function accepts arguments the same arguments as
                  *resolve_x_to_1_field_1* and a list of unique
                  constaints (lists of field names) that are going to be broken.
                  
                  .. warning::
                      *merged_child_model* is not deleted after the merging.
                      Delete it yourself or make sure it does not brake the
                      unique constraints.
    
    :param defaults:
        Default model resolver. A dictionary that looks like this:
            
            .. code-block:: Python
            
                defaults = {
                    OrmModelClass_1: {
                        'one': resolve_x_to_1_field_1,
                        'many': resolve_1_to_many_field_1,
                    },
                    ...
                }
            
            **Where:**
                
                - *OrmModelClass_1*,
                - *resolve_x_to_1_field_1*,
                - and *'resolve_1_to_many_field_1* are same as for the
                  `policy` parameter.
            
        If, in the example above, some other ORM model class has a relationship
        with *OrmModelClass_1*, but does not define a resolver, default model
        resolver is used. 
    """
    
    #: Default key for x-to-one resolvers.
    REL_ONE = 'one'
    #: Default key for x-to-many resolvers.
    REL_MANY = 'many'
    
    def __init__(self, db_adapter, policy, defaults=None):
        defaults = defaults or {}
        self.db_adapter = db_adapter
        self.__validate(policy, defaults)
        self.defaults = defaults
        self.update(policy)
        self.__resolve_defaults()
        
        self.registered_models = set(policy.keys()).union(defaults.keys())
    
    
    def add_model_policy(self, model_cls, model_policy, model_defaults=None):
        """ Adds merge policy for a model.
        
        :param model_cls: An ORM model class to add.
        :param model_policy: Merge policy for the class.
            This has the same structure as `policy[model_cls]` (where
            `policy` is the argument passed to constructor).
        :param model_defaults: Default model resolvers for the class.
            This has the same structure as `defaults[model_cls]` (where
            `defaults` is the argument passed to constructor).
        """
        if model_cls in self.registered_models:
            raise ModelClsAlreadyRegistered(
                'Merge policy already registered for class {}'.format(model_cls)
            )
        
        model_defaults = model_defaults or {}
        self.__validate_model_policy(model_cls, model_policy)
        self.__validate_model_defaults(model_defaults)
        self[model_cls] = model_policy
        self.defaults[model_cls] = model_defaults
        self.__resolve_defaults()
        
        self.registered_models.add(model_cls)
    
    
    def __resolve_defaults(self):
        
        for model_cls in self.db_adapter.iter_all_models():
            for fkey, fmodel_cls, direction, _ in \
                    self.db_adapter.iter_relations(model_cls):
                
                if fmodel_cls not in self.defaults:
                    continue
                
                if direction.is_x_to_one():
                    multiplication_key = self.REL_ONE
                else:
                    multiplication_key = self.REL_MANY
                
                if multiplication_key not in self.defaults[fmodel_cls]:
                    continue
                
                if model_cls not in self:
                    self[model_cls] = {}
                
                # default must not overwrite
                if fkey not in self[model_cls]:
                    self[model_cls][fkey] = \
                        self.defaults[fmodel_cls][multiplication_key]
    
    
    def __validate(self, policy, defaults):
        for model_cls, model_policy in policy.items():
            self.__validate_model_policy(model_cls, model_policy)
        
        for model_cls, model_defaults in defaults.items():
            self.__validate_model_defaults(model_defaults)
    
    
    def __validate_model_policy(self, model_cls, model_policy):
        policy_fkeys = set(model_policy)
        model_fkeys = set(
            fkey for fkey, _, _, _ in self.db_adapter.iter_relations(model_cls)
        )
        unknown_fkeys = policy_fkeys - model_fkeys
        if unknown_fkeys:
            raise UnknownRelationFieldNames(model_cls, unknown_fkeys)
        
    
    def __validate_model_defaults(self, model_defaults):
        default_keys = set(model_defaults)
        known_keys = {self.REL_ONE, self.REL_MANY}
        unknown_fkeys = default_keys - known_keys
        if unknown_fkeys:
            raise UnknownModelDefaultKey(unknown_fkeys)