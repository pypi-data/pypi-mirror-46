from save_to_db.core.item import Item
from save_to_db.utils.test_base import TestBase



class TestNorewrite(TestBase):
    
    ModelGeneralOne = None
    ModelGeneralTwo = None
    
    
    def test_norewrite_fields(self):
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = [{'f_integer'}]
            getters = [{'f_integer'}]
            norewrite_fields = {
                'f_text': True,
                'f_string': False,
            }
         
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
            creators = [{'f_integer'}]
            getters = [{'f_integer'}]
            

        persister = self.persister
         
        #--- normal fields ---
        # all fields set
        item_one = ItemGeneralOne(f_integer=1,
                                  f_text='text-1',
                                  f_string='string-1',
                                  f_float=1.0)
        _, model_ones_list = persister.persist(item_one)
        self.assertEqual(len(model_ones_list), 1)
        self.assertEqual(len(model_ones_list[0]), 1)
        model_one = model_ones_list[0][0]
          
        # model did not exist, everything was set
        self.assertEqual(model_one.f_integer, 1)
        self.assertEqual(model_one.f_text, 'text-1')
        self.assertEqual(model_one.f_string, 'string-1')
        self.assertEqual(model_one.f_float, 1.0)
          
        item_one = ItemGeneralOne(f_integer=1,
                                  f_text='text-2',
                                  f_string='string-2',
                                  f_float=2.0)
        _, model_ones_list = persister.persist(item_one)
        self.assertEqual(len(model_ones_list), 1)
        self.assertEqual(len(model_ones_list[0]), 1)
        model_one = model_ones_list[0][0]
          
        # only field that can be rewritten changed
        self.assertEqual(model_one.f_integer, 1)
        self.assertEqual(model_one.f_text, 'text-1')
        self.assertEqual(model_one.f_string, 'string-1')
        self.assertEqual(model_one.f_float, 2.0)  # changed
          
        # model did not exist, fields from norewrite are not set
        item_one = ItemGeneralOne(f_integer=2,
                                  f_float=2.0)
        _, model_ones_list = persister.persist(item_one)
        self.assertEqual(len(model_ones_list), 1)
        self.assertEqual(len(model_ones_list[0]), 1)
        model_one = model_ones_list[0][0]
         
        # model did not exist, everything that item had was set
        self.assertEqual(model_one.f_integer, 2)
        self.assertEqual(model_one.f_text, None)
        self.assertEqual(model_one.f_string, None)
        self.assertEqual(model_one.f_float, 2.0)
         
        item_one = ItemGeneralOne(f_integer=2,
                                  f_text='text-2',
                                  f_string='string-2',
                                  f_float=3.0)
        _, model_ones_list = persister.persist(item_one)
        self.assertEqual(len(model_ones_list), 1)
        self.assertEqual(len(model_ones_list[0]), 1)
        model_one = model_ones_list[0][0]
         
        # only field that can be rewritten changed
        self.assertEqual(model_one.f_integer, 2)
        self.assertEqual(model_one.f_text, 'text-2')
        self.assertEqual(model_one.f_string, None)  # cannot overwrite
        self.assertEqual(model_one.f_float, 3.0)  # changed
    
    
    def test_norewrite_cannot_create_1_to_1(self):
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = [{'f_integer'}]
            getters = [{'f_integer'}]
            norewrite_fields = {
                'two_1_1': False,
            }
         
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
            creators = [{'f_integer', 'one_1_1'}]
            getters = [{'f_integer'}]
            
        persister = self.persister
        
        item_one = ItemGeneralOne(f_integer=1)
        persister.persist(item_one)
        
        # item ones' two_1_1 cannot be ovewritten, hence `item_two` cannot
        # be created
        item_two = ItemGeneralTwo(
            f_integer=2,
            one_1_1=item_one
        )
        _, model_lists = persister.persist(item_two)
        self.assertEqual(len(model_lists), 0)
        
        model_twos = self.get_all_models(self.ModelGeneralTwo)
        self.assertEqual(len(model_twos), 0)
        
        model_ones = self.get_all_models(self.ModelGeneralOne)
        self.assertEqual(len(model_ones), 1)
        model_one = model_ones[0]
        self.assertEqual(model_one.f_integer, 1)
        self.assertTrue(not hasattr(model_one, 'one_1_1') or
                        model_one.one_1_1 is None)
    
    
    def test_norewrite_nullables(self):
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = [{'f_integer'}]
            getters = [{'f_integer'}]
            norewrite_fields = {
                'two_1_1': True,
                'two_x_x': True,
            }
            nullables = ['f_text', 'two_1_1', 'two_x_x']
            relations = {
                'two_x_x': {
                    'replace_x_to_many': True,
                }
            }
         
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
            creators = [{'f_integer'}]
            getters = [{'f_integer'}]
            nullables = ['f_text', 'one_1_1', 'one_x_x']
            relations = {
                'one_x_x': {
                    'replace_x_to_many': True,
                }
            }
        
        persister = self.persister
        
        item_one = ItemGeneralOne(
            f_integer=1,
            f_text='text',
            two_1_1=ItemGeneralTwo(f_integer=2),
            two_x_x=[ItemGeneralTwo(f_integer=3)]
        )
        _, model_lists = persister.persist(item_one)
        self.assertEqual(len(model_lists), 1)
        self.assertEqual(len(model_lists[0]), 1)
        model_one = model_lists[0][0]
        self.assertEqual(model_one.f_integer, 1)
        self.assertEqual(model_one.f_text, 'text')
        self.assertEqual(model_one.two_1_1.f_integer, 2)
        two_x_x = self.get_related_x_to_many(model_one, 'two_x_x')
        self.assertEqual(len(two_x_x), 1)
        self.assertEqual(two_x_x[0].f_integer, 3)
        
        # not all fields must not be rewritten with `None`
        item_one = ItemGeneralOne(f_integer=1)
        persister.persist(item_one)
        model_ones = self.get_all_models(self.ModelGeneralOne)
        self.assertEqual(len(model_ones), 1)
        
        model_one = model_ones[0]
        self.assertEqual(model_one.f_integer, 1)
        self.assertEqual(model_one.f_text, None)  # rewritten
        self.assertEqual(model_one.two_1_1.f_integer, 2)
        two_x_x = self.get_related_x_to_many(model_one, 'two_x_x')
        self.assertEqual(len(two_x_x), 1)
        self.assertEqual(two_x_x[0].f_integer, 3)
    
    
    def test_norewrite_relations_false(self):
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = [{'f_integer'}]
            getters = [{'f_integer'}]
            norewrite_fields = {
                'two_1_1': False,
                'two_1_x': False,
                'two_x_1': False,
                'two_x_x': False,
                
            }
         
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
            creators = [{'f_integer'}]
            getters = [{'f_integer'}]
        
        persister = self.persister
        sort_func = lambda model: model.f_integer
        
        item_one = ItemGeneralOne(f_integer=1)
        persister.persist(item_one)
        model_ones = self.get_all_models(self.ModelGeneralOne, sort_func)
        self.assertEqual(len(model_ones), 1)
        self.assertEqual(model_ones[0].f_integer, 1)
        
        #--- all newly created ---
        item_one = ItemGeneralOne(
            f_integer=1,
            two_1_1=ItemGeneralTwo(f_integer=2),  # cannot rewrite
            two_1_x=[ItemGeneralTwo(f_integer=3),
                     ItemGeneralTwo(f_integer=4)],  # can rewrite
            two_x_1=ItemGeneralTwo(f_integer=5),  # cannot rewrite
            two_x_x=[ItemGeneralTwo(f_integer=6),
                     ItemGeneralTwo(f_integer=7)],  # can rewrite
        )
        _, models_list = persister.persist(item_one)
        self.assertEqual(len(models_list), 1)
        self.assertEqual(len(models_list[0]), 1)
        model_one = models_list[0][0]
        
        # no related models
        two_1_x = self.get_related_x_to_many(model_one, 'two_1_x', sort_func)
        two_x_x = self.get_related_x_to_many(model_one, 'two_x_x', sort_func)
        self.assertEqual(len(two_1_x), 2)
        self.assertEqual(len(two_x_x), 2)
        
        self.assertEqual(two_1_x[0].f_integer, 3)
        self.assertEqual(two_1_x[1].f_integer, 4)
        self.assertEqual(two_x_x[0].f_integer, 6)
        self.assertEqual(two_x_x[1].f_integer, 7)
        
        self.assertEqual(model_one.f_integer, 1)
        self.assertTrue(not hasattr(model_one, 'two_1_1') or
                        model_one.two_1_1 is None)
        self.assertTrue(not hasattr(model_one, 'two_x_1') or
                        model_one.two_x_1 is None)
        
        # but the other models were created
        models_two = self.get_all_models(self.ModelGeneralTwo, sort_func)
        expected_f_integers = [2, 3, 4, 5, 6, 7]
        f_integers = [model.f_integer for model in models_two]
        self.assertEqual(f_integers, expected_f_integers)
        
        #--- all newly created, even model_one ---
        item_one = ItemGeneralOne(
            f_integer=2,
            two_1_1=ItemGeneralTwo(f_integer=1002),
            two_1_x=[ItemGeneralTwo(f_integer=1003),
                     ItemGeneralTwo(f_integer=1004)],
            two_x_1=ItemGeneralTwo(f_integer=1005),
            two_x_x=[ItemGeneralTwo(f_integer=1006),
                     ItemGeneralTwo(f_integer=1007)],
        )
        _, models_list = persister.persist(item_one)
        self.assertEqual(len(models_list), 1)
        self.assertEqual(len(models_list[0]), 1)
        model_one = models_list[0][0]
        
        # relations were set
        two_1_x = self.get_related_x_to_many(model_one, 'two_1_x', sort_func)
        two_x_x = self.get_related_x_to_many(model_one, 'two_x_x', sort_func)
        self.assertEqual(len(two_1_x), 2)
        self.assertEqual(len(two_x_x), 2)
        
        self.assertEqual(model_one.f_integer, 2)
        self.assertEqual(model_one.two_1_1.f_integer, 1002)
        self.assertEqual(two_1_x[0].f_integer, 1003)
        self.assertEqual(two_1_x[1].f_integer, 1004)
        self.assertEqual(model_one.two_x_1.f_integer, 1005)
        self.assertEqual(two_x_x[0].f_integer, 1006)
        self.assertEqual(two_x_x[1].f_integer, 1007)
        
        #--- checking for the other side ---
        item_two = ItemGeneralTwo(f_integer=1000000)
        persister.persist(item_two)
        model_twos = self.get_all_models(self.ModelGeneralTwo, sort_func)
        self.assertEqual(model_twos[-1].f_integer, 1000000)
        
        model_ones = self.get_all_models(self.ModelGeneralOne, sort_func)
        # model one with `f_integer=1000000` does not exists
        self.assertLess(model_ones[-1].f_integer, 1000000)
        item_one = ItemGeneralOne(
            f_integer=1000000,
            two_1_1=item_two,  # cannot rewrite model_two
            two_1_x=[item_two],  # cannot rewrite model_two
            two_x_1=item_two,  # can set
            two_x_x=[item_two]  # can set
        )
        _, models_list = persister.persist(item_one)
        self.assertEqual(len(models_list), 1)
        self.assertEqual(len(models_list[0]), 1)
        model_one = models_list[0][0]
        
        two_1_x = self.get_related_x_to_many(model_one, 'two_1_x', sort_func)
        two_x_x = self.get_related_x_to_many(model_one, 'two_x_x', sort_func)
        self.assertEqual(len(two_1_x), 0)
        self.assertEqual(len(two_x_x), 1)
        self.assertEqual(two_x_x[0].f_integer, 1000000)
        
        self.assertEqual(model_one.f_integer, 1000000)
        self.assertTrue(not hasattr(model_one, 'two_1_1') or
                        model_one.two_1_1 is None)
        self.assertEqual(model_one.two_x_1.f_integer, 1000000)
    
    
    def test_norewrite_relations_true(self):
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = [{'f_integer'}]
            getters = [{'f_integer'}]
            norewrite_fields = {
                'two_1_1': True,
                'two_1_x': True,
                'two_x_1': True,
                'two_x_x': True,
                
            }
         
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
            creators = [{'f_integer'}]
            getters = [{'f_integer'}]
        
        persister = self.persister
        sort_func = lambda model: model.f_integer
        
        item_one = ItemGeneralOne(f_integer=1)
        persister.persist(item_one)
        model_ones = self.get_all_models(self.ModelGeneralOne, sort_func)
        self.assertEqual(len(model_ones), 1)
        self.assertEqual(model_ones[0].f_integer, 1)
        
        #--- all newly created that can rewrite none ---
        item_one = ItemGeneralOne(
            f_integer=1,
            two_1_1=ItemGeneralTwo(f_integer=2),
            two_1_x=[ItemGeneralTwo(f_integer=3),
                     ItemGeneralTwo(f_integer=4)],
            two_x_1=ItemGeneralTwo(f_integer=5),
            two_x_x=[ItemGeneralTwo(f_integer=6),
                     ItemGeneralTwo(f_integer=7)],
        )
        _, models_list = persister.persist(item_one)
        self.assertEqual(len(models_list), 1)
        self.assertEqual(len(models_list[0]), 1)
        model_one = models_list[0][0]
        
        two_1_x = self.get_related_x_to_many(model_one, 'two_1_x', sort_func)
        two_x_x = self.get_related_x_to_many(model_one, 'two_x_x', sort_func)
        self.assertEqual(len(two_1_x), 2)
        self.assertEqual(len(two_x_x), 2)
        
        self.assertEqual(model_one.f_integer, 1)
        self.assertEqual(model_one.two_1_1.f_integer, 2)
        self.assertEqual(two_1_x[0].f_integer, 3)
        self.assertEqual(two_1_x[1].f_integer, 4)
        self.assertEqual(model_one.two_x_1.f_integer, 5)
        self.assertEqual(two_x_x[0].f_integer, 6)
        self.assertEqual(two_x_x[1].f_integer, 7)
        
        #--- item_one already exists and has values set, ---
        #--- nothing must be rewritten when all models already exist ---
        bulk_two = ItemGeneralTwo.Bulk()
        for f_integer in range(102, 108):
            bulk_two.gen(f_integer=f_integer)
        persister.persist(bulk_two)
        
        item_one = ItemGeneralOne(
            f_integer=1,
            two_1_1=ItemGeneralTwo(f_integer=102),
            two_1_x=[ItemGeneralTwo(f_integer=103),
                     ItemGeneralTwo(f_integer=104)],
            two_x_1=ItemGeneralTwo(f_integer=105),
            two_x_x=[ItemGeneralTwo(f_integer=106),
                     ItemGeneralTwo(f_integer=107)]
        )

        _, models_list = persister.persist(item_one)
        self.assertEqual(len(models_list), 1)
        self.assertEqual(len(models_list[0]), 1)
        model_one = models_list[0][0]
        
        # nothing changed
        two_1_x = self.get_related_x_to_many(model_one, 'two_1_x', sort_func)
        two_x_x = self.get_related_x_to_many(model_one, 'two_x_x', sort_func)
        self.assertEqual(len(two_1_x), 2)
        self.assertEqual(len(two_x_x), 2)
        
        self.assertEqual(model_one.f_integer, 1)
        self.assertEqual(model_one.two_1_1.f_integer, 2)
        self.assertEqual(two_1_x[0].f_integer, 3)
        self.assertEqual(two_1_x[1].f_integer, 4)
        self.assertEqual(model_one.two_x_1.f_integer, 5)
        self.assertEqual(two_x_x[0].f_integer, 6)
        self.assertEqual(two_x_x[1].f_integer, 7)
        
        #--- existed side "many" can be added to with created models ---
        item_one = ItemGeneralOne(
            f_integer=1,
            two_1_1=ItemGeneralTwo(f_integer=202),
            two_1_x=[ItemGeneralTwo(f_integer=203),
                     ItemGeneralTwo(f_integer=204)],
            two_x_1=ItemGeneralTwo(f_integer=205),
            two_x_x=[ItemGeneralTwo(f_integer=206),
                     ItemGeneralTwo(f_integer=207)]
        )
        _, models_list = persister.persist(item_one)
        self.assertEqual(len(models_list), 1)
        self.assertEqual(len(models_list[0]), 1)
        model_one = models_list[0][0]
        
        # x-to-many were added to and x-to-1 unchanged
        two_1_x = self.get_related_x_to_many(model_one, 'two_1_x', sort_func)
        two_x_x = self.get_related_x_to_many(model_one, 'two_x_x', sort_func)
        self.assertEqual(len(two_1_x), 4)
        self.assertEqual(len(two_x_x), 4)
        
        self.assertEqual(model_one.f_integer, 1)
        self.assertEqual(model_one.two_1_1.f_integer, 2)
        self.assertEqual(two_1_x[0].f_integer, 3)
        self.assertEqual(two_1_x[1].f_integer, 4)
        self.assertEqual(two_1_x[2].f_integer, 203)
        self.assertEqual(two_1_x[3].f_integer, 204)
        self.assertEqual(model_one.two_x_1.f_integer, 5)
        self.assertEqual(two_x_x[0].f_integer, 6)
        self.assertEqual(two_x_x[1].f_integer, 7)
        self.assertEqual(two_x_x[2].f_integer, 206)
        self.assertEqual(two_x_x[3].f_integer, 207)
        
        #--- checking for the other side ---
        item_two = ItemGeneralTwo(f_integer=1000)
        persister.persist(item_two)
        model_twos = self.get_all_models(self.ModelGeneralTwo, sort_func)
        self.assertEqual(model_twos[-1].f_integer, 1000)
        
        model_ones = self.get_all_models(self.ModelGeneralOne, sort_func)
        # model one with `f_integer=1000` does not exists
        self.assertLess(model_ones[-1].f_integer, 1000)
        # model_two can be rewritten
        item_one = ItemGeneralOne(
            f_integer=1000,
            two_1_1=item_two,
            two_1_x=[item_two],
            two_x_1=item_two,
            two_x_x=[item_two]
        )
        _, models_list = persister.persist(item_one)
        self.assertEqual(len(models_list), 1)
        self.assertEqual(len(models_list[0]), 1)
        model_one = models_list[0][0]
        
        two_1_x = self.get_related_x_to_many(model_one, 'two_1_x', sort_func)
        two_x_x = self.get_related_x_to_many(model_one, 'two_x_x', sort_func)
        self.assertEqual(len(two_1_x), 1)
        self.assertEqual(len(two_x_x), 1)
        
        self.assertEqual(model_one.f_integer, 1000)
        self.assertEqual(model_one.two_1_1.f_integer, 1000)
        self.assertEqual(two_1_x[0].f_integer, 1000)
        self.assertEqual(model_one.two_x_1.f_integer, 1000)
        self.assertEqual(two_x_x[0].f_integer, 1000)
        
        #--- no rewrite for model_two ---
        model_ones = self.get_all_models(self.ModelGeneralOne, sort_func)
        # model one with `f_integer=2000` does not exists
        self.assertLess(model_ones[-1].f_integer, 2000)
        item_one = ItemGeneralOne(f_integer=2000)
        persister.persist(item_one)
        
        # model_two cannot be rewritten
        item_one = ItemGeneralOne(
            f_integer=2000,
            two_1_1=item_two,
            two_1_x=[item_two],
            two_x_1=item_two,
            two_x_x=[item_two]
        )
        _, models_list = persister.persist(item_one)
        self.assertEqual(len(models_list), 1)
        self.assertEqual(len(models_list[0]), 1)
        model_one = models_list[0][0]
        
        two_1_x = self.get_related_x_to_many(model_one, 'two_1_x', sort_func)
        two_x_x = self.get_related_x_to_many(model_one, 'two_x_x', sort_func)
        self.assertEqual(len(two_1_x), 0)
        self.assertEqual(len(two_x_x), 0)
        
        self.assertEqual(model_one.f_integer, 2000)
        self.assertTrue(not hasattr(model_one, 'two_1_1') or
                        model_one.two_1_1 is None)
        self.assertTrue(not hasattr(model_one, 'two_x_1') or
                        model_one.two_x_1 is None)
    
        # model one with `f_integer=3000` does not exists
        self.assertLess(model_ones[-1].f_integer, 3000)
        
        # "many" side can be added to using new models if the side existed
        item_one = ItemGeneralOne(
            f_integer=3000,
            two_1_1=item_two,  # cannot rewrite item two
            two_1_x=[item_two],  # cannot redirect item_two
            two_x_1=item_two,  # can add to "many" side
            two_x_x=[item_two]  # can add to "many" side
        )
        _, models_list = persister.persist(item_one)
        self.assertEqual(len(models_list), 1)
        self.assertEqual(len(models_list[0]), 1)
        model_one = models_list[0][0]
        
        two_1_x = self.get_related_x_to_many(model_one, 'two_1_x', sort_func)
        two_x_x = self.get_related_x_to_many(model_one, 'two_x_x', sort_func)
        self.assertEqual(len(two_1_x), 0)
        self.assertEqual(len(two_x_x), 1)
        self.assertEqual(two_x_x[0].f_integer, 1000)
        
        self.assertEqual(model_one.f_integer, 3000)
        self.assertTrue(not hasattr(model_one, 'two_1_1') or
                        model_one.two_1_1 is None)
        self.assertEqual(model_one.two_x_1.f_integer, 1000)
        
    
    def test_norewrite_none(self):
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = [{'f_integer'}]
            getters = [{'f_integer'}]
            norewrite_fields = {
                'f_string': None,
                'two_1_1': None,
                True: True,
            }
          
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
            creators = [{'f_integer'}]
            getters = [{'f_integer'}]
         
        persister = self.persister
         
        # creating
        item_one = ItemGeneralOne(f_integer=1,
                                  # cannot rewrite
                                  f_string='str-1',
                                  two_1_1=ItemGeneralTwo(f_integer=102),
                                  # can rewrite
                                  f_text='text-1',
                                  two_x_1=ItemGeneralTwo(f_integer=103))
        persister.persist(item_one)
        model_ones = self.get_all_models(self.ModelGeneralOne)
        self.assertEqual(len(model_ones), 1)
        model_one = model_ones[0]
        self.assertEqual(model_one.f_integer, 1)
        self.assertEqual(model_one.f_string, 'str-1')
        self.assertIsNotNone(model_one.two_1_1)
        self.assertEqual(model_one.two_1_1.f_integer, 102)
        self.assertEqual(model_one.f_text, 'text-1')
        self.assertEqual(model_one.two_x_1.f_integer, 103)
         
        # updating
        item_one = ItemGeneralOne(f_integer=1,
                                  # cannot rewrite
                                  f_string='str-2',
                                  two_1_1=ItemGeneralTwo(f_integer=202),
                                  # can rewrite
                                  f_text='text-2',
                                  two_x_1=ItemGeneralTwo(f_integer=203))

        persister.persist(item_one)
        model_ones = self.get_all_models(self.ModelGeneralOne)
        self.assertEqual(len(model_ones), 1)
        model_one = model_ones[0]
        self.assertEqual(model_one.f_integer, 1)
        self.assertEqual(model_one.f_string, 'str-2')
        self.assertIsNotNone(model_one.two_1_1)
        self.assertEqual(model_one.two_1_1.f_integer, 202)
        self.assertEqual(model_one.f_text, 'text-1')
        self.assertEqual(model_one.two_x_1.f_integer, 103)
        
    
    def test_norewrite_false_creation(self):
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = [{'f_integer'}]
            getters = [{'f_integer'}]
            norewrite_fields = {
                'two_1_1': False,
                'two_1_x': False,
                'two_x_1': False,
                'two_x_x': False,
            }
          
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
            creators = [{'f_integer'}]
            getters = [{'f_integer'}]
        
        sort_func = lambda model: model.f_integer
        
        model_ones = self.get_all_models(self.ModelGeneralOne)
        model_twos = self.get_all_models(self.ModelGeneralTwo)
        self.assertEqual(len(model_ones), 0)
        self.assertEqual(len(model_twos), 0)    
        
        item_one = ItemGeneralOne(f_integer=1,
                                  two_1_1=ItemGeneralTwo(f_integer=1),
                                  two_1_x=[ItemGeneralTwo(f_integer=2)],
                                  two_x_1=ItemGeneralTwo(f_integer=3),
                                  two_x_x=[ItemGeneralTwo(f_integer=4)],)
        self.persister.persist(item_one)
        
        model_ones = self.get_all_models(self.ModelGeneralOne,
                                         sort_key=sort_func)
        model_twos = self.get_all_models(self.ModelGeneralTwo,
                                         sort_key=sort_func)
        # everything can be created
        self.assertEqual(len(model_ones), 1)
        self.assertEqual(len(model_twos), 4)
        
        two_1_x = self.get_related_x_to_many(model_ones[0], 'two_1_x',
                                             sort_key=sort_func)
        two_x_x = self.get_related_x_to_many(model_ones[0], 'two_x_x',
                                             sort_key=sort_func)
        self.assertEqual(len(two_1_x), 1)
        self.assertEqual(len(two_x_x), 1)
        self.assertEqual(model_ones[0].f_integer, 1)
        self.assertEqual(two_1_x[0].f_integer, 2)
        self.assertEqual(model_ones[0].two_x_1.f_integer, 3)
        self.assertEqual(two_x_x[0].f_integer, 4)
        
        # case when all models already existed
        bulk_two = ItemGeneralTwo.Bulk()
        bulk_two.gen(f_integer=5)
        bulk_two.gen(f_integer=6)
        bulk_two.gen(f_integer=7)
        bulk_two.gen(f_integer=8)
        self.persister.persist(bulk_two)
        # updating
        item_one = ItemGeneralOne(f_integer=1,
                                  two_1_1=ItemGeneralTwo(f_integer=5),
                                  two_1_x=[ItemGeneralTwo(f_integer=6)],
                                  two_x_1=ItemGeneralTwo(f_integer=7),
                                  two_x_x=[ItemGeneralTwo(f_integer=8)],)
        self.persister.persist(item_one)
        
        model_ones = self.get_all_models(self.ModelGeneralOne,
                                         sort_key=sort_func)
        model_twos = self.get_all_models(self.ModelGeneralTwo,
                                         sort_key=sort_func)
        self.assertEqual(len(model_ones), 1)
        self.assertEqual(len(model_twos), 8)  # models two existed
        
        # but model one stayed the same
        two_1_x = self.get_related_x_to_many(model_ones[0], 'two_1_x',
                                             sort_key=sort_func)
        two_x_x = self.get_related_x_to_many(model_ones[0], 'two_x_x',
                                             sort_key=sort_func)
        self.assertEqual(len(two_1_x), 1)
        self.assertEqual(len(two_x_x), 1)
        self.assertEqual(model_ones[0].f_integer, 1)
        self.assertEqual(two_1_x[0].f_integer, 2)
        self.assertEqual(model_ones[0].two_x_1.f_integer, 3)
        self.assertEqual(two_x_x[0].f_integer, 4)
        
        # case when models two are created
        item_one = ItemGeneralOne(f_integer=1,
                                  two_1_1=ItemGeneralTwo(f_integer=9),
                                  two_1_x=[ItemGeneralTwo(f_integer=10)],
                                  two_x_1=ItemGeneralTwo(f_integer=11),
                                  two_x_x=[ItemGeneralTwo(f_integer=12)],)
        self.persister.persist(item_one)
        
        model_ones = self.get_all_models(self.ModelGeneralOne,
                                         sort_key=sort_func)
        model_twos = self.get_all_models(self.ModelGeneralTwo,
                                         sort_key=sort_func)
        # everything can be created
        self.assertEqual(len(model_ones), 1)
        self.assertEqual(len(model_twos), 12)  # models two created
        
        # but model one stayed the same
        two_1_x = self.get_related_x_to_many(model_ones[0], 'two_1_x',
                                             sort_key=sort_func)
        two_x_x = self.get_related_x_to_many(model_ones[0], 'two_x_x',
                                             sort_key=sort_func)
        # x-to-many updated, but x-to-1 not
        self.assertEqual(len(two_1_x), 2)
        self.assertEqual(len(two_x_x), 2)
        self.assertEqual(model_ones[0].f_integer, 1)
        self.assertEqual(two_1_x[0].f_integer, 2)
        self.assertEqual(two_1_x[1].f_integer, 10)
        self.assertEqual(model_ones[0].two_x_1.f_integer, 3)
        self.assertEqual(two_x_x[0].f_integer, 4)
        self.assertEqual(two_x_x[1].f_integer, 12)
        
        
    def test_norewrite_false_cannot_create_1_x(self):
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = [{'f_integer'}]
            getters = [{'f_integer'}]
            norewrite_fields = {
                'two_1_1': False,
                'two_1_x': False,
                'two_x_1': False,
                'two_x_x': False,
            }
         
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
            creators = [{'one_1_1', 'one_1_x', 'f_integer',}]
            getters = [{'f_integer',}]
        
        sort_func = lambda model: model.f_integer
        
        model_ones = self.get_all_models(self.ModelGeneralOne)
        model_twos = self.get_all_models(self.ModelGeneralTwo)
        self.assertEqual(len(model_ones), 0)
        self.assertEqual(len(model_twos), 0)    
        
        # everything can be created
        item_two = ItemGeneralTwo(f_integer=2)
        item_one = ItemGeneralOne(f_integer=1,
                                  two_1_1=item_two,
                                  two_x_1=item_two)
        self.persister.persist(item_one)
        
        model_ones = self.get_all_models(self.ModelGeneralOne,
                                         sort_key=sort_func)
        model_twos = self.get_all_models(self.ModelGeneralTwo,
                                         sort_key=sort_func)
        
        self.assertEqual(len(model_ones), 1)
        self.assertEqual(len(model_twos), 1)
        
        self.assertEqual(model_ones[0].f_integer, 1)
        self.assertEqual(model_ones[0].two_1_1.f_integer, 2)
        self.assertEqual(model_ones[0].two_x_1.f_integer, 2)
        
        # models twos cannot be created (cannot rewrite model_one)
        item_two = ItemGeneralTwo(f_integer=3)
        item_one = ItemGeneralOne(f_integer=1,
                                  two_1_1=item_two,
                                  two_x_1=item_two)
        self.persister.persist(item_one)
        
        # nothing changed
        model_ones = self.get_all_models(self.ModelGeneralOne,
                                         sort_key=sort_func)
        model_twos = self.get_all_models(self.ModelGeneralTwo,
                                         sort_key=sort_func)
        
        self.assertEqual(len(model_ones), 1)
        self.assertEqual(len(model_twos), 1)
        
        self.assertEqual(model_ones[0].f_integer, 1)
        self.assertEqual(model_ones[0].two_1_1.f_integer, 2)
        self.assertEqual(model_ones[0].two_x_1.f_integer, 2)