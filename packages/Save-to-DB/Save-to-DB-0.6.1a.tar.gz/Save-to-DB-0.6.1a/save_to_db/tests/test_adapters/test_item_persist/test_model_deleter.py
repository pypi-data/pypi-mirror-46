from itertools import chain

from save_to_db.core.item import Item
from save_to_db.core.scope import Scope
from save_to_db.utils.test_base import TestBase



class TestModelDeleter(TestBase):
    
    ModelGeneralOne = None
    ModelGeneralTwo = None
    
    
    def test_model_deleter(self):
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = [{'f_integer', 'f_string'}]
            getters = [{'f_integer', 'f_string'}]
            deleter_selectors = ['f_string']
        
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
        
        persister = self.persister
        get_key = lambda model: (model.f_string, model.f_integer)
        
        # imitating first collection from different sources
        for source_number in range(1, 4):
            for outer_i in range(1, 3):
                bulk = ItemGeneralOne.Bulk(
                    f_string='source-{}'.format(source_number))
                for inner_i in range(1, 3):
                    bulk.gen(f_integer=outer_i*100 + inner_i)
                persister.persist(bulk)
        
        # will delete nothing
        persister.execute_deleter(ItemGeneralOne)
        model_ones = self.get_all_models(self.ModelGeneralOne,
                                         sort_key=get_key)

        model_keys = [get_key(model) for model in model_ones]
        expected = [
            # source-1 first iteration
            ('source-1', 101),
            ('source-1', 102),
            # source-1 second iteration
            ('source-1', 201),
            ('source-1', 202),
            # source-2 first iteration
            ('source-2', 101),
            ('source-2', 102),
            # source-2 second iteration
            ('source-2', 201),
            ('source-2', 202),
            # source-3 first iteration
            ('source-3', 101),
            ('source-3', 102),
            # source-3 second iteration
            ('source-3', 201),
            ('source-3', 202),
        ]
        self.assertEqual(model_keys, expected)
        
        # imitating first collection from different sources
        for source_number in range(2, 4):
            for outer_i in range(2, 3):
                bulk = ItemGeneralOne.Bulk(
                    f_string='source-{}'.format(source_number))
                for inner_i in range(1, 4):
                    bulk.gen(f_integer=outer_i*100 + inner_i)
                persister.persist(bulk)
        
        persister.execute_deleter(ItemGeneralOne)
        model_ones = self.get_all_models(self.ModelGeneralOne,
                                         sort_key=get_key)

        model_keys = [get_key(model) for model in model_ones]
        expected = [
            # source-1 must have been ignored (and not deleted)
            ('source-1', 101),
            ('source-1', 102),
            ('source-1', 201),
            ('source-1', 202),
            # source-2 starts from second iteration
            ('source-2', 201),
            ('source-2', 202),
            ('source-2', 203),  # new model
            # source-3 starts from second iteration
            ('source-3', 201),
            ('source-3', 202),
            ('source-3', 203),  # new model
        ]
        self.assertEqual(model_keys, expected)
        
        
    def test_model_deleter_execute_on_persist(self):
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = [{'f_integer', 'f_string'}]
            getters = [{'f_integer', 'f_string'}]
            deleter_selectors = ['f_string']
            deleter_execute_on_persist = True
        
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
            creators = [{'f_integer', 'f_string'}]
            getters = [{'f_integer', 'f_string'}]
            deleter_selectors = ['f_string']
        
        persister = self.persister
        get_key = lambda model: (model.f_string, model.f_integer)
        
        # creating items
        item_one_bulk = ItemGeneralOne.Bulk()
        item_two_bulk = ItemGeneralTwo.Bulk()
        for i in range(1, 3):
            item_one_bulk.gen(f_integer=100+i, f_string='source-1')
            item_two_bulk.gen(f_integer=100+i, f_string='source-1')
        
        persister.persist(item_one_bulk)
        persister.persist(item_two_bulk)
        
        # recreating items (first item from bulk one must be deleted)
        item_one_bulk = ItemGeneralOne.Bulk()
        item_two_bulk = ItemGeneralTwo.Bulk()
        for i in range(2, 4):
            item_one_bulk.gen(f_integer=100+i, f_string='source-1')
            item_two_bulk.gen(f_integer=100+i, f_string='source-1')
        
        persister.persist(item_one_bulk)
        persister.persist(item_two_bulk)
        
        models_one = self.get_all_models(self.ModelGeneralOne,
                                         sort_key=get_key)
        model_one_keys = [get_key(model) for model in models_one]
        expect = [('source-1', 102), ('source-1', 103)]
        self.assertEqual(model_one_keys, expect)
        
        models_two = self.get_all_models(self.ModelGeneralTwo,
                                         sort_key=get_key)
        model_two_keys = [get_key(model) for model in models_two]
        expect = [('source-1', 101), ('source-1', 102), ('source-1', 103)]
        self.assertEqual(model_two_keys, expect)
    
    
    def test_model_deleter_execute_scoped(self):
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = [{'f_integer', 'f_string'}]
            getters = [{'f_integer', 'f_string'}]
            deleter_selectors = ['f_string']
        
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
        
        persister = self.persister
        get_key = lambda model: (model.f_string, model.f_integer)
        
        
        test_scope = Scope(
            {}, collection_id='test_model_deleter_execute_scoped_dummy')
        persister.persist(test_scope[ItemGeneralOne](
            f_string='source-9000', f_integer='9000'
        ))
        
        
        # imitating first collection from different sources
        for source_number in range(1, 3):
            bulk = ItemGeneralOne.Bulk(
                f_string='source-{}'.format(source_number))
            for inner_i in range(1, 3):
                bulk.gen(f_integer=100 + inner_i)
            persister.persist(bulk)
        
        # will delete nothing (db is empty)
        self.assertEqual(
            ItemGeneralOne.metadata['model_deleter'].selectors,
            [{'f_string': 'source-1'}, {'f_string': 'source-2'}],
        )
        self.assertEqual(
            ItemGeneralOne.metadata['model_deleter'].keepers,
            [{'id': 2}, {'id': 3}, {'id': 4}, {'id': 5}],
        )
        persister.execute_scope_deleter(ItemGeneralOne.get_collection_id())
        
        # delete must be reset after executing
        self.assertFalse(ItemGeneralOne.metadata['model_deleter'].selectors)
        self.assertFalse(ItemGeneralOne.metadata['model_deleter'].keepers)
        
        model_ones = self.get_all_models(self.ModelGeneralOne,
                                         sort_key=get_key)

        model_keys = [get_key(model) for model in model_ones]
        expected = [
            # source-1
            ('source-1', 101),
            ('source-1', 102),
            # source-2
            ('source-2', 101),
            ('source-2', 102),
            # from test scope
            ('source-9000', 9000),
        ]
        self.assertEqual(model_keys, expected)
        
        
        # delete without scope
        # ('source-1', 101) and ('source-2', 101) must be deleted
        scope = Scope({}, collection_id='test_model_deleter_execute_scoped')
        ScopedItemGeneralOne = scope[ItemGeneralOne]
        
        for source_number in range(1, 3):
            bulk = ItemGeneralOne.Bulk(
                f_string='source-{}'.format(source_number))
            for inner_i in range(2, 4):
                bulk.gen(f_integer=100 + inner_i)
            persister.persist(bulk)
        
        persister.execute_scope_deleter(ItemGeneralOne.get_collection_id())
        model_ones = self.get_all_models(self.ModelGeneralOne,
                                         sort_key=get_key)

        model_keys = [get_key(model) for model in model_ones]
        expected = [
            # source-1
            ('source-1', 102),
            ('source-1', 103),
            # source-2
            ('source-2', 102),
            ('source-2', 103),
            # from test scope
            ('source-9000', 9000),
        ]
        self.assertEqual(model_keys, expected)
        
        # delete with scope
        persisted_models = []
        for source_number in range(1, 3):
            bulk = ScopedItemGeneralOne.Bulk(
                f_string='source-{}'.format(source_number))
            for inner_i in range(3, 5):
                bulk.gen(f_integer=100 + inner_i)
            _, models_list = persister.persist(bulk)
            for model_list in models_list:
                persisted_models.extend(model_list)
        
        # before executing making sure that different model deleter was used
        self.assertFalse(ItemGeneralOne.metadata['model_deleter'].selectors)
        self.assertFalse(ItemGeneralOne.metadata['model_deleter'].keepers)
        
        expect_selectors = [
            {'f_string': 'source-1'},
            {'f_string': 'source-2'},
        ]
        scoped_deleter = ScopedItemGeneralOne.metadata['model_deleter']
        self.assertEqual(scoped_deleter.selectors, expect_selectors)
        
        persisted_models.sort(key=lambda model: model.id)
        scoped_deleter.keepers.sort(key=lambda keeper: keeper['id'])
        expect_keepers = [{'id': model.id} for model in persisted_models]
        self.assertTrue(len(expect_keepers) != 0)
        self.assertEqual(scoped_deleter.keepers, expect_keepers)
        
        # creating model without scope
        persister.persist(ItemGeneralOne(f_string='source-9009',
                                         f_integer='9009'))
        
        persister.execute_scope_deleter(
            ScopedItemGeneralOne.get_collection_id()
        )
        model_ones = self.get_all_models(self.ModelGeneralOne,
                                         sort_key=get_key)

        model_keys = [get_key(model) for model in model_ones]
        expected = [
            # source-1
            ('source-1', 103),
            ('source-1', 104),
            # source-2
            ('source-2', 103),
            ('source-2', 104),
            # from test scope
            ('source-9000', 9000),
            # from not scoped item class with deleter not executed
            ('source-9009', 9009),
        ]
        self.assertEqual(model_keys, expected)
    
    
    def test_model_unrefs(self):
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = [{'f_integer'}]
            getters = [{'f_integer'}]
            unref_x_to_many = {
                'two_1_x': ['f_string'],
                'two_x_x': ['f_string']
            }
        
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
            creators = [{'f_integer', 'f_string'}]
            getters = [{'f_integer', 'f_string'}]
        
        persister = self.persister
        get_key = lambda model: (model.f_text, model.f_string, model.f_integer)
        
        item_one = ItemGeneralOne(f_integer=100)
        for source_name in ['src-1', 'src-2']:
            for i in range(1, 3):
                item_one['two_1_x'].gen(f_integer=200+i, f_string=source_name,
                                        f_text='two_1_x')
                item_one['two_x_x'].gen(f_integer=900+i, f_string=source_name,
                                        f_text='two_x_x')
        persister.persist(item_one)
        
        model_ones = self.get_all_models(self.ModelGeneralOne)
        self.assertEqual(len(model_ones), 1)
        model_one = model_ones[0]
        self.assertEqual(model_one.f_integer, 100)
        two_1_x = self.get_related_x_to_many(model_one, 'two_1_x',
                                             sort_key=get_key)
        two_x_x = self.get_related_x_to_many(model_one, 'two_x_x',
                                             sort_key=get_key)
        self.assertEqual(len(two_1_x), 4)
        self.assertEqual(len(two_x_x), 4)
        keys = [get_key(model) for model in chain(two_1_x, two_x_x)]
        expect = [
            ('two_1_x', 'src-1', 201),
            ('two_1_x', 'src-1', 202),
            ('two_1_x', 'src-2', 201),
            ('two_1_x', 'src-2', 202),
            ('two_x_x', 'src-1', 901),
            ('two_x_x', 'src-1', 902),
            ('two_x_x', 'src-2', 901),
            ('two_x_x', 'src-2', 902)
        ]
        self.assertEqual(keys, expect)
        
        item_one = ItemGeneralOne(f_integer=100)
        for source_name in ['src-1', 'src-2']:
            for i in range(2, 4):
                item_one['two_1_x'].gen(f_integer=200+i, f_string=source_name,
                                        f_text='two_1_x')
                item_one['two_x_x'].gen(f_integer=900+i, f_string=source_name,
                                        f_text='two_x_x')
        persister.persist(item_one)
        model_ones = self.get_all_models(self.ModelGeneralOne)
        self.assertEqual(len(model_ones), 1)
        model_one = model_ones[0]
        self.assertEqual(model_one.f_integer, 100)
        two_1_x = self.get_related_x_to_many(model_one, 'two_1_x',
                                             sort_key=get_key)
        two_x_x = self.get_related_x_to_many(model_one, 'two_x_x',
                                             sort_key=get_key)
        self.assertEqual(len(two_1_x), 4)
        self.assertEqual(len(two_x_x), 4)
        keys = [get_key(model) for model in chain(two_1_x, two_x_x)]
        # f_integer 201 and 901 were removed
        expect = [
            ('two_1_x', 'src-1', 202),
            ('two_1_x', 'src-1', 203),
            ('two_1_x', 'src-2', 202),
            ('two_1_x', 'src-2', 203),
            ('two_x_x', 'src-1', 902),
            ('two_x_x', 'src-1', 903),
            ('two_x_x', 'src-2', 902),
            ('two_x_x', 'src-2', 903)
        ]
        self.assertEqual(keys, expect)
        
        # f_integer 201 and 901 are still in database
        model_twos = self.get_all_models(self.ModelGeneralTwo,
                                         sort_key=get_key)
        keys = [get_key(model) for model in model_twos]
        expect = [
            ('two_1_x', 'src-1', 201),
            ('two_1_x', 'src-1', 202),
            ('two_1_x', 'src-1', 203),
            ('two_1_x', 'src-2', 201),
            ('two_1_x', 'src-2', 202),
            ('two_1_x', 'src-2', 203),
            ('two_x_x', 'src-1', 901),
            ('two_x_x', 'src-1', 902),
            ('two_x_x', 'src-1', 903),
            ('two_x_x', 'src-2', 901),
            ('two_x_x', 'src-2', 902),
            ('two_x_x', 'src-2', 903)
        ]
        self.assertEqual(keys, expect)
        
        # delete must be reset after executing
        self.assertFalse(
            ItemGeneralOne.metadata['model_unrefs']['two_1_x'].selectors)
        self.assertFalse(
            ItemGeneralOne.metadata['model_unrefs']['two_1_x'].keepers)
        self.assertFalse(
            ItemGeneralOne.metadata['model_unrefs']['two_x_x'].selectors)
        self.assertFalse(
            ItemGeneralOne.metadata['model_unrefs']['two_x_x'].keepers)