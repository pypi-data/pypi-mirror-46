from itertools import chain
from .db_persister import db_persist
from .merge_models import merge_models


class AdapterBase(object):
    """ Base adapter class for all database adapters.
    Here you can see descriptions of all required methods for DB adapters
    that are going to extend this class.
    
    :ivar adapter_settings: Adapter configuration object.
    """

    #: Must be set to `True` if ORM supports composite primary keys.
    COMPOSITE_KEYS_SUPPORTED = True
    
    #: Must be set to `True` if ORM automatically updates model that is being
    #: assigned to or unassigned from another model.
    REVERSE_MODEL_AUTOUPDATE_SUPPORTED = True
    
    #: This value must be set to `True` if a model has to be first saved
    #: before its changes can be committed to database. 
    SAVE_MODEL_BEFORE_COMMIT = False
    
    #: Maximum number of models that can be pulled with one query.
    #:
    #:     .. seealso::
    #:        `batch_size` class variable of
    #:        :py:class:`~save_to_db.core.item.Item` class.
    BATCH_SIZE = 300
    
    
    def __init__(self, adapter_settings):
        self.adapter_settings = adapter_settings
        
    
    #--- general methods -------------------------------------------------------
    
    @classmethod
    def is_usable(cls, model_cls):
        """ Returns `True` if this adapter can deal with `model_cls` class.
        Here you must somehow recognize that the model class was created
        using the particular ORM library that this adapter is for.
        
        :param model_cls: ORM model class (of any library).
        :returns: Boolean value indicating whether this adapter can deal with
            the given model class.
        """
        raise NotImplementedError()
    
    
    def commit(self):
        """ Commits current transaction to database. """
        raise NotImplementedError()
    
    
    def rollback(self):
        """ Rolls back current transaction. """
        raise NotImplementedError()
    
    
    @classmethod
    def iter_fields(cls, model_cls):
        """ Returns an iteratorable of field names and their types. Foreign keys
        and relations must be ignored.
        
        :param model_cls: ORM model class for which column data are going to be
            returned.
        :returns: An iteratorable of tuples of type:
        
                *(field_name, field_type)*
            
            Where:
            
                - *field_name* is a name of an ORM model field.
                - *field_type* must be one of the fields of
                  :py:class:`~.column_type.ColumnType` enumeration class.
        """
        raise NotImplementedError()
    
    
    @classmethod
    def iter_relations(cls, model_cls):
        """ Returns an iteratorable of names of fields that reference
        other ORM models.
        
        :param model_cls: ORM model class for which relations are going to be
            iterated.
        :returns: An iteratorable of tuples of type:
        
                *(relation_field_name, relation_model_cls, relation_type,
                reverse_key)*
                
            Where:
            
            - *relation_field_name* is a field of the `model_cls` that
              references another model.
            
            - *relation_model_cls* is an ORM model class being referenced.
              
            - *relation_type* must be one of the fields of
              :py:class:`~.relation_type.RelationType` enumeration class.
            
            - *reverse_key* is the relationship name used in related model
              to reference the original model.
        """
        raise NotImplementedError()
    
    
    @classmethod
    def iter_required_fields(cls, model_cls):
        """ Returns an iteratorable of names of fields that cannot be null for
        an ORM model class:
        
            - Simple field value cannot be null if the column has a not null
              constraint.
            - Relation field cannot be null if any column used as
              foreign key (can be multiple in case of composite key) is not
              null.
        
        :param model_cls: ORM model class for which relations are going to be
            iterated.
        :returns: An iteratorable of names of fields that cannot be null.
        """
        raise NotImplementedError()
    
    
    @classmethod
    def iter_unique_field_combinations(cls, model_cls):
        """ Returns an iteratorable of unique constraints (set of
        field names) on the model.
        
        .. note::
            Relation considered to be unique if the set of columns used as
            foreign keys (can be multiple in case of composite key) has a
            unique constraint.
        
            *Relations can be unique together with other fields.*
        
        :param model_cls: ORM model class for which relations are going to be
            iterated.
        :returns: Returns an iteratorable of unique constraints.
        """
        raise NotImplementedError()
    
    
    @classmethod
    def get_table_fullname(cls, model_cls):
        """ Returns full table name with schema (if applicable) used by an
        ORM model class.
        
        :param model_cls: An ORM model class.
        :returns: Full table name with schema (if applicable). Examples:
        
                - 'public.some_table'
                - 'some_table' (no schema, e.g. SQLite database).
        """
        raise NotImplementedError()
    
    
    def get_model_cls_by_table_fullname(self, name):
        """ Return ORM model class based on full table that that model class
        uses.
        
        :param name: table full name.
        :return: ORM model class.
        """
        raise NotImplementedError()
    
    
    def iter_all_models(self):
        """ Returns an iteratorable of all known ORM model classes.
        
        :returns: An iteratorable of all known ORM model classes
        """
        raise NotImplementedError()
    
    
    #--- methods for working with items ----------------------------------------
    
    def persist(self, item):
        """ Saves item data into a database by creating or update appropriate
        database records.
        
        :param item: an instance of
            :py:class:`~save_to_db.core.item_base.ItemBase` to persist.
        :returns: Item list and corresponding ORM models as a list of lists
            (in case one item updates multiple models).
        """
        return db_persist(self, item)


    def get(self, items_and_fkeys):
        """ Accepts items and their foreign keys and gets corresponding models
        from database.
        
        .. warning::
            Items must have the same ORM model class.
        
        :param items_and_fkeys: a list of lists of type:
        
            .. code-block:: Python
            
                [
                    [item, {fkey: model, ...}],
                    ...
                ]
                
        :returns: List of created and updated models.
        """
        raise NotImplementedError()
    

    def delete(self, model):
        """ Deletes model from the database.
        
        :param model: ORM model to be deleted.
        """
        raise NotImplementedError()
    

    def create_blank_model(self, model_cls):
        """ Create empty model instance.
        
        :param model_cls: ORM model class to create.
        :returns: Newly created ORM model instance.
        """
        raise NotImplementedError()
    

    def add_related_models(self, model, fkey, related_models):
        """ Adds related models for x-to-many relationships to a parent model.
        
        :param model: Parent ORM model instance.
        :param key: Parent ORM model instance foreign key field.
        :param related_models: Referenced ORM models.
        """
        raise NotImplementedError()
    
    
    def clear_related_models(self, model, fkey):
        """ Removes related models for x-to-many relationships from a parent
        model.
        
        :param model: Parent ORM model instance.
        :param fkey: Parent ORM model instance foreign key field.
        """
        raise NotImplementedError()
    
    
    def related_x_to_many_exists(self, model, fkey):
        """ Returns `True` if `model` contains any other models with
        `field_name` relation key.
        
        :param model: Parent ORM model instance.
        :param fkey: Parent ORM model instance foreign key field.
        :returns: `True` if `model` contains any other models with
            the relation key.
        """
        raise NotImplementedError()
    

    def related_x_to_many_contains(self, model, fkey, child_models):
        """ Returns list of contained models from `child_models` by
        `model` parent model trough `field_name` foreign key field.
        
        .. note::
            The returned list must contain instances from `child_models` list,
            not other instances for the same database rows.
        
        :param model: ORM model instance.
        :param fkey: field name used for reference.
        :param child_models: list of child models.
        :returns: Returns list of contained models from `child_models` by
            `model` parent model trough `fkey` foreign key field.
        """
        raise NotImplementedError()
    
    
    @classmethod
    def get_primary_key_names(cls, model_cls):
        """ Returns tuple of primary key names.
        
        :param model_cls: ORM model class.
        :returns: Tuple of primary key names of `model_cls`.
        """
        raise NotImplementedError()
    
    
    def save_model(self, model):
        """ Saves ORM model to database.
        
        .. note::
            If possible, session must not be committed, just flushed.
        
        :param model: Parent ORM model instance.
        :param key: Parent ORM model instance foreign key field.
        """
        raise NotImplementedError()
    
    

    def execute_delete(self, model_cls, selectors, keepers):
        """ Deletes all rows in database that can be selected using `selectors`
        except those that can be selected using `keepers`.
        
        For example, suppose our `selectors` and `keepers` look like this:
        
        .. code-block:: Python
        
            selectors = [{
                'field_1': 10,
                'field_2': 20,
            }, {
                'field_1': 30,
                'field_2': 40,
            }]
            
            keepers = [{
                'field_10': 100,
                'field_20': 200,
            }, {
                'field_10': 300,
                'field_20': 400,
            }]
        
        SQL query can look like this:
        
        .. code-block:: postgres
        
            DELETE FROM model_cls_table
            WHERE
            /* selectors */
            ((field_1 = 10 AND field_2 = 20) OR
             (field_1 = 30 AND field_2 = 40))
            AND
            /* keepers */
            ((field_10 != 100 OR field_20 != 200) AND
             (field_10 != 300 OR field_20 != 400))
        
        :param model_cls: ORM model class used to work with database table.
        :param selectors: List of dictionaries with model field names as keys
            and model field values as dictionary values.
        :param keepers: Same as `selectors`.
        """
        raise NotImplementedError()
    
    
    def execute_unref(self, parent, fkey, selectors, keepers):
        """ Removes models from x-to-many field.
        
        :param parent: Parent ORM model.
        :param fkey: X-to-many foreign key field of `parent`.
        :param selectors: List of dictionaries with model field names as keys
            and model field values as dictionary values.
            
            .. seealso::
        
                `selectors` and `keepers` parameters of
                :py:meth:`~.execute_delete` method.
                
        :param keepers: Same as `selectors`.
        """
        raise NotImplementedError()
    
    
    def get_related_x_to_many(self, model, fkey):
        """ Returns iterable of many-to-many related  models.
        
        :param model: ORM model instance.
        :param fkey: field name used for reference.
        """
        return getattr(model, fkey)
    
    
    def merge_models(self, models, merge_policy=None, ignore_fields=None):
        """ Merges models into one. First model from `models` becomes the
        result model, all other models get deleted.
        
        :param models: List of ORM models (of the same class) to be merged into
            one.
        :param merge_policy: An instance of
            :py:class:`~save_to_db.core.merge_policy.MergePolicy` class.
        :param ignore_fields: List of field to ignore (not copy to result
            model) when merging.
        :returns: First model from `models` into which all other models are
            merged.
        """
        return merge_models(self, models, merge_policy=merge_policy,
                            ignore_fields=ignore_fields)
    
    
    #--- helper functions ------------------------------------------------------
    
    def pprint(self, *models):
        """ Pretty prints `models`.
        
        :param \*models: List of models to print.
        """
        if not models:
            return
        
        def repr_model(model):
            pkeys_names = self.get_primary_key_names(model.__class__)
            pkeys_values = list(str(getattr(model, pkey))
                                for pkey in pkeys_names)
            return '({},)'.format(','.join(pkeys_values))
            
        
        model_cls = None
        for model in models:
            if not (model.__class__ is model_cls):
                model_cls = model.__class__
                pkeys_names = self.get_primary_key_names(model_cls)
        
                field_names = [
                    fname for fname, _, in self.iter_fields(model_cls)
                ]
                for pk_fname in pkeys_names:
                    field_names.remove(pk_fname)
                field_names.sort()
                
                relations = {
                    fname: direction
                    for fname, _, direction, _ in self.iter_relations(model_cls)
                }
                relation_names = list(relations.keys())
                relation_names.sort()
                
                padding = len(max(chain(pkeys_names,
                                        field_names,
                                        relation_names), key=len))
                
            to_print = ['{}:'.format(model_cls.__name__)]
            for fname in chain(pkeys_names, field_names, relation_names):
                if fname in field_names or fname in pkeys_names:
                    value = getattr(model, fname)
                    no_value = value is None
                else:
                    if not relations[fname].is_x_to_many():
                        other_model = None
                        if hasattr(model, fname):
                            other_model = getattr(model, fname)
                            
                        if other_model is None:
                            value = None
                            no_value = True
                        else:
                            value = repr_model(other_model)
                            no_value = False
                    else:
                        other_models = self.get_related_x_to_many(model, fname)
                        no_value = not other_models
                        value = '[{}]'.format(
                            ','.join([repr_model(m) for m in other_models]))
                    
                to_print.append('    {:<3} {:>{padding}}: {}'.format(
                    'PK' if fname in pkeys_names else
                        '' if no_value else '::',
                    fname if no_value else fname.upper(),
                    value,
                    padding=padding))
            
            print('\n'.join(to_print))
    
    
    #--- methods for tests -----------------------------------------------------
    
    def get_all_models(self, model_cls, sort_key=None):
        """ Returns all models from database `model_cls` class.
        
        .. note::
            Used by tests only.
        
        :param model_cls: An ORM model class.
        :param sort_key: If not `None` then result is sorted using this
            function as `key` argument for `sort` method of the result list.
        :returns: List of all model instances for `model_cls` class.
        """
        raise NotImplementedError()
        