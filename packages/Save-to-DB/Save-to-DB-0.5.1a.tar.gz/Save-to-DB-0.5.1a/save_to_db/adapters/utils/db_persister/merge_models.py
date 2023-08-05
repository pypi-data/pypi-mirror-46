from save_to_db.core.exceptions import CannotMergeModels


def merge_models(db_adapter, item, models):
    if not models:
        return None
    if len(models) == 1:
        return models[0]
    
    # sorting models to always get the same result after merging
    models = list(models)
    pk_list = list(db_adapter.get_primary_key_names(type(models[0])))
    pk_list.sort()
    get_model_key = lambda model: tuple(getattr(model, field)
                                        for field in pk_list)
    models.sort(key=get_model_key)
    all_models = models
    
    # `before_models_merge` hook
    item.before_models_merge(all_models)
    
    # first model is the resulting model
    result_model, *models = models
    
    # checking for x-to-one relations
    for fkey, relation in item.relations.items():
        if not relation['relation_type'].is_x_to_one():
            continue
        
        f_models = [getattr(model, fkey) for model in all_models
                                          if hasattr(model, fkey) and
                                             getattr(model, fkey) is not None]
        if not f_models:
            continue
        
        # making sure models are all the same
        f_model = f_models[0]
        for cur_f_model in f_models[1:]:
            if cur_f_model != f_model:
                raise CannotMergeModels(item, f_model, cur_f_model)
        
        # saving f_model
        setattr(result_model, fkey, f_model)
    
    # combining x-to-many models
    for fkey, relation in item.relations.items():
        if not relation['relation_type'].is_x_to_many():
            continue
        
        for model in models:
            f_models = db_adapter.get_related_x_to_many(model, fkey)
            db_adapter.add_related_models(result_model, fkey, f_models)
    
    # grabbing plain values from other models
    for key in item.fields:
        if hasattr(result_model, key) and \
                getattr(result_model, key) is not None:
            continue
        # looking for first value to grab
        for model in models:
            if hasattr(model, key) and getattr(model, key) is not None:
                setattr(result_model, key, getattr(model, key))
                break
    
    # deleting all merged models
    for model in models:
        db_adapter.delete(model)
    
    # `before_models_merge` hook
    item.after_models_merge(result_model)
    
    return result_model
    