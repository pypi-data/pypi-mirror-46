from save_to_db.core.item import Item
from save_to_db.utils.test_base import TestBase
from save_to_db.exceptions import ItemsNotTheSame, MultipleItemsMatch


class TestSimpleConfig(TestBase):
    
    ModelGeneralOne = None
    ModelGeneralTwo = None
    
    
    #--- batch_size ------------------------------------------------------------
    
    def test_batch_size(self):
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = [{'f_integer'}]
            getters = [{'f_integer'}]
        
        # need this for `ItemGeneralOne` (related field)
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
        
        persister = self.persister
        db_adapter = persister.db_adapter
        original_adapter_batch_size = db_adapter.BATCH_SIZE
        original_adapter_get = db_adapter.get
        list_of_get_sizes = []
        def decorated_adapter_get(items_and_fkeys, *args, **kwargs):
            nonlocal list_of_get_sizes
            list_of_get_sizes.append(len(items_and_fkeys))
            return original_adapter_get(items_and_fkeys, *args, **kwargs)
        db_adapter.get = decorated_adapter_get
        
        try:
            # unlimited batch size
            db_adapter.BATCH_SIZE = 1000
            bulk = ItemGeneralOne.Bulk()
            for i in range(10):
                bulk.gen(f_integer=i)
            persister.persist(bulk)
            # got everything in one batch
            self.assertEqual(list_of_get_sizes, [10])
            list_of_get_sizes.clear()
            
            db_adapter.BATCH_SIZE = 3
            persister.persist(bulk)
            # 4 batches with max size of 3
            self.assertEqual(list_of_get_sizes, [3, 3, 3, 1])
            list_of_get_sizes.clear()
            
            # unlimited again
            db_adapter.BATCH_SIZE = 1000
            persister.persist(bulk)
            self.assertEqual(list_of_get_sizes, [10])
            list_of_get_sizes.clear()
            
            # limit on item class side
            ItemGeneralOne.batch_size = 4
            persister.persist(bulk)
            # 2 batches with max size of 4
            self.assertEqual(list_of_get_sizes, [4, 4, 2])
            list_of_get_sizes.clear()
            
            bulk = ItemGeneralTwo.Bulk()
            for i in range(10):
                bulk.gen(f_integer=i)
            persister.persist(bulk)
            # second class not effected
            self.assertEqual(list_of_get_sizes, [10])
            list_of_get_sizes.clear()
        finally:
            db_adapter.get = original_adapter_get
            db_adapter.BATCH_SIZE = original_adapter_batch_size
    
    
    #--- nullables -------------------------------------------------------------
    
    def test_nullables(self):
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = [{'f_integer'}]
            getters = [{'f_integer'}]
            nullables = ['f_text', 'two_1_1', 'two_x_1', 'two_x_x']
            relations = {
                'two_x_x': {
                    'replace_x_to_many': True,
                }
            }
         
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
            creators = [{'f_integer'}]
            getters = [{'f_integer'}]
        
        persister = self.persister
        
        item_one = ItemGeneralOne(
            f_integer=1,
            f_text='text',
            two_1_1=ItemGeneralTwo(f_integer=2),
            two_x_1=ItemGeneralTwo(f_integer=3),
            two_x_x=[ItemGeneralTwo(f_integer=4)],
        )
        
        persister.persist(item_one)
        model_ones = self.get_all_models(self.ModelGeneralOne)
        self.assertEqual(len(model_ones), 1)
        model_one = model_ones[0]
        self.assertEqual(model_one.f_integer, 1)
        self.assertEqual(model_one.f_text, 'text')
        self.assertEqual(model_one.two_1_1.f_integer, 2)
        self.assertEqual(model_one.two_x_1.f_integer, 3)
        two_x_x = self.get_related_x_to_many(model_one, 'two_x_x')
        self.assertEqual(len(two_x_x), 1)
        self.assertEqual(two_x_x[0].f_integer, 4)
        
        # rewriting nullables with other values
        item_one = ItemGeneralOne(
            f_integer=1,
            f_text='text-2',
            two_1_1=ItemGeneralTwo(f_integer=1001),
            two_x_1=ItemGeneralTwo(f_integer=1002),
            two_x_x=[ItemGeneralTwo(f_integer=1003),
                     ItemGeneralTwo(f_integer=1004)],
        )
        persister.persist(item_one)
        model_ones = self.get_all_models(self.ModelGeneralOne)
        self.assertEqual(len(model_ones), 1)
        model_one = model_ones[0]
        self.assertEqual(model_one.f_integer, 1)
        self.assertEqual(model_one.f_text, 'text-2')
        self.assertEqual(model_one.two_1_1.f_integer, 1001)
        self.assertEqual(model_one.two_x_1.f_integer, 1002)
        two_x_x = self.get_related_x_to_many(model_one, 'two_x_x')
        self.assertEqual(len(two_x_x), 2)
        self.assertEqual(two_x_x[0].f_integer, 1003)
        self.assertEqual(two_x_x[1].f_integer, 1004)
        
        # no values fo nullables
        item_one = ItemGeneralOne(f_integer=1)
        persister.persist(item_one)
        model_ones = self.get_all_models(self.ModelGeneralOne)
        self.assertEqual(len(model_ones), 1)
        model_one = model_ones[0]
        self.assertEqual(model_one.f_integer, 1)
        self.assertIsNone(model_one.f_text)
        self.assertTrue(not hasattr(model_one, 'two_1_1') or
                        model_one.two_1_1 is None)
        two_x_x = self.get_related_x_to_many(model_one, 'two_x_x')
        self.assertEqual(len(two_x_x), 0)
    
    
    #--- fast_insert -----------------------------------------------------------
    
    def test_fast_insert(self):
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = [{'f_integer'}]
            getters = [{'f_integer'}]
        
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
            creators = ['f_integer']
            getters = ['f_integer']
            fast_insert = True
            
        persister = self.persister
        sort_func = lambda model: (model.f_integer, model.f_string)
        
        #--- no fast_insert ---
        item_one = ItemGeneralOne(f_integer=1, f_string='one')
        persister.persist(item_one)
        
        bulk_one = ItemGeneralOne.Bulk()
        bulk_one.gen(f_integer=1, f_string='one-updated')
        bulk_one.gen(f_integer=2, f_string='two')
        persister.persist(bulk_one)
        
        model_ones = self.get_all_models(self.ModelGeneralOne,
                                         sort_key=sort_func)
        self.assertEqual(len(model_ones), 2)
        self.assertEqual(model_ones[0].f_string, 'one-updated')
        self.assertEqual(model_ones[1].f_string, 'two')
        
        #--- fast_insert ---
        item_two = ItemGeneralTwo(f_integer=1, f_string='one')
        persister.persist(item_two)
        
        bulk_two = ItemGeneralTwo.Bulk()
        bulk_two.gen(f_integer=1, f_string='one-updated')
        bulk_two.gen(f_integer=2, f_string='two')
        # although "f_integer" field is a getter, since we use fast_insert,
        # new model will be create without checking for update
        persister.persist(bulk_two)
        
        model_twos = self.get_all_models(self.ModelGeneralTwo,
                                         sort_key=sort_func)
        self.assertEqual(len(model_twos), 3)
        self.assertEqual(model_twos[0].f_integer, 1)
        self.assertEqual(model_twos[0].f_string, 'one')
        self.assertEqual(model_twos[1].f_integer, 1)
        self.assertEqual(model_twos[1].f_string, 'one-updated')
        self.assertEqual(model_twos[2].f_integer, 2)
        self.assertEqual(model_twos[2].f_string, 'two')
    
    
    #--- get_only_mode ---------------------------------------------------------
    
    def test_get_only_mode(self):
        
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = [{'f_integer'}]
            getters = [{'f_integer'}, {'two_x_x'}]
            
            def __str__(self):
                return 'ItemGeneralOne, f_integer: {}'.format(self['f_integer'])
            
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
            creators = [{'f_integer'}]
            getters = [{'f_integer'}]
            
            def __str__(self):
                return 'ItemGeneralTwo, f_integer: {}'.format(self['f_integer'])
        
        persister = self.persister
        get_key = lambda model: (model.f_integer,
                                 model.f_string if model.f_string else '')
        
        #--- normal model creating ---------------------------------------------
        bulk_item_one = ItemGeneralOne.Bulk()
        
        for i in range(2):
            bulk_item_one.gen(f_integer=i,
                              two_x_x=[ItemGeneralTwo(f_integer=i)])
        
        self.assertFalse(ItemGeneralOne.get_only_mode)
        self.assertFalse(ItemGeneralTwo.get_only_mode)
        
        persister.persist(bulk_item_one)
        model_ones = self.get_all_models(self.ModelGeneralOne, sort_key=get_key)
        
        self.assertEqual(len(model_ones), 2)
        self.assertEqual(model_ones[0].f_integer, 0)
        self.assertEqual(model_ones[1].f_integer, 1)
        
        two_x_x_first = self.get_related_x_to_many(model_ones[0], 'two_x_x',
                                                   sort_key=get_key)
        self.assertEqual(len(two_x_x_first), 1)
        self.assertEqual(two_x_x_first[0].f_integer, 0)
        
        two_x_x_second = self.get_related_x_to_many(model_ones[1], 'two_x_x',
                                                    sort_key=get_key)
        self.assertEqual(len(two_x_x_second), 1)
        self.assertEqual(two_x_x_second[0].f_integer, 1)
        
        #--- some items in get_only_mode ---------------------------------------
        bulk_item_one = ItemGeneralOne.Bulk()
        
        # get only (cannot be created)
        # (related by "two_x_x" field item must be created)
        not_saved_item = bulk_item_one.gen(
            f_integer=10, f_string='str-{}'.format(10),
            two_x_x=[ItemGeneralTwo(f_integer=10)])
        not_saved_item.get_only_mode = True
        
        # normal
        item = bulk_item_one.gen(f_integer=20,
                                 f_string='str-{}'.format(20),
                                 two_x_x=[ItemGeneralTwo(f_integer=20)])
        
        
        # old items
        for i in range(2):
            item = bulk_item_one.gen(
                f_integer=i, f_string='str-{}'.format(i),
                two_x_x=[ItemGeneralTwo(f_integer=i,
                                        f_string='str-{}'.format(i))])
            
            # second item update only
            if i == 1:
                del item['f_integer']  # forcing to use 'two_x_x' getter
                item.get_only_mode = True
                item['two_x_x'][0].get_only_mode = True
        
        
        saved_items, _ = persister.persist(bulk_item_one)
        
        # f_integer values are 0, 1, 20 (with f_integer=1 deleted)    
        self.assertEqual(len(saved_items), 3)
        self.assertNotIn(not_saved_item, saved_items)
        
        # all items can be loaded except for `f_integer=10` one
        for item in bulk_item_one:
            if item is not_saved_item:
                continue
            self.assertIn(item, saved_items)
        
        # checking the data
        model_ones = self.get_all_models(self.ModelGeneralOne, sort_key=get_key)
        self.assertEqual(len(model_ones), 3)
        
        self.assertEqual(model_ones[0].f_integer, 0)
        self.assertEqual(model_ones[1].f_integer, 1)
        self.assertEqual(model_ones[2].f_integer, 20)
        
        self.assertEqual(model_ones[0].f_string, 'str-0')
        self.assertIsNone(model_ones[1].f_string)  # get_only_mode
        self.assertEqual(model_ones[2].f_string, 'str-20')
        
        # checking model_two without model_one
        model_twos = self.get_all_models(self.ModelGeneralTwo, sort_key=get_key)
        
        self.assertEqual(len(model_twos), 4)
        model_two = model_twos[-2]  # with `f_integer=10`
        self.assertEqual(model_two.f_integer, 10)
        
        one_x_x = self.get_related_x_to_many(model_two, 'one_x_x')
        self.assertEqual(len(one_x_x), 0)  # get_only_mode
        
        # checking all other model_two
        two_x_x = self.get_related_x_to_many(model_ones[0], 'two_x_x',
                                             sort_key=get_key)
        self.assertEqual(len(two_x_x), 1)
        self.assertEqual(two_x_x[0].f_integer, 0)
        self.assertEqual(two_x_x[0].f_string, 'str-0')
        
        two_x_x = self.get_related_x_to_many(model_ones[1], 'two_x_x',
                                             sort_key=get_key)
        self.assertEqual(len(two_x_x), 1)
        self.assertEqual(two_x_x[0].f_integer, 1)
        self.assertIsNone(two_x_x[0].f_string)  # get_only_mode
        
        two_x_x = self.get_related_x_to_many(model_ones[2], 'two_x_x',
                                             sort_key=get_key)
        self.assertEqual(len(two_x_x), 1)
        self.assertEqual(two_x_x[0].f_integer, 20)
    
    
    #--- update_only_mode ------------------------------------------------------
    
    def test_update_only_mode(self):
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = [{'f_integer'}]
            getters = [{'f_integer'}]
            update_only_mode = True
        
        self.item_cls_manager.autogenerate = True
        persister = self.persister
        
        bulk_one = ItemGeneralOne.Bulk()
        item = bulk_one.gen(f_integer='10', f_text='10-first')
        item.update_only_mode = False
        item = bulk_one.gen(f_integer='20', f_text='20-first')
        item.update_only_mode = False
        
        items, _ = persister.persist(bulk_one)
        self.assertEqual(len(items), 2)
        
        sort_func = lambda model: model.f_integer
        
        models_one = self.get_all_models(self.ModelGeneralOne,
                                         sort_key=sort_func)
        self.assertEqual(len(models_one), 2)
        self.assertEqual(models_one[0].f_integer, 10)
        self.assertEqual(models_one[0].f_text, '10-first')
        self.assertEqual(models_one[1].f_integer, 20)
        self.assertEqual(models_one[1].f_text, '20-first')
        
        bulk_one = ItemGeneralOne.Bulk()
        item = bulk_one.gen(f_integer='10', f_text='10-second')
        item = bulk_one.gen(f_integer='30', f_text='30-second')
        
        items, _ = persister.persist(bulk_one)
        self.assertEqual(len(items), 1)
        models_one = self.get_all_models(self.ModelGeneralOne,
                                         sort_key=sort_func)
        self.assertEqual(len(models_one), 2)
        self.assertEqual(models_one[0].f_integer, 10)
        self.assertEqual(models_one[0].f_text, '10-second')
        self.assertEqual(models_one[1].f_integer, 20)
        self.assertEqual(models_one[1].f_text, '20-first')
        
    
    #--- allow_multi_update ----------------------------------------------------
    
    def test_multiple_model_update(self):
        model_one_cls = self.ModelGeneralOne
        model_two_cls = self.ModelGeneralTwo
        
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = [{'f_integer'}]
            getters = [{'f_integer'}, {'f_float', 'f_text'}]
        
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
            creators = [{'f_integer'}]
            getters = [{'f_integer'}, {'f_float', 'one_x_1'}]
        
        persister = self.persister
        
        # with simple fields ---------------------------------------------------
        # creating two items with different integer fields but same other fields
        item = ItemGeneralOne(f_integer='100', f_float='200.200',
                              f_boolean=True)
        persister.persist(item)
        item = ItemGeneralOne(f_integer='200', f_float='200.200',
                              f_boolean=False)
        persister.persist(item)
        
        # updating to get 'f_float' and 'f_text' have the same values for
        # different models 
        item = ItemGeneralOne(f_integer='100', f_text='text-1')
        persister.persist(item)
        item = ItemGeneralOne(f_integer='200', f_text='text-1')
        persister.persist(item)
        
        self.assertEqual(len(self.get_all_models(model_one_cls)), 2)
        
        # this must get two models from database
        item = ItemGeneralOne(f_integer='100',
                              f_float='200.200', f_text='text-1')
        ItemGeneralOne.allow_multi_update= True
        items, model_lists = persister.persist(item)
        ItemGeneralOne.allow_multi_update= False
        
        self.assertEqual(len(items), 1)
        self.assertEqual(len(model_lists), 1)
        self.assertEqual(len(model_lists[0]), 2)
        models = model_lists[0]
        models.sort(key=lambda model: not model.f_boolean)
        
        self.assertIs(models[0].f_boolean, True)
        self.assertEqual(models[0].f_integer, 100)
        self.assertEqual(models[0].f_float, 200.2)
        self.assertEqual(models[0].f_text, 'text-1')
        
        self.assertIs(models[1].f_boolean, False)
        self.assertEqual(models[1].f_integer, 100)
        self.assertEqual(models[1].f_float, 200.2)
        self.assertEqual(models[1].f_text, 'text-1')
        
        # still 2 models in database
        self.assertEqual(len(self.get_all_models(model_one_cls)), 2)
        
        # using relations ------------------------------------------------------
        item = ItemGeneralTwo(f_integer='100', f_float='200.200')
        persister.persist(item)
        item = ItemGeneralTwo(f_integer='200', f_float='200.200')
        persister.persist(item)
        
        item_one = ItemGeneralOne(f_integer='300')  # new item one
        item = ItemGeneralTwo(f_integer='100', one_x_1=item_one)
        persister.persist(item)
        item = ItemGeneralTwo(f_integer='200', one_x_1=item_one)
        persister.persist(item)
        
        self.assertEqual(len(self.get_all_models(model_one_cls)), 3)
        self.assertEqual(len(self.get_all_models(model_two_cls)), 2)

        # this must get two models from database
        item = ItemGeneralTwo(f_float='200.200', one_x_1=item_one)
        ItemGeneralTwo.allow_multi_update = True
        item, model_lists = persister.persist(item)
        ItemGeneralTwo.allow_multi_update = False
        
        self.assertEqual(len(items), 1)
        self.assertEqual(len(model_lists), 1)
        self.assertEqual(len(model_lists[0]), 2)
        models = model_lists[0]
        models.sort(key=lambda model: model.f_integer)
        
        self.assertEqual(models[0].f_integer, 100)
        self.assertEqual(models[0].f_float, 200.2)
        
        self.assertEqual(models[1].f_integer, 200)
        self.assertEqual(models[1].f_float, 200.2)
        
        self.assertIs(models[0].one_x_1, models[1].one_x_1)
        self.assertEqual(models[0].one_x_1.f_integer, 300)
    
    
    def test_set_multiple_related(self):
        model_one_cls = self.ModelGeneralOne
        
        class ItemGeneralOne(Item):
            allow_multi_update = True
            model_cls = self.ModelGeneralOne
            creators = [{'f_integer'}]
            getters = [{'f_integer'}, {'f_float', 'f_text'}]
        
        class ItemGeneralTwo(Item):
            allow_multi_update = True
            model_cls = self.ModelGeneralTwo
            creators = [{'f_integer'}]
            getters = [{'f_integer'}, {'f_float', 'one_x_1'}]
        
        persister = self.persister
        
        # creating two items with different integer fields but same other fields
        item = ItemGeneralOne(f_integer='100', f_float='200.200',
                              f_boolean=True)
        persister.persist(item)
        item = ItemGeneralOne(f_integer='200', f_float='200.200',
                              f_boolean=False)
        persister.persist(item)
        
        # updating to get 'f_float' and 'f_text' have the same values for
        # different models 
        item_one = ItemGeneralOne(f_integer='100', f_text='text-1')
        persister.persist(item_one)
        item_one = ItemGeneralOne(f_integer='200', f_text='text-1')
        persister.persist(item_one)
        
        self.assertEqual(len(self.get_all_models(model_one_cls)), 2)
        
        #--- set two models to x-to-many field must work -----------------------
        item_two = ItemGeneralTwo(f_integer='100')
        item_two['one_1_x'].gen(f_float='200.200', f_text='text-1')
        
        items, model_lists = persister.persist(item_two)
        self.assertEqual(len(items), 1)
        self.assertEqual(len(model_lists), 1)
        self.assertEqual(len(model_lists[0]), 1)
        
        # but the model has two related models
        one_1_x = self.get_all_models(model_one_cls)
        self.assertEqual(len(one_1_x), 2)
        
        one_1_x.sort(key=lambda model: model.f_integer)
        self.assertEqual(one_1_x[0].f_integer, 100)
        self.assertEqual(one_1_x[0].f_float, 200.2)
        self.assertEqual(one_1_x[0].f_text, 'text-1')
        self.assertEqual(one_1_x[1].f_integer, 200)
        self.assertEqual(one_1_x[1].f_float, 200.2)
        self.assertEqual(one_1_x[1].f_text, 'text-1')

    
    #--- allow_merge_items -----------------------------------------------------
    
    def test_allow_merge_items(self):
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = ['f_integer']
            getters = ['f_integer']
            allow_merge_items = True
        
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
            creators = ['f_integer']
            getters = ['f_integer']
            allow_merge_items = True
        
        # one
        item_one_1 = ItemGeneralOne(f_integer='1000')
        
        # two
        item_one_1['two_1_x'].gen(f_integer='1001',
                                  f_text='text-1')
        item_two_2 = item_one_1['two_1_x'].gen(f_integer='1001',
                                               f_string='str-1')
        
        # one
        item_two_2['one_x_x'].gen(f_integer='2001',
                                  f_text='text-2')
        item_two_2['one_x_x'].gen(f_integer='2001',
                                  f_string='str-2')
        # not mergable
        item_two_2['one_x_x'].gen(f_integer='9999',
                                  f_string='str-9')
        item_one_1.process()
        
        expect = {
            'item': {
                'two_1_x': {
                    'defaults': {
                        'one_x_1': {
                            'id': 1
                        }
                    },
                    'bulk': [{
                        'item': {
                            'one_x_x': {
                                'defaults': {
                                    'two_x_x': {
                                        'defaults': {},
                                        'bulk': [{
                                            'id': 2
                                        }]
                                    }
                                },
                                'bulk': [{
                                    'item': {
                                        'f_text': 'text-2',
                                        'two_x_x': {
                                            'defaults': {},
                                            'bulk': [{
                                                'id': 2
                                            }]
                                        },
                                        'f_integer': 2001,
                                        'f_string': 'str-2'
                                    }
                                }, {
                                    'item': {
                                        'two_x_x': {
                                            'defaults': {},
                                            'bulk': [{
                                                'id': 2
                                            }]
                                        },
                                        'f_integer': 9999,
                                        'f_string': 'str-9'
                                    }
                                }]
                            },
                            'f_text': 'text-1',
                            'one_x_1': {
                                'id': 1
                            },
                            'f_integer': 1001,
                            'f_string': 'str-1'
                        },
                        'id': 2
                    }]
                },
                'f_integer': 1000
            },
            'id': 1
        }

        self.assertEqual(item_one_1.to_dict(), expect)
        
        # merging at top level
        bulk_one = ItemGeneralOne.Bulk()
        bulk_one.gen(f_integer='1', f_string='str-1')
        bulk_one.gen(f_integer='1', f_text='text-1')
        bulk_one.process()
        
        expect = {
            'bulk': [
                {
                    'item': {
                        'f_integer': 1,
                        'f_string': 'str-1',
                        'f_text': 'text-1'
                    }
                }
            ],
            'defaults': {}
        }
        self.assertEqual(bulk_one.to_dict(), expect)
        
        
    def test_merging_items_point_each_other(self):
        class ItemMergeOne(Item):
            model_cls = self.ModelMergeOne
            creators = ['f_integer']
            getters = ['f_integer']
        
        class ItemMergeTwo(Item):
            model_cls = self.ModelMergeTwo
            creators = ['f_integer']
            getters = ['f_integer']
            allow_merge_items = True
        
        class ItemMergeThree(Item):
            model_cls = self.ModelMergeThree
            creators = ['f_integer']
            getters = ['f_integer']
            allow_merge_items = True
        
        bulk_one = ItemMergeOne.Bulk(two_x_1__three_x_1__f_float=1.0,
                                     two_x_1__f_integer=10)
        for i in range(1, 3):
            item_one = bulk_one.gen(f_integer=i)
            item_one['two_x_1__three_x_1'](f_integer=20)
        
        # items two and items three must be merged, they all the same and can
        # be merged into one item, but they reference each other
        bulk_one.process()
        
        item_one_1, item_one_2 = bulk_one
        
        self.assertEqual(item_one_1['f_integer'], 1)
        self.assertEqual(item_one_2['f_integer'], 2)
        
        self.assertIs(item_one_1['two_x_1'], item_one_1['two_x_1'])
        two_x_1 = item_one_1['two_x_1']
        
        self.assertEqual(two_x_1['f_integer'], 10)
        three_x_1 = two_x_1['three_x_1']
        
        self.assertEqual(three_x_1['f_integer'], 20)
        self.assertEqual(three_x_1['f_float'], 1.0)
        
        
    def test_merge_items_not_the_same(self):
        class ItemMergeOne(Item):
            model_cls = self.ModelMergeOne
            creators = ['f_integer']
            getters = ['f_integer']
        
        class ItemMergeTwo(Item):
            model_cls = self.ModelMergeTwo
            creators = ['f_integer']
            getters = ['f_integer']
            allow_merge_items = True
        
        class ItemMergeThree(Item):
            model_cls = self.ModelMergeThree
            creators = ['f_integer']
            getters = ['f_integer']
            
        
        bulk_one = ItemMergeOne.Bulk(two_x_1__three_x_1__f_float=1.0,
                                     two_x_1__f_integer=10)
        for i in range(1, 3):
            item_one = bulk_one.gen(f_integer=i)
            item_one['two_x_1__three_x_1'](f_integer=20+i)
        
        with self.assertRaises(ItemsNotTheSame):
            bulk_one.process()
    
    
    def test_merge_bulk_items(self):
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = ['f_integer']
            getters = ['f_integer']
        
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
            creators = ['f_integer']
            getters = ['f_integer']
        
        def gen_bulk_one():
            bulk_one = ItemGeneralOne.Bulk()
            bulk_one.gen(f_integer=1,
                         two_x_x=[ItemGeneralTwo(f_integer=10),
                                  ItemGeneralTwo(f_integer=11)])
            bulk_one.gen(f_integer=2,
                         two_x_x=[ItemGeneralTwo(f_integer=11),
                                  ItemGeneralTwo(f_integer=12)])
            return bulk_one
        
        bulk_one = gen_bulk_one()
        with self.assertRaises(MultipleItemsMatch):
            bulk_one.process()
        
        ItemGeneralOne.allow_merge_items = True
        ItemGeneralTwo.allow_merge_items = True
        bulk_one = gen_bulk_one()
        bulk_one[0]['two_x_x'][1]['f_float'] = 1
        bulk_one[1]['two_x_x'][0]['f_float'] = 2
        
        with self.assertRaises(ItemsNotTheSame):
            bulk_one.process()
        
        bulk_one = gen_bulk_one()
        self.assertIsNot(bulk_one[0]['two_x_x'][1], 
                         bulk_one[1]['two_x_x'][0])
        bulk_one.process()
        self.assertEqual(len(bulk_one[0]['two_x_x']), 2)
        self.assertEqual(len(bulk_one[1]['two_x_x']), 2)
        self.assertIs(bulk_one[0]['two_x_x'][1], 
                      bulk_one[1]['two_x_x'][0])
        two_x_x = []
        for item_one in bulk_one:
            for item_two in item_one['two_x_x']:
                if item_two not in two_x_x:
                    two_x_x.append(item_two)
        self.assertEqual(len(two_x_x), 3)