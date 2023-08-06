from save_to_db.exceptions import CannotMergeModels, MultipleModelsMatch
from save_to_db.core.item import Item
from save_to_db.utils.test_base import TestBase



class TestResolveModel(TestBase):
    
    ModelGeneralOne = None
    ModelGeneralTwo = None
    
    def setUp(self):
        super().setUp()
        self.item_cls_manager.clear()
        
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = [{'f_integer'}]
            getters = [{'f_integer'}, {'f_float', 'f_text'}]
        self.ItemGeneralOne = ItemGeneralOne
        
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
            creators = [{'f_integer'}]
            getters = [{'f_integer'}, {'f_float', 'f_text'}]
        self.ItemGeneralTwo = ItemGeneralTwo
        
        persister = self.persister
        
        bulk = ItemGeneralOne.Bulk()
        bulk.gen(f_integer='1', f_float='1.1', f_text='text-1')
        bulk.gen(f_integer='2', f_float='1.1', f_text='text-2')
        persister.persist(bulk)
        
        item = ItemGeneralOne(f_integer='2', f_text='text-1')
        persister.persist(item)
        
        with self.assertRaises(MultipleModelsMatch):
            item = ItemGeneralOne(f_integer='2', f_float='1.1', f_text='text-1')
            persister.persist(item)
            
        models = self.get_all_models(self.ModelGeneralOne)
        self.assertEqual(len(models), 2)
    
    
    def __resolve_model(self, models):
        # sorting models to always get the same result after merging
        db_adapter = self.persister.db_adapter
        models = list(models)
        pk_list = list(db_adapter.get_primary_key_names(type(models[0])))
        pk_list.sort()
        get_model_key = lambda model: tuple(getattr(model, field)
                                            for field in pk_list)
        models.sort(key=get_model_key)
        
        result_model = db_adapter.merge_models(models)
        
        return result_model
    
    
    def test_merging_plain_fields(self):
        self.ItemGeneralOne.resolve_model = self.__resolve_model
        
        bulk = self.ItemGeneralOne.Bulk()
        bulk.gen(f_integer='1', f_string='string-1')
        bulk.gen(f_integer='2', f_boolean=True, f_date='2010-10-10')
        self.persister.persist(bulk)
        
        models = self.get_all_models(self.ModelGeneralOne)
        self.assertEqual(len(models), 2)
        
        item = self.ItemGeneralOne(f_integer='2',
                                   f_float='1.1', f_text='text-1',
                                   f_date='2010-10-20',
                                   f_time='10:20:30')
        items, model_lists = self.persister.persist(item)
        self.assertEqual(len(items), 1)
        self.assertEqual(len(model_lists), 1)
        self.assertEqual(len(model_lists[0]), 1)
        
        models = self.get_all_models(self.ModelGeneralOne)
        self.assertEqual(len(models), 1)  # second model was deleted
        
        model = models[0]
        # old values
        self.assertEqual(model.f_integer, 2)
        self.assertEqual(model.f_float, 1.1)
        self.assertEqual(model.f_text, 'text-1')
        # values from different models merged
        self.assertEqual(model.f_string, 'string-1')
        self.assertEqual(model.f_boolean, True)
        # values from item
        # (model value overwritten with item value)
        self.assertEqual(model.f_date.strftime('%Y-%m-%d'), '2010-10-20')
        # (new value from item)
        self.assertEqual(model.f_time.strftime('%H:%M:%S'), '10:20:30')
    
    
    def test_merging_x_to_many(self):
        persister = self.persister
        self.ItemGeneralOne.resolve_model = self.__resolve_model
        sort_func = lambda model: model.f_integer
        
        item_two_1 = self.ItemGeneralTwo(f_integer=1, f_string='two-1')
        item_two_2 = self.ItemGeneralTwo(f_integer=2, f_string='two-2')
        item_two_3 = self.ItemGeneralTwo(f_integer=3, f_string='two-3')
        item_two_4 = self.ItemGeneralTwo(f_integer=4, f_string='two-4')
        item_two_5 = self.ItemGeneralTwo(f_integer=5, f_string='two-5')
        item_two_6 = self.ItemGeneralTwo(f_integer=6, f_string='two-6')
        item_two_7 = self.ItemGeneralTwo(f_integer=7,
                                         f_string='two-7 (in item)')
        item_two_8 = self.ItemGeneralTwo(f_integer=8,
                                         f_string='two-8 (in item)')
        
        bulk = self.ItemGeneralOne.Bulk()
        item_one_1 = bulk.gen(f_integer='1')
        item_one_2 = bulk.gen(f_integer='2')
        
        # one-to-many
        item_one_1['two_1_x'].add(item_two_1, item_two_2)
        item_one_2['two_1_x'].add(item_two_3)
        
        # many-to-many
        item_one_1['two_x_x'].add(item_two_4, item_two_5)
        item_one_2['two_x_x'].add(item_two_5, item_two_6)
        
        persister.persist(bulk)
        
        models = self.get_all_models(self.ModelGeneralOne, sort_key=sort_func)
        self.assertEqual(len(models), 2)
        
        model_one_1, model_one_2 = models
        self.assertEqual(model_one_1.f_integer, 1)
        self.assertEqual(model_one_2.f_integer, 2)
        
        one_1_two_1_x = self.get_related_x_to_many(model_one_1, 'two_1_x',
                                                   sort_key=sort_func)
        one_1_two_x_x = self.get_related_x_to_many(model_one_1, 'two_x_x',
                                                   sort_key=sort_func)
        one_2_two_1_x = self.get_related_x_to_many(model_one_2, 'two_1_x',
                                                 sort_key=sort_func)
        one_2_two_x_x = self.get_related_x_to_many(model_one_2, 'two_x_x',
                                                   sort_key=sort_func)
        
        self.assertEqual(len(one_1_two_1_x), 2)
        self.assertEqual(one_1_two_1_x[0].f_integer, 1)
        self.assertEqual(one_1_two_1_x[1].f_integer, 2)
        
        self.assertEqual(len(one_2_two_1_x), 1)
        self.assertEqual(one_2_two_1_x[0].f_integer, 3)
        
        self.assertEqual(len(one_1_two_x_x), 2)
        self.assertEqual(one_1_two_x_x[0].f_integer, 4)
        self.assertEqual(one_1_two_x_x[1].f_integer, 5)
        
        self.assertEqual(len(one_2_two_x_x), 2)
        self.assertEqual(one_2_two_x_x[0].f_integer, 5)
        self.assertEqual(one_2_two_x_x[1].f_integer, 6)
        
        item = self.ItemGeneralOne(f_integer='2',
                                   f_float='1.1', f_text='text-1',
                                   two_1_x=[item_two_7],
                                   two_x_x=[item_two_8])
        items, model_lists = persister.persist(item)
        self.assertEqual(len(items), 1)
        self.assertEqual(len(model_lists), 1)
        self.assertEqual(len(model_lists[0]), 1)
        
        # now checking that all was merged correctly
        models = self.get_all_models(self.ModelGeneralOne)
        self.assertEqual(len(models), 1)  # second model was deleted
        
        model = models[0]
        self.assertEqual(model.f_integer, 2)
        self.assertEqual(model.f_float, 1.1)
        self.assertEqual(model.f_text, 'text-1')
        two_1_x = self.get_related_x_to_many(model, 'two_1_x',
                                             sort_key=sort_func)
        two_x_x = self.get_related_x_to_many(model, 'two_x_x',
                                             sort_key=sort_func)
        self.assertEqual(len(two_1_x), 4)
        self.assertEqual(two_1_x[0].f_integer, 1)
        self.assertEqual(two_1_x[1].f_integer, 2)
        self.assertEqual(two_1_x[2].f_integer, 3)
        self.assertEqual(two_1_x[3].f_integer, 7)  # from item
        
        self.assertEqual(len(two_x_x), 4)
        self.assertEqual(two_x_x[0].f_integer, 4)
        self.assertEqual(two_x_x[1].f_integer, 5)
        self.assertEqual(two_x_x[2].f_integer, 6)
        self.assertEqual(two_x_x[3].f_integer, 8)  # from item
    

    def test_merging_x_to_one(self):
        self.ItemGeneralOne.resolve_model = self.__resolve_model
        sort_func = lambda model: model.f_integer
        
        item_two_1 = self.ItemGeneralTwo(f_integer=1, f_string='two-1')
        item_two_2 = self.ItemGeneralTwo(f_integer=2, f_string='two-2')
        
        bulk = self.ItemGeneralOne.Bulk()
        item_one_1 = bulk.gen(f_integer='1')
        item_one_2 = bulk.gen(f_integer='2')
        
        # same reference
        item_one_1['two_x_1'] = item_two_1
        item_one_2['two_x_1'] = item_two_1
        
        # one reference
        item_one_1['two_1_1'] = item_two_2
        
        self.persister.persist(bulk)
        models = self.get_all_models(self.ModelGeneralOne, sort_key=sort_func)
        self.assertEqual(len(models), 2)
        
        self.assertEqual(models[0].two_x_1.f_integer, 1)
        self.assertEqual(models[1].two_x_1.f_integer, 1)
        
        self.assertEqual(models[0].two_1_1.f_integer, 2)
        
        # merging models
        item = self.ItemGeneralOne(f_integer='2',
                                   f_float='1.1', f_text='text-1')
        items, model_lists = self.persister.persist(item)

        self.assertEqual(len(items), 1)
        self.assertEqual(len(model_lists), 1)
        self.assertEqual(len(model_lists[0]), 1)
        
        models = self.get_all_models(self.ModelGeneralOne)
        self.assertEqual(len(models), 1)
        self.assertEqual(models[0].two_x_1.f_integer, 1)
        self.assertEqual(models[0].two_1_1.f_integer, 2)
        
    
    def test_merging_x_to_one_overwrite(self):
        persister = self.persister
        self.ItemGeneralOne.resolve_model = self.__resolve_model
        sort_func = lambda model: model.f_integer
        
        item_two_1 = self.ItemGeneralTwo(f_integer=1, f_string='two-1')
        item_two_2 = self.ItemGeneralTwo(f_integer=2, f_string='two-2')
        item_two_3 = self.ItemGeneralTwo(f_integer=3,
                                         f_string='two-3 (in item)')
        item_two_4 = self.ItemGeneralTwo(f_integer=4,
                                         f_string='two-4 (in item)')
        
        bulk = self.ItemGeneralOne.Bulk()
        item_one_1 = bulk.gen(f_integer='1')
        item_one_2 = bulk.gen(f_integer='2')
        
        # same reference
        item_one_1['two_x_1'] = item_two_1
        item_one_2['two_x_1'] = item_two_1
        
        # one reference
        item_one_1['two_1_1'] = item_two_2
        
        persister.persist(bulk)
        models = self.get_all_models(self.ModelGeneralOne, sort_key=sort_func)
        self.assertEqual(len(models), 2)
        
        self.assertEqual(models[0].two_x_1.f_integer, 1)
        self.assertEqual(models[1].two_x_1.f_integer, 1)
        
        self.assertEqual(models[0].two_1_1.f_integer, 2)
        
        # merging models
        item = self.ItemGeneralOne(f_integer='2',
                                   f_float='1.1', f_text='text-1',
                                   two_x_1=item_two_3, two_1_1=item_two_4)
        items, model_lists = persister.persist(item)
        self.assertEqual(len(items), 1)
        self.assertEqual(len(model_lists), 1)
        self.assertEqual(len(model_lists[0]), 1)
        
        models = self.get_all_models(self.ModelGeneralOne)
        self.assertEqual(len(models), 1)
        self.assertEqual(models[0].two_x_1.f_integer, 3)
        self.assertEqual(models[0].two_1_1.f_integer, 4)
        
        
    def test_merging_many_to_one_exception(self):
        persister = self.persister
        self.ItemGeneralOne.resolve_model = self.__resolve_model
        sort_func = lambda model: model.f_integer
        
        item_two_1 = self.ItemGeneralTwo(f_integer=1, f_string='two-1')
        item_two_2 = self.ItemGeneralTwo(f_integer=2, f_string='two-2')
        
        bulk = self.ItemGeneralOne.Bulk()
        bulk.gen(f_integer='1', two_x_1=item_two_1)
        bulk.gen(f_integer='2', two_x_1=item_two_2)
    
        persister.persist(bulk)
        
        models = self.get_all_models(self.ModelGeneralOne, sort_key=sort_func)
        self.assertEqual(len(models), 2)
        self.assertEqual(models[0].two_x_1.f_integer, 1)
        self.assertEqual(models[1].two_x_1.f_integer, 2)
        
        # merging models
        item = self.ItemGeneralOne(f_integer='2',
                                   f_float='1.1', f_text='text-1')
        
        with self.assertRaises(CannotMergeModels):
            persister.persist(item)
            
            
    def test_merging_one_to_one_exception(self):
        persister = self.persister
        self.ItemGeneralOne.resolve_model = self.__resolve_model
        sort_func = lambda model: model.f_integer
        
        item_two_1 = self.ItemGeneralTwo(f_integer=1, f_string='two-1')
        item_two_2 = self.ItemGeneralTwo(f_integer=2, f_string='two-2')
        
        bulk = self.ItemGeneralOne.Bulk()
        bulk.gen(f_integer='1', two_1_1=item_two_1)
        bulk.gen(f_integer='2', two_1_1=item_two_2)
    
        persister.persist(bulk)
        
        models = self.get_all_models(self.ModelGeneralOne, sort_key=sort_func)
        self.assertEqual(len(models), 2)
        self.assertEqual(models[0].two_1_1.f_integer, 1)
        self.assertEqual(models[1].two_1_1.f_integer, 2)
        
        # merging models
        item = self.ItemGeneralOne(f_integer='2',
                                   f_float='1.1', f_text='text-1')
        
        with self.assertRaises(CannotMergeModels):
            persister.persist(item)
    
    
    def test_allow_multi_update_true(self):
        persister = self.persister
        self.ItemGeneralOne.resolve_model = self.__resolve_model
        self.ItemGeneralOne.allow_multi_update = True
        sort_func = lambda model: model.f_integer
        
        item_two_1 = self.ItemGeneralTwo(f_integer=1, f_string='two-1')
        item_two_2 = self.ItemGeneralTwo(f_integer=2, f_string='two-2')
        
        bulk = self.ItemGeneralOne.Bulk()
        bulk.gen(f_integer='1', two_x_x=[item_two_1])
        bulk.gen(f_integer='2', two_x_x=[item_two_2])
    
        persister.persist(bulk)
        
        models = self.get_all_models(self.ModelGeneralOne, sort_key=sort_func)
        self.assertEqual(len(models), 2)
        
        self.assertEqual(models[0].f_boolean, None)
        self.assertEqual(models[1].f_boolean, None)
        
        two_x_x_1 = self.get_related_x_to_many(models[0], 'two_x_x')
        two_x_x_2 = self.get_related_x_to_many(models[1], 'two_x_x')
        
        self.assertEqual(len(two_x_x_1), 1)
        self.assertEqual(len(two_x_x_2), 1)
        
        self.assertEqual(two_x_x_1[0].f_integer, 1)
        self.assertEqual(two_x_x_2[0].f_integer, 2)
        
        # no merging models
        item = self.ItemGeneralOne(f_integer='2',
                                   f_float='1.1', f_text='text-1',
                                   f_boolean=True)
        
        persister.persist(item)
        
        models = self.get_all_models(self.ModelGeneralOne, sort_key=sort_func)
        self.assertEqual(len(models), 2)  # still two items
        
        # `f_boolean` updated for both models
        self.assertEqual(models[0].f_boolean, True)
        self.assertEqual(models[1].f_boolean, True)
        
        # but the rest stays the same
        two_x_x_1 = self.get_related_x_to_many(models[0], 'two_x_x')
        two_x_x_2 = self.get_related_x_to_many(models[1], 'two_x_x')
        
        self.assertEqual(len(two_x_x_1), 1)
        self.assertEqual(len(two_x_x_2), 1)
        
        self.assertEqual(two_x_x_1[0].f_integer, 1)
        self.assertEqual(two_x_x_2[0].f_integer, 2)
        
        