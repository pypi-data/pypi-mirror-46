from save_to_db.core.item import Item
from save_to_db.utils.test_base import TestBase



class TestReplace(TestBase):
    
    ModelGeneralOne = None
    ModelGeneralTwo = None
    
    ModelManyRefsOne = None
    ModelManyRefsTwo = None
    
    
    def test_replace_x_to_many(self):
        
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = [{'f_string'}]
            getters = [{'f_string'}]
        
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
            creators = [{'f_string'}]
            getters = [{'f_string'}]
            relations = {
                'one_1_x': {
                    'replace_x_to_many': True,
                }
            }
        
        persister = self.persister
        
        # replace_x_to_many = False
        item_one = ItemGeneralOne(f_string='1')
        item_one['two_1_x'].gen(f_string='1: 2->1')
        item_one['two_1_x'].gen(f_string='2: 2->1')
        persister.persist(item_one)
        item_one = ItemGeneralOne(f_string='1')  # item recreated
        item_one['two_1_x'].gen(f_string='3: 2->1')
        item_one['two_1_x'].gen(f_string='4: 2->1')
        
        _, model_lists = persister.persist(item_one)
        self.assertEqual(len(model_lists), 1)
        models = model_lists[0]
        self.assertEqual(len(models), 1)
        model = models[0]
        two_1_x = self.get_related_x_to_many(model, 'two_1_x')
        self.assertEqual(len(two_1_x), 4)
        two_1_x.sort(key=lambda m: m.f_string)
        for i in range(4):
            self.assertEqual(two_1_x[i].f_string, '{}: 2->1'.format(i+1))
        
        # replace_x_to_many = True
        item_two = ItemGeneralTwo(f_string='2')
        item_two['one_1_x'].gen(f_string='1: 1->2')
        item_two['one_1_x'].gen(f_string='2: 1->2')
        persister.persist(item_two)
        item_two = ItemGeneralTwo(f_string='2')  # item recreated
        item_two['one_1_x'].gen(f_string='3: 1->2')
        item_two['one_1_x'].gen(f_string='4: 1->2')
        
        _, model_lists = persister.persist(item_two)
        self.assertEqual(len(model_lists), 1)
        models = model_lists[0]
        self.assertEqual(len(models), 1)
        model = models[0]
        one_1_x = self.get_related_x_to_many(model, 'one_1_x')
        self.assertEqual(len(one_1_x), 2)
        
        one_1_x.sort(key=lambda m: m.f_string)
        for i in range(2):
            # `i+3` because first two items replaced
            self.assertEqual(one_1_x[i].f_string, '{}: 1->2'.format(i+3))
    
    
    def __test_replace_x_to_many_additional_refrence(self,
                                                     one_1_x_a='one_1_x_a',
                                                     two_1_x_b='two_1_x_b'):

        class ItemManyRefsOne(Item):
            model_cls = self.ModelManyRefsOne
            creators = [{'f_string'}]
            getters = [{'f_string'}]
            relations = {
                'two_1_x_b': {
                    'replace_x_to_many': True,
                },
                'two_x_x_b': {
                    'replace_x_to_many': True,
                }
            }
        
        class ItemManyRefsTwo(Item):
            model_cls = self.ModelManyRefsTwo
            creators = [{'f_string'}]
            getters = [{'f_string'}]
            relations = {
                'one_1_x_a': {
                    'replace_x_to_many': True,
                },
                'one_x_x_a': {
                    'replace_x_to_many': True,
                }
            }
        
        persister = self.persister
        
        # --- creating ---
        item_two = ItemManyRefsTwo(f_string='Item 2.1')
        item_one = item_two[one_1_x_a].gen(f_string='Item 1.1')
        item_one[two_1_x_b].add(item_two)
        
        persister.persist(item_two)
        
        models_one = self.get_all_models(self.ModelManyRefsOne)
        models_two = self.get_all_models(self.ModelManyRefsTwo)
        self.assertEqual(len(models_one), 1)
        self.assertEqual(len(models_two), 1)
        self.assertEqual(models_one[0].f_string, 'Item 1.1')
        self.assertEqual(models_two[0].f_string, 'Item 2.1')
        
        x_models_two = self.get_related_x_to_many(models_one[0], two_1_x_b)
        x_models_one = self.get_related_x_to_many(models_two[0], one_1_x_a)
        self.assertEqual(len(x_models_one), 1)
        self.assertEqual(len(x_models_two), 1)
        
        self.assertEqual(x_models_one[0], models_one[0])
        self.assertEqual(x_models_two[0], models_two[0])
        
        # --- updating ---
        # item_two
        item_two = ItemManyRefsTwo(f_string='Item 2.1')
        item_two[one_1_x_a].gen(f_string='Item 1.2')
        # old item with old reference
        item_two['one_1_1_b'] = ItemManyRefsOne(f_string='Item 1.1')
        
        # item_one
        item_one = item_two['one_1_1_b']
        item_one[two_1_x_b].gen(f_string='Item 2.2')
        # old item with old reference
        item_one['two_1_1_a'] = item_two
        
        persister.persist(item_two)
        
        sort_func = lambda model: model.f_string
        
        models_one = self.get_all_models(self.ModelManyRefsOne)
        models_two = self.get_all_models(self.ModelManyRefsTwo)
        self.assertEqual(len(models_one), 2)
        self.assertEqual(len(models_two), 2)
        
        models_one.sort(key=sort_func)
        models_two.sort(key=sort_func)
        
        self.assertEqual(models_one[0].f_string, 'Item 1.1')
        self.assertEqual(models_one[1].f_string, 'Item 1.2')
        self.assertEqual(models_two[0].f_string, 'Item 2.1')
        self.assertEqual(models_two[1].f_string, 'Item 2.2')
        
        # updated relations must be without old references
        x_models_two = self.get_related_x_to_many(models_one[0], two_1_x_b)
        x_models_one = self.get_related_x_to_many(models_two[0], one_1_x_a)
        self.assertEqual(len(x_models_one), 1)
        self.assertEqual(len(x_models_two), 1)
        
        self.assertEqual(x_models_one[0], models_one[1])
        self.assertEqual(x_models_two[0], models_two[1])
        
        self.assertEqual(models_one[0].two_1_1_a, models_two[0])
        self.assertEqual(models_two[0].one_1_1_b, models_one[0])
    
    
    def test_replace_one_to_many_additional_refrence(self):
        self.__test_replace_x_to_many_additional_refrence(one_1_x_a='one_1_x_a',
                                                          two_1_x_b='two_1_x_b')
    
    
    def test_replace_many_to_many_additional_refrence(self):
        self.__test_replace_x_to_many_additional_refrence(one_1_x_a='one_x_x_a',
                                                          two_1_x_b='two_x_x_b')
    
    
    def test_one_to_one_replacement(self):

        class ItemManyRefsOne(Item):
            allow_merge_items = True
            model_cls = self.ModelManyRefsOne
            creators = [{'f_string'}]
            getters = [{'f_string'}]
        
        class ItemManyRefsTwo(Item):
            allow_merge_items = True
            model_cls = self.ModelManyRefsTwo
            creators = [{'f_string'}]
            getters = [{'f_string'}]
        
        persister = self.persister
        sort_func = lambda model: model.f_string
        
        # creating
        item_two = ItemManyRefsTwo(f_string='Item 2.1')
        item_two['one_1_1_a'] = ItemManyRefsOne(f_string='Item 1.1')
         
        persister.persist(item_two)
         
        models_one = self.get_all_models(self.ModelManyRefsOne)
        models_two = self.get_all_models(self.ModelManyRefsTwo)
        self.assertEqual(len(models_one), 1)
        self.assertEqual(len(models_two), 1)
        self.assertEqual(models_two[0].f_string, 'Item 2.1')
        self.assertEqual(models_one[0].f_string, 'Item 1.1')
         
        self.assertEqual(models_two[0].one_1_1_a, models_one[0])

        # updating without pulling old item
        item_two = ItemManyRefsTwo(f_string='Item 2.1')
        item_two['one_1_1_a'] = ItemManyRefsOne(f_string='Item 1.2')
        persister.persist(item_two)
        
        models_one = self.get_all_models(self.ModelManyRefsOne, sort_func)
        models_two = self.get_all_models(self.ModelManyRefsTwo, sort_func)
        self.assertEqual(len(models_one), 2)
        self.assertEqual(len(models_two), 1)
        self.assertEqual(models_one[0].f_string, 'Item 1.1')
        self.assertEqual(models_one[0].two_1_1_a, None)
        self.assertEqual(models_one[1].f_string, 'Item 1.2')
        self.assertEqual(models_one[1].two_1_1_a, models_two[0])
        self.assertEqual(models_two[0].f_string, 'Item 2.1')
        self.assertEqual(models_two[0].one_1_1_a, models_one[1])
    
    
    def test_one_to_one_additional_refrence(self):

        class ItemManyRefsOne(Item):
            allow_merge_items = True
            model_cls = self.ModelManyRefsOne
            creators = [{'f_string'}]
            getters = [{'f_string'}]
        
        class ItemManyRefsTwo(Item):
            allow_merge_items = True
            model_cls = self.ModelManyRefsTwo
            creators = [{'f_string'}]
            getters = [{'f_string'}]
        
        persister = self.persister
        sort_func = lambda model: model.f_string
        
        #  creating 
        item_two = ItemManyRefsTwo(f_string='Item 2.1')
        item_two['one_1_1_a'] = ItemManyRefsOne(f_string='Item 1.1')
        item_two['one_1_1_a']['two_1_1_b'] = \
            ItemManyRefsTwo(f_string='Item 2.2')
        
        persister.persist(item_two)
         
        models_one = self.get_all_models(self.ModelManyRefsOne, sort_func)
        models_two = self.get_all_models(self.ModelManyRefsTwo, sort_func)
        self.assertEqual(len(models_one), 1)
        self.assertEqual(len(models_two), 2)
        self.assertEqual(models_two[0].f_string, 'Item 2.1')
        self.assertEqual(models_one[0].f_string, 'Item 1.1')
        self.assertEqual(models_two[1].f_string, 'Item 2.2')
        
        self.assertEqual(models_one[0].two_1_1_a, models_two[0])
        self.assertEqual(models_one[0].two_1_1_b, models_two[1])
        
        #  updating with pulling old item 
        item_two = ItemManyRefsTwo(f_string='Item 2.1')
        item_two['one_1_1_a'] = ItemManyRefsOne(f_string='Item 1.2')
        item_one = item_two['one_x_x_a'].gen(f_string='Item 1.1')
        item_one['two_1_1_b'] = ItemManyRefsTwo(f_string='Item 2.3')
        # this item can potentially keep reference to item two
        item_one['two_x_x_b'].gen(f_string='Item 2.2')
          
        persister.persist(item_two)
        models_one = self.get_all_models(self.ModelManyRefsOne, sort_func)
        models_two = self.get_all_models(self.ModelManyRefsTwo, sort_func)
        self.assertEqual(len(models_one), 2)
        self.assertEqual(len(models_two), 3)
        self.assertEqual(models_two[0].f_string, 'Item 2.1')
        self.assertEqual(models_two[1].f_string, 'Item 2.2')
        self.assertEqual(models_two[2].f_string, 'Item 2.3')
        self.assertEqual(models_one[0].f_string, 'Item 1.1')
        self.assertEqual(models_one[1].f_string, 'Item 1.2')
        
        self.assertFalse(hasattr(models_one[0], 'two_1_1_a') and
                         models_one[0].two_1_1_a)
        self.assertEqual(models_one[0].two_1_1_b, models_two[2])
        
        self.assertEqual(models_two[0].one_1_1_a, models_one[1])
        self.assertFalse(hasattr(models_two[0], 'one_1_1_b') and
                         models_two[0].one_1_1_b)
        
        self.assertFalse(hasattr(models_two[1], 'one_1_1_a') and
                         models_two[1].one_1_1_a)
        self.assertFalse(hasattr(models_two[1], 'one_1_1_b') and
                         models_two[1].one_1_1_b)
        
        x_models_two = self.get_related_x_to_many(models_one[0], 'two_x_x_b')
        self.assertEqual(len(x_models_two), 1)
        self.assertEqual(x_models_two[0].f_string, 'Item 2.2')
        
        x_models_one = self.get_related_x_to_many(models_two[0], 'one_x_x_a')
        self.assertEqual(len(x_models_one), 1)
        self.assertEqual(x_models_one[0].f_string, 'Item 1.1')