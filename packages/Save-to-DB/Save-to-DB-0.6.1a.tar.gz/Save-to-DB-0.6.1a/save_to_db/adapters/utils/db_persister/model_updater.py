from save_to_db.exceptions import (CannotMergeModels,
                                   CannotMergeModelsForItem,
                                   MultipleModelsMatch,)
from save_to_db.core.item_base import ItemBase
from save_to_db.adapters.utils.relation_type import RelationType

from .process_keeper import ProcessKeeper



class ModelUpdater(object):
    
    def __init__(self, item_structure, db_adapter):
        self.process_keeper = ProcessKeeper(item_structure)
        self.db_adapter = db_adapter
        self.created_models = []
        # for x-to-many relationships we have to keep track of missing values
        # as during model updated after first model is set, relationship is
        # no longer empty, the rest of the child models won't set 
        self.no_value_models = []
        self.no_value_fields = []
    
    def add_created_model(self, model):
        self.created_models.append(model)
    
    def is_model_created(self, model):
        return model in self.created_models
    
    #--- checkers --------------------------------------------------------------
    
    def can_set_model_field(self, item, model, field_name, value):
        """ Checks if we can set given `value` for the given `model` using
        given `field_name`.
        
        .. note::
            `model` can be `None` if the corresponding model for the item was
            not yet created.
            
        :param item: Item used to populated `model`.
        :param model: ORM model that corresponds to the `item`.
        :param field_name: Field name used to set value for the `model`.
        :param value: Value to set. For x-to-many relationships only a single
            value must be used.
        :returns: `True` if the `value` can be set, `False` otherwise.
        """
        # checking for get_only_mode
        if item.get_only_mode or \
                (isinstance(value, ItemBase) and value.get_only_mode):
            return False
        
        # checking if the field can be always set
        if field_name not in item.norewrite_fields or \
                item.norewrite_fields[field_name] is None:
            return True
        
        created = model is None or self.is_model_created(model)
        rewrite_none = item.norewrite_fields[field_name]
        
        # not a relation
        if field_name not in item.relations:
            if created:
                return True
            model_value = getattr(model, field_name)
            return False if model_value is not None else rewrite_none
        
        # value is a related model
        elif created and (value is None or self.is_model_created(value)):
            return True
        
        relation_type = item.relations[field_name]['relation_type']
        
        # for x-to-many relationships we can add to many a newly created model
        if value:
            if relation_type.is_many_to_x() and created:
                return True
            if relation_type.is_x_to_many() and \
                    (value is None or self.is_model_created(value)):
                return True
        
        # at least one of the model already existed, we can set only if
        # we can rewrite nones and the values are `None`
        if rewrite_none is False:
            return False
            
        # checking values
        def model_had_value(relation_type, model, field_name):
            if model in self.no_value_models:
                index = self.no_value_models.index(model)
                if field_name in self.no_value_fields[index]:
                    return False
            
            result = __model_had_value(relation_type, model, field_name)
            
            if not result:
                if model not in self.no_value_models:
                    self.no_value_models.append(model)
                    self.no_value_fields.append([field_name])
                else:
                    index = self.no_value_models.index(model)
                    self.no_value_fields[index].append(field_name)
            return result
        
            
        def __model_had_value(relation_type, model, field_name):    
            if not hasattr(model, field_name):
                return False
            if relation_type.is_x_to_one():
                model_value = getattr(model, field_name)
                return model_value is not None
            else:
                return self.db_adapter.related_x_to_many_exists(
                    model, field_name)
        
        # this side
        if model and model_had_value(relation_type, model, field_name):
            return False
        
        # that side
        if value is not None:
            reverse_key = item.relations[field_name]['reverse_key']
            if reverse_key and model_had_value(relation_type.reverse(),
                                               value, reverse_key):
                return False
        
        return True
    
    
    def can_create_model(self, item, fkeys):
        """ Checks that a new row can be created in database for
        the item.
        
        .. note::
            For relations fields we check that it is in `fkeys`. For normal
            fields we just check that it is present and not `None`.
        
        :param item: Item for which a corresponding model should be created.
        :param fkeys: A `dict` where keys are relation field names and values
            are ORM models that were got from or created in database.
        :returns: `True` if a corresponding row for the item can be created in
            database, `False` otherwise.
        """
        if item.creators is None or item.get_only_mode or item.update_only_mode:
            return False
        if not item.creators:
            return True
        
        for group in item.creators:
            can_create = True
            for field_name in group:
                if field_name in item.relations:
                    # checking can set on the other side of relationship
                    if field_name not in fkeys:
                        can_create = False
                        break
                    for f_model in fkeys[field_name]:
                        if not self.can_set_model_field(item, None, field_name,
                                                        f_model):
                            can_create = False
                            break
                    if not can_create:
                        break
                        
                # always can set normal fields when creating
                elif field_name not in item.data:
                    can_create = False
                    break
                
            if can_create:
                return True
        return False
    
    #--- modifiers -------------------------------------------------------------
    
    def clear_related_models(self, item, model, fkey):
        """ Removes all referenced models by the foreign key `fkey` of `model`
        if possible.
        
        :param item: Item used to get or create the `model`.
        :param model: model created or loaded from database using the `item`.
        :param fkey: x-to-many foreign key that needs to get empty. 
        """
        relation = item.relations[fkey]
        
        if not self.db_adapter.REVERSE_MODEL_AUTOUPDATE_SUPPORTED and \
                relation['reverse_key'] and relation['item_cls'] and \
                relation['relation_type'] is RelationType.ONE_TO_MANY:
            item_cls = relation['item_cls']
            
            models_to_check = []
            for item_track in self.process_keeper[item_cls]:
                models_to_check.extend(item_track.models)
            contained_models = self.db_adapter.related_x_to_many_contains(
                model, fkey, models_to_check)
             
            for contained_model in contained_models:
                self.set_related_model(item_track.item,
                                       contained_model,
                                       relation['reverse_key'],
                                       None)
    
        self.db_adapter.clear_related_models(model, fkey)
        
        # clearing model_unrefs
        model_unrefs = item.metadata['model_unrefs']
        if fkey in model_unrefs:
            model_unrefs[fkey].reset()
        
    
    def set_related_model(self, item, model, fkey, fmodel):
        """ Sets a model `fmodel` as a related model of `model` under
        foreign key `fkey` if possible.
        
        :param item: Item used to get or create the `model`.
        :param model: model created or loaded from database using the `item`.
        :param fkey: foreign key used to reference `fmodel`.
        :param fmodel: referenced foreign model. 
        """
        if not self.can_set_model_field(item, model, fkey, fmodel):
            return
            
        def clean_1_to_1_relation(model, fkey, fmodel, item_cls, reverse_key):
            if reverse_key and hasattr(model, fkey):
                related_model = getattr(model, fkey)
                if related_model and related_model != fmodel:
                    setattr(related_model, reverse_key, None)
                    self.db_adapter.save_model(related_model)
             
            for item_track in self.process_keeper[item_cls]:
                found = False
                for track_model in item_track.models:
                    if track_model == model:
                        continue
                    if hasattr(track_model, fkey) and \
                            getattr(track_model, fkey) == fmodel:
                        found = True
                        setattr(track_model, fkey, None)
                        self.db_adapter.save_model(track_model)
                        break
                 
                if found:
                    break
                 
        relation = item.relations[fkey]
        if relation['relation_type'] is RelationType.ONE_TO_ONE and \
                ((not hasattr(model, fkey) and fmodel is not None) or
                 (hasattr(model, fkey) and getattr(model, fkey) != fmodel)):
            # forward relation
            clean_1_to_1_relation(model, fkey, fmodel,
                                  type(item), relation['reverse_key'])
            # backward
            if relation['reverse_key']:
                clean_1_to_1_relation(fmodel, relation['reverse_key'], model,
                                      relation['item_cls'], fkey)
        
        setattr(model, fkey, fmodel)
    
    
    def add_related_models(self, item, model, fkey, fmodels):
        """ Adds related models `fmodels` to x-to-many relationship of `model`
        using foreign key `fkey`.
        
        :param item: Item used to get or create the `model`.
        :param model: model created or loaded from database using the `item`.
        :param fkey: foreign key used to reference `fmodels`.
        :param fmodels: referenced models.
        """
        # no need to updated other models:
        #    1. If it is many-to-many relationship, then calling this function
        #       does not mean that other relationships must be nullified
        #    2. If it one-to-many relationship, then foreign key is on the
        #       `fmodels` models.
        filtered_models = [
            fmodel for fmodel in fmodels
            if self.can_set_model_field(item, model, fkey, fmodel)
        ]
        self.db_adapter.add_related_models(model, fkey, filtered_models)
        
        # saving to model_unrefs
        model_unrefs = item.metadata['model_unrefs']
        if fkey in model_unrefs:
            for fmodel in fmodels:
                if self.is_model_created(fmodel):
                    self.db_adapter.save_model(fmodel)
                model_unrefs[fkey].collect_model(fmodel)
    
    #---------------------------------------------------------------------------
    
    def merge_models_for_item(self, item, models):
        if not models:
            return None
        
        # sorting models to always get the same result after merging
        models = list(models)
        pk_list = list(self.db_adapter.get_primary_key_names(type(models[0])))
        pk_list.sort()
        get_model_key = lambda model: tuple(getattr(model, field)
                                            for field in pk_list)
        models.sort(key=get_model_key)
        
        # `before_models_merge` hook
        item.before_models_merge(models)
        
        try:
            result_model = self.db_adapter.merge_models(models)
        except CannotMergeModels as e:
            raise CannotMergeModelsForItem(item, *e.args)
        
        # `after_models_merge` hook
        item.after_models_merge(result_model)
        
        return result_model
    
    
    def update_model_fields(self, item_track, model):
        created = self.is_model_created(model)
        
        for field_name in item_track.item.data:
            if field_name in item_track.item.fields:
                if self.can_set_model_field(item_track.item, model, field_name,
                                            item_track.item[field_name]):
                    setattr(model, field_name, item_track.item[field_name])
            
        # many to one before saving
        for fkey in item_track.fkeys:
            relation_type = item_track.item.relations[fkey]['relation_type']
            if relation_type.is_x_to_one():
                self.set_related_model(item_track.item, model, fkey,
                                       item_track.fkeys[fkey][0])
        
        # for the rest model has to be saved
        if created and self.db_adapter.SAVE_MODEL_BEFORE_COMMIT:
            self.db_adapter.save_model(model)
    
        for fkey, fmodels in item_track.fkeys.items():
            relation_type = item_track.item.relations[fkey]['relation_type']
            if not relation_type.is_x_to_one():
                self.add_related_models(item_track.item,  model, fkey, fmodels)
    
    
    def update_relationships(self, items, models):
        """ Completes relationships on the `items`, e.g. sets reverse
        relationships where possible.
        
        :param items: All the items that we deal with. These items include
            the items that we persist directly and those referenced by those
            items.
        :param models: All the models that were loaded from database or
            created using the `items`.
        :returns: `creator_keeper` that contains items that can be now created
            because of updated relationships.
            `getter_keeper` that contains items that can be now tried to be
            loaded from database because of updated relationships.
        """
        original_items, original_models = items, models
        
        creator_keeper = ProcessKeeper()
        getter_keeper = ProcessKeeper()
        
        # update_fkey --------------------------------------------------------------
        
        def update_fkey(item_track, fkey, foreign_item_track):
    
            def update_result_keepers():
                item_cls = type(item)
                for keeper, groups in [[creator_keeper[item_cls], item.creators],
                                       [getter_keeper[item_cls], item.getters]]:
                    if groups is None:
                        continue
                    
                    for group in groups:
                        if fkey not in group:
                            continue
                        
                        do_add = True
                        for field in group:
                            if field not in item:
                                do_add = False
                                break
                        if do_add:
                            keeper.append(item_track)
                            break
            
            if foreign_item_track is not None:
                foreign_models = foreign_item_track.models
                if not foreign_models:
                    return
            else:
                foreign_models = [None]
            
            item = item_track.item
            models = item_track.models
            fkeys = item_track.fkeys[fkey]
            
            relation = item.relations[fkey]
            is_x_to_one = relation['relation_type'].is_x_to_one()
            
            if foreign_item_track is not None:
                keepers_updated = False
                for foreign_model in foreign_models:
                    if foreign_model not in fkeys:
                        fkeys.append(foreign_model)
                        if not keepers_updated:
                            update_result_keepers()
            else:
                fkeys.append(None)
    
            for model in models:
                if is_x_to_one:
                    if len(foreign_models) > 1:
                        # cannot reference more then one model
                        raise MultipleModelsMatch(item, fkey, foreign_models)
                    self.set_related_model(item_track.item, model, fkey,
                                           foreign_models[0])
                else:
                    self.add_related_models(item_track.item, model, fkey,
                                            foreign_models)
    
        # saving models to process_keeper ------------------------------------------
        
        for item, models in zip(original_items, original_models):
            if not models:
                continue
            item_cls = type(item)
            
            # getting item_track
            for item_track in self.process_keeper[item_cls]:
                if item_track.item is item:
                    break
                
            for model in models:
                if model not in item_track.models:
                    item_track.models.append(model)
                    
                    if len(item_track.models) > 1 and \
                            not item_cls.allow_multi_update:
                        item_track.models = [
                            item_track.item.resolve_model(item_track.models)
                        ]
                
        # updating relationships ---------------------------------------------------
        
        for item, models in zip(original_items, original_models):
            if not models:
                continue
            item_cls = type(item)
            
            # getting item_track
            for item_track in self.process_keeper[item_cls]:
                if item_track.item is item:
                    break
                   
            # --- forward relations ---
            for f_fkey in item_cls.relations:
                if f_fkey not in item:
                    continue
                
                if item[f_fkey] is None:
                    update_fkey(item_track, f_fkey, None)
                    continue
                
                for f_item in item[f_fkey].as_list():
                    
                    # looking for f_item_track
                    found = False
                    for f_item_cls in self.process_keeper:
                        for f_item_track in self.process_keeper[f_item_cls]:
                            if f_item_track.item is f_item:
                                update_fkey(item_track, f_fkey, f_item_track)
                                found = True
                                break
                        if found:
                            break
    
                    # updating f_fkey
                    
            # --- backward relations ---
            for b_item_cls in self.process_keeper:
                # looking for b_item_track
                for b_item_track in self.process_keeper[b_item_cls]:
                    b_item = b_item_track.item
    
                    for b_fkey, b_value in b_item.data.items():
                        # not an item?
                        if not isinstance(b_value, ItemBase):
                            continue
                         
                        # not referenced?
                        if b_value.is_single_item():
                            if not (b_value is item):
                                continue
                        else:
                            if item not in b_value.bulk:
                                continue
                        
                        # updating b_fkey
                        update_fkey(b_item_track, b_fkey, item_track)
        
        return creator_keeper, getter_keeper