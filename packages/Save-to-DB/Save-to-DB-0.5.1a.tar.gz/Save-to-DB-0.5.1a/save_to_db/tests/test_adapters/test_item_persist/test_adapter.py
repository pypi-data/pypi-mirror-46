from save_to_db.core.item import Item
from save_to_db.utils.test_base import TestBase



class TestAdapter(TestBase):
    
    ModelGeneralOne = None
    ModelGeneralTwo = None
    
    
    def test_multiple_same_models_returned(self):
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = ['f_integer']
            getters = ['two_x_x', 'f_string']
        
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
            creators = ['f_integer']
            getters = ['f_string']
        
        persister = self.persister
        
        item_one = ItemGeneralOne(f_integer='1', f_string='str-1')
        item_two_1 = ItemGeneralTwo(f_integer='2', f_string='str-2')
        item_two_2 = ItemGeneralTwo(f_integer='3', f_string='str-3')
        # through x-to-many relation same model can be loaded twice
        item_one['two_x_x'].add(item_two_1, item_two_2)
        
        def ensure_saved_models():
            models_one = self.get_all_models(self.ModelGeneralOne)
            models_two = self.get_all_models(self.ModelGeneralTwo,
                                             sort_key=lambda x: x.f_integer)
            self.assertEqual(len(models_one), 1)
            self.assertEqual(len(models_two), 2)
            model_one = self.get_all_models(self.ModelGeneralOne)[0]
            model_two_1 = self.get_all_models(self.ModelGeneralTwo)[0]
            model_two_2 = self.get_all_models(self.ModelGeneralTwo)[1]
            
            self.assertEqual(model_one.f_integer, 1)
            self.assertEqual(model_one.f_string, 'str-1')
            related_two = self.get_related_x_to_many(model_one, 'two_x_x')
            related_two.sort(key=lambda x: x.f_integer)
            self.assertEqual(len(related_two), 2)
            self.assertEqual(model_two_1, related_two[0])
            self.assertEqual(model_two_2, related_two[1])
            
            self.assertEqual(model_two_1.f_integer, 2)
            self.assertEqual(model_two_1.f_string, 'str-2')
            related_one = self.get_related_x_to_many(model_two_1,
                                                            'one_x_x')
            self.assertEqual(len(related_one), 1)
            self.assertEqual(model_one, related_one[0])
            
            self.assertEqual(model_two_2.f_integer, 3)
            self.assertEqual(model_two_2.f_string, 'str-3')
            related_one = self.get_related_x_to_many(model_two_2, 'one_x_x')
            self.assertEqual(len(related_one), 1)
            self.assertEqual(model_one, related_one[0])
        
        persister.persist(item_one)
        ensure_saved_models()
        
        # saving models second time might cause same model to be returned
        # for ['two_x_x', 'f_string'] getters
        persister.persist(item_one)
        ensure_saved_models()
    
    
    def test_no_item_returned_with_fkey(self):
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = [['f_integer', 'two_1_1']]
            getters = [['f_integer', 'two_1_1']]
        
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
            creators = ['f_integer']
            getters = ['f_integer']
            
        persister = self.persister
        db_adapter = persister.db_adapter
        
        item_one = ItemGeneralOne(f_integer=1)
        item_one['two_1_1'](f_integer=2)
        
        persister.persist(item_one)
        models_one = self.get_all_models(self.ModelGeneralOne)
        self.assertEqual(len(models_one), 1)
        model_one = models_one[0]
        self.assertEqual(model_one.f_integer, 1)
        self.assertIsNotNone(model_one.two_1_1)
        self.assertEqual(model_one.two_1_1.f_integer, 2)
        
        item_one = ItemGeneralOne(f_integer=1)
        item_one['two_1_1'](f_integer=2)
        items_and_fkeys = [[item_one, {}],]
        got_models = db_adapter.get(items_and_fkeys)
        self.assertFalse(bool(got_models),
                         'Adapter returned models that have relations in '
                         'getter when empty `fkey`. Probably adapter '
                         'just returned all models from DB.')
    
    
    def test_related_x_to_many_contains(self):
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = ['f_integer']
            getters = ['f_integer']
        
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
            creators = ['f_integer']
            getters = ['f_integer']
        
        persister = self.persister
        db_adapter = persister.db_adapter
        
        for f_key in ['two_1_x', 'two_x_x']:
            item_one_1 = ItemGeneralOne(f_integer='1000')
            item_one_1[f_key].gen(f_integer='1001')
            item_one_1[f_key].gen(f_integer='1002')
            
            item_one_2 = ItemGeneralOne(f_integer='2000')
            item_one_2[f_key].gen(f_integer='2001')
            item_one_2[f_key].gen(f_integer='2002')
            
            persister.persist(item_one_1)
            persister.persist(item_one_2)
            
            sort_func = lambda model: model.f_integer
            
            model_ones = self.get_all_models(self.ModelGeneralOne,
                                             sort_key=sort_func)
            self.assertEqual(len(model_ones), 2)
            model_one_1000, model_one_2000 = model_ones
            
            models_two_1 = self.get_related_x_to_many(model_one_1000, f_key)
            self.assertEqual(len(models_two_1), 2)
            model_two_1001, model_two_1002 = models_two_1
            
            models_two_2 = self.get_related_x_to_many(model_one_2000, f_key)
            self.assertEqual(len(models_two_2), 2)
            model_two_2001, model_two_2002 = models_two_2
            
            self.assertEqual(model_one_1000.f_integer, 1000)
            self.assertEqual(model_one_2000.f_integer, 2000)
            self.assertEqual(model_two_1001.f_integer, 1001)
            self.assertEqual(model_two_1002.f_integer, 1002)
            self.assertEqual(model_two_2001.f_integer, 2001)
            self.assertEqual(model_two_2002.f_integer, 2002)
            
            # the testing
            models_two = db_adapter.related_x_to_many_contains(
                model_one_1000, f_key, [model_two_1001, model_two_1002,
                                        model_two_2001, model_two_2002])
            self.assertEqual(len(models_two), 2)
            models_two.sort(key=sort_func)
            self.assertEqual(models_two[0].f_integer, 1001)
            self.assertEqual(models_two[1].f_integer, 1002)
            # exectly the same models returned
            self.assertIs(model_two_1001, models_two[0])
            self.assertIs(model_two_1002, models_two[1])
            
            models_two = db_adapter.related_x_to_many_contains(
                model_one_1000, f_key, [model_two_1001, model_two_2002])
            self.assertEqual(len(models_two), 1)
            self.assertEqual(models_two[0].f_integer, 1001)
            self.assertIs(model_two_1001, models_two[0])
            
            models_two = db_adapter.related_x_to_many_contains(
                model_one_1000, f_key, [model_two_2001, model_two_2002])
            self.assertEqual(len(models_two), 0)
            
            models_two = db_adapter.related_x_to_many_contains(
                model_one_1000, f_key, [])
            self.assertEqual(len(models_two), 0)
    