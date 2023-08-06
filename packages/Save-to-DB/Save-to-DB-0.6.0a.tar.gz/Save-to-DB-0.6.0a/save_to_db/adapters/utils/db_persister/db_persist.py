from save_to_db.core import signals
from .model_updater import ModelUpdater
from .match_items_to_models import match_items_to_models


def db_persist(db_adapter, item):
    top_item = item
    result_items = item.as_list()
    
    # emitting `before_db_persist` signal
    item_structure = item.process()
    signals.before_db_persist.emit(top_item, item_structure)
    
    # creating model updater
    model_updater = ModelUpdater(item_structure, db_adapter)
    process_keeper = model_updater.process_keeper
    
    # --- getting and updating initial models ---
    getter_process_keeper = process_keeper
    while not getter_process_keeper.is_empty():
        all_items, all_models = [], []
        for item_cls in getter_process_keeper:
            if item_cls.fast_insert or not getter_process_keeper[item_cls]:
                continue
            
            items_and_fkeys = []
            new_items, new_models = [], []
            
            for item_track in getter_process_keeper[item_cls]:
                items_and_fkeys.append([item_track.item,
                                        item_track.fkeys])
            
            batch_size = item_cls.batch_size \
                if item_cls.batch_size is not None \
                else db_adapter.BATCH_SIZE
            got_models = []
            for batch_start in range(0, len(items_and_fkeys), batch_size):
                got_models.extend(
                    db_adapter.get(
                        items_and_fkeys[batch_start:batch_start+batch_size]
                    )
                )
            if not got_models:
                continue
            got_items, got_models = match_items_to_models(db_adapter,
                                                          items_and_fkeys,
                                                          got_models)
            all_items.extend(got_items)
            all_models.extend(got_models)
        
        getter_process_keeper = model_updater.update_relationships(
            all_items, all_models)[1]
    
    for item_cls in process_keeper:
        for item_track in process_keeper[item_cls]:
            item = item_track.item
            models = item_track.models
            for model in models:
                item.before_model_update(model)  # hook
                
                # cleaning x-to-many relations if needed
                for fkey in item_cls.relations:
                    relation = item_cls.relations[fkey]
                    if not relation['relation_type'].is_x_to_many() or \
                            not relation['replace_x_to_many'] or \
                            fkey not in item:
                        continue
                    if not model_updater.can_set_model_field(
                            item, model, fkey, None):
                        continue
                    model_updater.clear_related_models(item, model, fkey)
                
                model_updater.update_model_fields(item_track, model)
                
    # --- creation loop ---
    create_process_keeper = process_keeper
    while not create_process_keeper.is_empty():
        new_items, new_models = [], []
        for item_cls in create_process_keeper:
            for item_track in create_process_keeper[item_cls]:
                if item_track.models:
                    continue
                item = item_track.item
                if item not in new_items and \
                        model_updater.can_create_model(item, item_track.fkeys):
                    new_items.append(item)
                    model = db_adapter.create_blank_model(item.model_cls)
                    model_updater.add_created_model(model)
                    new_models.append([model])
                    item.before_model_update(model)  # hook
                    model_updater.update_model_fields(item_track, model)

        create_process_keeper = model_updater.update_relationships(
            new_items, new_models)[0]
    
    # emitting `item_dropped` signal
    for item_cls in process_keeper:
        for item_track in process_keeper[item_cls]:
            if item_track.models:
                continue
            item = item_track.item
            if item.get_only_mode:
                reason = \
                    signals.item_dropped.reason_cannot_create_get_only_mode
            elif item.update_only_mode:
                reason = \
                    signals.item_dropped.reason_cannot_create_update_only_mode
            else:
                reason = \
                    signals.item_dropped.reason_cannot_create_not_enough_data
            
            signals.item_dropped.emit(item, reason)
    
    # saving models
    for item_cls in process_keeper:
        for item_track in process_keeper[item_cls]:
            item = item_track.item
            for model in item_track.models:
                db_adapter.save_model(model)
                
                if item_cls.metadata['model_deleter'] is not None:
                    item_cls.metadata['model_deleter'].collect_model(model)
                
    # executing model unrefs
    for item_cls in process_keeper:
        for item_track in process_keeper[item_cls]:
            item = item_track.item
            for fkey, model_deleter in item.metadata['model_unrefs'].items():
                for parent_model in item_track.models:
                    model_deleter.execute_unref(parent_model, fkey, db_adapter)
    
    # `after_model_save` hook
    for item_cls in process_keeper:
        for item_track in process_keeper[item_cls]:
            item = item_track.item
            for model in item_track.models:
                item.after_model_save(model)
    
    # creating result
    items, models = [], []
    for item in result_items:
        # looking for models
        for item_track in process_keeper[type(item)]:
            if item is item_track.item:
                if item_track.models:
                    items.append(item_track.item)
                    models.append(item_track.models)
                break
    
    # emitting `after_db_persist` signal
    signals.after_db_persist.emit(top_item, items, models)
    
    # executing model deleters
    for item_cls in item_structure:
        if item_cls.deleter_execute_on_persist and \
                item_cls.metadata['model_deleter']:
            item_cls.metadata['model_deleter'].execute_delete(db_adapter)
    
    return items, models

