from save_to_db.exceptions import CannotMergeModels, MergeModelsNotAllowed
from .relation_type import RelationType


def __one_to_many_merge(db_adapter,
                        result_model, other_model,
                        result_children, other_children,
                        fkey, reverse_key,
                        merge_function, ignore_fields):
    if not result_children or not other_children or not reverse_key:
        return other_children  # no merging needed
    
    # getting unique constraints
    f_model_cls = type(result_children[0])
    unique_constraints = db_adapter.iter_unique_field_combinations(
        f_model_cls)

    unique_constraints = [
        set(field_names)
            for field_names in unique_constraints
            if reverse_key in field_names
    ]
    if not unique_constraints:
        return other_children  # no broken constraints
    
    # looking for conflicting constraints
    def grab_model_values(model, field_names):
        return [
            getattr(model, field_name)
                    if hasattr(model, field_name)
                    else None
                for field_name in field_names
                # parent is supposed to be the same
                if field_name != reverse_key and field_name not in ignore_fields
        ]
    
    for result_i, result_child in enumerate(result_children):
        
        for other_child in other_children[:]:
            broken_constraints = []
            for constraint in unique_constraints:
                outer_values = grab_model_values(result_child, constraint)
                inner_values = grab_model_values(other_child, constraint)
                if outer_values and outer_values == inner_values:
                    broken_constraints.append(constraint)
                    other_children.remove(other_child)
        
            if broken_constraints:
                if merge_function is False:
                    raise MergeModelsNotAllowed(result_model, other_model,
                                                fkey)
                
                new_model = merge_function(result_model, other_model,
                                           result_child, other_child,
                                           fkey, reverse_key,
                                           broken_constraints)
                
                result_children[result_i] = new_model
            
    return other_children


def merge_models(db_adapter, models, merge_policy=None, ignore_fields=None):
    """ See
    :py:meth:`~save_to_db.adapters.utils.adapter_base.AdapterBase.merge_models`
    method of
    :py:class:`~save_to_db.adapters.utils.adapter_base.AdapterBase` class.
    """
    if not models:
        return None
    if len(models) == 1:
        return models[0]
    
    ignore_fields = ignore_fields or []
    all_models = models
    
    # first model is the resulting model
    result_model, *models = all_models
    
    merge_policy = merge_policy or {}
    merge_cls_policy = merge_policy.get(type(result_model), {})
    
    model_cls = type(result_model)
    relations = [
        [fkey, direction, reverse_fkey]
        for fkey, _, direction, reverse_fkey
        in db_adapter.iter_relations(model_cls)
    ]
    fields = [key for key, _ in db_adapter.iter_fields(model_cls)]
    
    # checking for x-to-one relations
    for fkey, direction, reverse_key in relations:
        if fkey in ignore_fields or not direction.is_x_to_one():
            continue

        model_and_fmodels = [
            [model, getattr(model, fkey, None)] for model in all_models
        ]
        
        # making sure models are all the same
        this_model, this_child_model = model_and_fmodels[0]
        result_child_model = this_child_model
        for merged_model, child_merged_model in model_and_fmodels[1:]:
            if child_merged_model is None:
                continue
            if result_child_model is None:
                result_child_model = child_merged_model
                # resetting reverse_key if needed
                if reverse_key and direction is RelationType.ONE_TO_ONE and \
                        hasattr(child_merged_model, reverse_key) and \
                        getattr(child_merged_model, reverse_key) != result_model:
                    setattr(child_merged_model, reverse_key, None)
                    db_adapter.save_model(child_merged_model)
                continue

            if child_merged_model != this_child_model:
                if fkey in merge_cls_policy:
                    merge_function = merge_cls_policy[fkey]
                    if merge_function is False:
                        raise MergeModelsNotAllowed(this_model, merged_model,
                                                    fkey)
                    
                    result_child_model = merge_function(
                        this_model, merged_model,
                        result_child_model, child_merged_model,
                        fkey, reverse_key)
                else:
                    raise CannotMergeModels(fkey,
                                            this_model, this_child_model,
                                            merged_model, child_merged_model)
            
        # saving f_model
        setattr(result_model, fkey, result_child_model)
            

    # combining x-to-many models
    for fkey, direction, reverse_key in relations:
        if fkey in ignore_fields or not direction.is_x_to_many():
            continue
        
        result_children = None
        for other_model in models:
            other_children = list(db_adapter.get_related_x_to_many(other_model,
                                                                   fkey))
            
            if other_children and direction is RelationType.ONE_TO_MANY and \
                    fkey in merge_cls_policy:

                if result_children is None:
                    result_children = list(
                        db_adapter.get_related_x_to_many(result_model, fkey))
                if result_children:
                    merge_function = merge_cls_policy[fkey]
                    __one_to_many_merge(db_adapter,
                                        result_model, other_model,
                                        result_children, other_children,
                                        fkey, reverse_key,
                                        merge_function,
                                        ignore_fields=ignore_fields)

            db_adapter.add_related_models(result_model, fkey, other_children)

            
    
    # grabbing plain values from other models
    for key in fields:
        if key in ignore_fields or hasattr(result_model, key) and \
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
    
    return result_model