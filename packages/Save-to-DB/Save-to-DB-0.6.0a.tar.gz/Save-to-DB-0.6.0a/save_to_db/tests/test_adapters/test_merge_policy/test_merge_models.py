from save_to_db.exceptions import CannotMergeModels, MergeModelsNotAllowed
from save_to_db.core.item import Item
from save_to_db.core.merge_policy import MergePolicy
from save_to_db.utils.test_base import TestBase


class TestMergeModels(TestBase):
    
    def setUp(self):
        super().setUp()

        class ItemMergeOne(Item):
            model_cls = self.ModelMergeOne
        self.ItemMergeOne = ItemMergeOne
        
        class ItemMergeTwo(Item):
            model_cls = self.ModelMergeTwo
        self.ItemMergeTwo = ItemMergeTwo
        
        class ItemMergeThree(Item):
            model_cls = self.ModelMergeThree
        self.ItemMergeThree = ItemMergeThree
        
        
        class ItemMergeOneX(Item):
            model_cls = self.ModelMergeOneX
        self.ItemMergeOneX = ItemMergeOneX
        
        class ItemMergeTwoX(Item):
            model_cls = self.ModelMergeTwoX
        self.ItemMergeTwoX = ItemMergeTwoX
        
        class ItemMergeThreeX(Item):
            model_cls = self.ModelMergeThreeX
        self.ItemMergeThreeX = ItemMergeThreeX
        
        
        def x_to_one_merge(model, merged_model,
                           child_model, merged_child_model,
                           forward_foreign_key, reverse_foreign_key):
            self.merge_call_log.append([
                model, merged_model,
                child_model, merged_child_model,
                forward_foreign_key, reverse_foreign_key,
            ])
            return self.persister.merge_models(
                [child_model, merged_child_model],
                merge_policy=self.merge_policy,
                ignore_fields=[reverse_foreign_key])
            
        def one_to_many_merge(model, merged_model,
                              child_model, merged_child_model,
                              forward_foreign_key, reverse_foreign_key,
                              constaints):
            self.merge_call_log.append([
                model, merged_model,
                child_model, merged_child_model,
                
                forward_foreign_key, reverse_foreign_key,
                constaints,
            ])
            return self.persister.merge_models(
                [child_model, merged_child_model],
                merge_policy=self.merge_policy,
                ignore_fields=[reverse_foreign_key])
        
        self.merge_call_log = []
        self.merge_policy = MergePolicy(self.db_adapter, {
            self.ModelMergeOne: {
                'two_1_1': x_to_one_merge,
                'two_x_1': x_to_one_merge,
            },
            self.ModelMergeTwo: {
                'one_1_1': x_to_one_merge,
                'one_1_x': one_to_many_merge,
                'three_1_1': x_to_one_merge,
                'three_x_1': x_to_one_merge,
            },
            self.ModelMergeThree: {
                'two_1_1': x_to_one_merge,
                'two_1_x': one_to_many_merge,
            },
                             
            self.ModelMergeOneX: {
                'two_x_1': x_to_one_merge,
            },
            self.ModelMergeTwoX: {
                'one_1_x': one_to_many_merge,
                'three_x_1': x_to_one_merge,
            },
            self.ModelMergeThreeX: {
                'two_1_x': one_to_many_merge,
            },
        })
        
    
    def test_merge_propagation_1_to_1(self):
        sort_func = lambda model: model.f_integer
        
        item_one = self.ItemMergeOne(f_integer=101, f_text='text-101')
        item_two = item_one['two_1_1'](f_integer=102, f_text='text-102')
        item_two['three_1_1'](f_integer=103, f_text='text-103')
        self.persister.persist(item_one)
        
        item_one = self.ItemMergeOne(f_integer=201, f_string='string-201')
        item_two = item_one['two_1_1'](f_integer=202, f_string='string-202')
        item_two['three_1_1'](f_integer=203, f_string='string-203')
        self.persister.persist(item_one)
        
        model_ones = self.get_all_models(self.ModelMergeOne, sort_key=sort_func)
        self.assertEqual(len(model_ones), 2)
        
        model_one = model_ones[0]
        self.assertEqual(model_one.f_integer, 101)
        self.assertEqual(model_one.two_1_1.f_integer, 102)
        self.assertEqual(model_one.two_1_1.three_1_1.f_integer, 103)
        
        model_one = model_ones[1]
        self.assertEqual(model_one.f_integer, 201)
        self.assertEqual(model_one.two_1_1.f_integer, 202)
        self.assertEqual(model_one.two_1_1.three_1_1.f_integer, 203)
        
        # merging
        expect_log = [
            [
                model_ones[0],
                model_ones[1],
                model_ones[0].two_1_1,
                model_ones[1].two_1_1,
                'two_1_1', 'one_1_1',
            ],
            [
                model_ones[0].two_1_1,
                model_ones[1].two_1_1,
                model_ones[0].two_1_1.three_1_1,
                model_ones[1].two_1_1.three_1_1,
                'three_1_1', 'two_1_1',
            ],
        ]
        merged_one = self.persister.merge_models(model_ones,
                                                 merge_policy=self.merge_policy)
        self.persister.db_adapter.save_model(merged_one)
        self.assertEqual(self.merge_call_log, expect_log)
        
        model_ones = self.get_all_models(self.ModelMergeOne, sort_key=sort_func)
        self.assertEqual(len(model_ones), 1)
        self.assertEqual(merged_one, model_ones[0])
        
        # other models should be merged
        model_twos = self.get_all_models(self.ModelMergeTwo, sort_key=sort_func)
        self.assertEqual(len(model_twos), 1)
        model_threes = self.get_all_models(self.ModelMergeThree,
                                           sort_key=sort_func)
        self.assertEqual(len(model_threes), 1)
        
        # checking the model
        self.assertEqual(merged_one.f_integer, 101)
        self.assertEqual(merged_one.f_text, 'text-101')
        self.assertEqual(merged_one.f_string, 'string-201')
        self.assertEqual(merged_one.two_1_1.f_integer, 102)
        self.assertEqual(merged_one.two_1_1.f_text, 'text-102')
        self.assertEqual(merged_one.two_1_1.f_string, 'string-202')
        self.assertEqual(merged_one.two_1_1.three_1_1.f_integer, 103)
        self.assertEqual(merged_one.two_1_1.three_1_1.f_text, 'text-103')
        self.assertEqual(merged_one.two_1_1.three_1_1.f_string, 'string-203')
    
    
    def test_merge_no_propagation_1_to_1(self):
        sort_func = lambda model: model.f_integer
        
        item_one = self.ItemMergeOne(f_integer=101, f_text='text-101')
        item_two = item_one['two_1_1'](f_integer=102, f_text='text-102')
        item_two['three_1_1'](f_integer=103, f_text='text-103')
        self.persister.persist(item_one)
        
        item_one = self.ItemMergeOne(f_integer=201, f_string='string-201')
        item_two = item_one['two_1_1'](f_integer=202, f_string='string-202')
        item_two['three_1_1'](f_integer=203, f_string='string-203')
        self.persister.persist(item_one)
        
        model_ones = self.get_all_models(self.ModelMergeOne, sort_key=sort_func)
        self.assertEqual(len(model_ones), 2)
        
        model_one = model_ones[0]
        self.assertEqual(model_one.f_integer, 101)
        self.assertEqual(model_one.two_1_1.f_integer, 102)
        self.assertEqual(model_one.two_1_1.three_1_1.f_integer, 103)
        
        model_one = model_ones[1]
        self.assertEqual(model_one.f_integer, 201)
        self.assertEqual(model_one.two_1_1.f_integer, 202)
        self.assertEqual(model_one.two_1_1.three_1_1.f_integer, 203)
        
        # merging
        with self.assertRaises(CannotMergeModels):
            self.persister.merge_models(model_ones)
        
    
    def test_merge_propagation_x_to_1(self):
        sort_func = lambda model: model.f_integer
        
        item_one = self.ItemMergeOne(f_integer=101, f_text='text-101')
        item_two = item_one['two_x_1'](f_integer=102, f_text='text-102')
        item_two['three_x_1'](f_integer=103, f_text='text-103')
        self.persister.persist(item_one)
        
        item_one = self.ItemMergeOne(f_integer=201, f_string='string-201')
        item_two = item_one['two_x_1'](f_integer=202, f_string='string-202')
        item_two['three_x_1'](f_integer=203, f_string='string-203')
        self.persister.persist(item_one)
        
        model_ones = self.get_all_models(self.ModelMergeOne, sort_key=sort_func)
        self.assertEqual(len(model_ones), 2)
        
        model_one = model_ones[0]
        self.assertEqual(model_one.f_integer, 101)
        self.assertEqual(model_one.two_x_1.f_integer, 102)
        self.assertEqual(model_one.two_x_1.three_x_1.f_integer, 103)
        
        model_one = model_ones[1]
        self.assertEqual(model_one.f_integer, 201)
        self.assertEqual(model_one.two_x_1.f_integer, 202)
        self.assertEqual(model_one.two_x_1.three_x_1.f_integer, 203)
        
        # merging
        expect_log = [
            [
                model_ones[0],
                model_ones[1],
                model_ones[0].two_x_1,
                model_ones[1].two_x_1,
                'two_x_1', 'one_1_x',
            ],
            [
                model_ones[0].two_x_1,
                model_ones[1].two_x_1,
                model_ones[0].two_x_1.three_x_1,
                model_ones[1].two_x_1.three_x_1,
                'three_x_1', 'two_1_x',
            ],
        ]
        merged_one = self.persister.merge_models(model_ones,
                                                 merge_policy=self.merge_policy)
        self.persister.db_adapter.save_model(merged_one)
        self.assertEqual(self.merge_call_log, expect_log)
        
        model_ones = self.get_all_models(self.ModelMergeOne, sort_key=sort_func)
        self.assertEqual(len(model_ones), 1)
        self.assertEqual(merged_one, model_ones[0])
        
        # other models should be merged
        model_twos = self.get_all_models(self.ModelMergeTwo, sort_key=sort_func)
        self.assertEqual(len(model_twos), 1)
        model_threes = self.get_all_models(self.ModelMergeThree,
                                           sort_key=sort_func)
        self.assertEqual(len(model_threes), 1)
        
        # checking the model
        self.assertEqual(merged_one.f_integer, 101)
        self.assertEqual(merged_one.f_text, 'text-101')
        self.assertEqual(merged_one.f_string, 'string-201')
        self.assertEqual(merged_one.two_x_1.f_integer, 102)
        self.assertEqual(merged_one.two_x_1.f_text, 'text-102')
        self.assertEqual(merged_one.two_x_1.f_string, 'string-202')
        self.assertEqual(merged_one.two_x_1.three_x_1.f_integer, 103)
        self.assertEqual(merged_one.two_x_1.three_x_1.f_text, 'text-103')
        self.assertEqual(merged_one.two_x_1.three_x_1.f_string, 'string-203')
    
    
    def test_merge_no_propagation_x_to_1(self):
        sort_func = lambda model: model.f_integer
        
        item_one = self.ItemMergeOne(f_integer=101, f_text='text-101')
        item_two = item_one['two_x_1'](f_integer=102, f_text='text-102')
        item_two['three_x_1'](f_integer=103, f_text='text-103')
        self.persister.persist(item_one)
        
        item_one = self.ItemMergeOne(f_integer=201, f_string='string-201')
        item_two = item_one['two_x_1'](f_integer=202, f_string='string-202')
        item_two['three_x_1'](f_integer=203, f_string='string-203')
        self.persister.persist(item_one)
        
        model_ones = self.get_all_models(self.ModelMergeOne, sort_key=sort_func)
        self.assertEqual(len(model_ones), 2)
        
        model_one = model_ones[0]
        self.assertEqual(model_one.f_integer, 101)
        self.assertEqual(model_one.two_x_1.f_integer, 102)
        self.assertEqual(model_one.two_x_1.three_x_1.f_integer, 103)
        
        model_one = model_ones[1]
        self.assertEqual(model_one.f_integer, 201)
        self.assertEqual(model_one.two_x_1.f_integer, 202)
        self.assertEqual(model_one.two_x_1.three_x_1.f_integer, 203)
        
        # merging
        with self.assertRaises(CannotMergeModels):
            self.persister.merge_models(model_ones)
    
    
    def __structure_models_for_propagation_1_to_x(self, model_threes):
        sort_func = lambda model: model.f_integer
        
        structure = []
        for model_three in model_threes:
            entry_three = {
                'f_string': model_three.f_string,
                'f_integer': model_three.f_integer,
                'entries': []
            }
            structure.append(entry_three)
            for model_two in self.get_related_x_to_many(
                        model_three, 'two_1_x', sort_key=sort_func):
                entry_two = {
                    'f_string': model_two.f_string,
                    'f_integer': model_two.f_integer,
                    'entries': []
                }
                entry_three['entries'].append(entry_two)
                for model_one in self.get_related_x_to_many(
                        model_two, 'one_1_x',  sort_key=sort_func):
                    entry_one = {
                        'f_string': model_one.f_string,
                        'f_integer': model_one.f_integer,
                        'entries': []
                    }
                    entry_two['entries'].append(entry_one)
        
        return structure
                    
    
    def __generate_models_for_propagation_1_to_x(self):
        # Two structurees will be merged (three->two->one):
        #     /-1
        #    1--0
        # 0--|
        #    0--0
        #     \-0
        #
        # Where models must that must be merged mark as 1.
        
        sort_func = lambda model: model.f_string
        
        bulk_three = self.ItemMergeThreeX.Bulk()
        for x in range(1, 3):
            item_three = bulk_three.gen(
                f_integer=x*100,
                f_string='x: {}'.format(x))
            
            for y in range(1, 3):
                item_two = item_three['two_1_x'].gen(
                    f_integer=x*100 + y*10,
                    f_string='x: {}; y: {}'.format(x, y))
                
                for z in range(1, 3):
                    item_two['one_1_x'].gen(
                        f_integer=x*100 + y*10 + z,
                        f_string='x: {}; y: {}; z: {}'.format(x, y, z))

        self.persister.persist(bulk_three)
        model_threes = self.get_all_models(self.ModelMergeThreeX,
                                           sort_key=sort_func)
        self.assertEqual(len(model_threes), 2)
        
        model_three_1 = model_threes[0]
        model_three_2 = model_threes[1]
        
        # making some models to merge
        two_1_x_one = self.get_related_x_to_many(model_three_1, 'two_1_x',
                                                 sort_key=sort_func)
        two_1_x_two = self.get_related_x_to_many(model_three_2, 'two_1_x',
                                                 sort_key=sort_func)
        self.assertEqual(len(two_1_x_one), 2)
        self.assertEqual(len(two_1_x_two), 2)
        
        two_1_x_one[0].f_integer = two_1_x_two[0].f_integer
        self.persister.db_adapter.save_model(two_1_x_one[0])
        
        one_1_x_one = self.get_related_x_to_many(two_1_x_one[0], 'one_1_x',
                                                 sort_key=sort_func)
        one_1_x_two = self.get_related_x_to_many(two_1_x_two[0], 'one_1_x',
                                                 sort_key=sort_func)
        self.assertEqual(len(one_1_x_one), 2)
        self.assertEqual(len(one_1_x_two), 2)
        
        one_1_x_one[0].f_integer = one_1_x_two[0].f_integer
        self.persister.db_adapter.save_model(one_1_x_one[0])
        
    
    def test_merge_propagation_1_to_x(self):
        sort_func = lambda model: model.f_string
        self.__generate_models_for_propagation_1_to_x()
        
        # merging models
        model_threes = self.get_all_models(self.ModelMergeThreeX,
                                           sort_key=sort_func)
        self.assertEqual(len(model_threes), 2)
          
          
        two_1_x_one = self.get_related_x_to_many(model_threes[0], 'two_1_x',
                                                 sort_key=sort_func)[0]
        two_1_x_two = self.get_related_x_to_many(model_threes[1], 'two_1_x',
                                                 sort_key=sort_func)[0]
        one_1_x_one = self.get_related_x_to_many(two_1_x_one, 'one_1_x',
                                                 sort_key=sort_func)[0]
        one_1_x_two = self.get_related_x_to_many(two_1_x_two, 'one_1_x',
                                                 sort_key=sort_func)[0]
                                                   
        # merging
        # (for django models can be different after merge because of deletion)
        expect_log = [
            [
                model_threes[0].f_string,
                model_threes[1].f_string,
                two_1_x_one.f_string,
                two_1_x_two.f_string,
                'two_1_x', 'three_x_1',
                [{'three_x_1', 'f_integer'}]
            ],
            [
                two_1_x_one.f_string,
                two_1_x_two.f_string,
                one_1_x_one.f_string,
                one_1_x_two.f_string,
                'one_1_x', 'two_x_1',
                [{'two_x_1', 'f_integer'}]
            ],
        ]
        merged_three = self.persister.merge_models(
            model_threes, merge_policy=self.merge_policy)
        self.persister.db_adapter.save_model(merged_three)
        
        for entry in self.merge_call_log:
            for i in range(4):
                entry[i] = entry[i].f_string
        self.assertEqual(self.merge_call_log, expect_log)
        
        model_threes = self.get_all_models(self.ModelMergeThreeX,
                                           sort_key=sort_func)
        self.assertEqual(len(model_threes), 1)
        self.assertEqual(merged_three, model_threes[0])
         
        structure = self.__structure_models_for_propagation_1_to_x(
            model_threes)
        
        expected = [{
            'entries': [{
                'entries': [{
                    'entries': [],
                    'f_integer': 121,
                    'f_string': 'x: 1; y: 2; z: 1'
                }, {
                    'entries': [],
                    'f_integer': 122,
                    'f_string': 'x: 1; y: 2; z: 2'
                }],
                'f_integer': 120,
                'f_string': 'x: 1; y: 2'
            }, {
                'entries': [{
                    'entries': [],
                    'f_integer': 112,
                    'f_string': 'x: 1; y: 1; z: 2'
                }, {
                    'entries': [],
                    'f_integer': 211,
                    'f_string': 'x: 1; y: 1; z: 1'
                }, {
                    'entries': [],
                    'f_integer': 212,
                    'f_string': 'x: 2; y: 1; z: 2'
                }],
                'f_integer': 210,
                'f_string': 'x: 1; y: 1'
            }, {
                'entries': [{
                    'entries': [],
                    'f_integer': 221,
                    'f_string': 'x: 2; y: 2; z: 1'
                }, {
                    'entries': [],
                    'f_integer': 222,
                    'f_string': 'x: 2; y: 2; z: 2'
                }],
                'f_integer': 220,
                'f_string': 'x: 2; y: 2'
            }],
            'f_integer': 100,
            'f_string': 'x: 1'
        }]
        
        self.assertEqual(structure, expected)
        
        
    def test_merge_no_propagation_1_to_x(self):
        self.__generate_models_for_propagation_1_to_x()
        
        # merging models
        model_threes = self.get_all_models(self.ModelMergeThreeX)
        self.assertEqual(len(model_threes), 2)
        
        # for now we do not check before exception
        with self.assertRaises(Exception):
            self.persister.merge_models(model_threes)
    
    
    def test_ignore_regular_field(self):
        sort_func = lambda model: model.f_integer
        
        bulk_one = self.ItemMergeOne.Bulk()
        bulk_one.gen(f_integer=1, f_float=2.0)
        bulk_one.gen(f_integer=2, f_float=3.0, f_text='text', f_string='string')
        
        self.persister.persist(bulk_one)
        models_one = self.get_all_models(self.ModelMergeOne, sort_key=sort_func)
        self.assertEqual(len(models_one), 2)
        
        merged_model = self.persister.merge_models(models_one,
                                                   ignore_fields=['f_string'])
        self.persister.db_adapter.save_model(merged_model)
        
        models_one = self.get_all_models(self.ModelMergeOne, sort_key=sort_func)
        self.assertEqual(len(models_one), 1)
        
        model_one = models_one[0]
        self.assertEqual(model_one.f_integer, 1)
        self.assertEqual(model_one.f_float, 2)
        self.assertEqual(model_one.f_text, 'text')
        self.assertIsNone(model_one.f_string)
        
    
    def test_merging_not_allowed(self):
        sort_func = lambda model: model.f_integer
        
        #--- x-to-one allowed --------------------------------------------------
        # (CannotMergeModels exception will be raised)
        bulk_one = self.ItemMergeOne.Bulk()
        bulk_one.gen(f_integer=1,
                     two_1_1=self.ItemMergeTwo(f_integer=2))
        bulk_one.gen(f_integer=3,
                     two_1_1=self.ItemMergeTwo(f_integer=4))
        self.persister.persist(bulk_one)
        
        models_one = self.get_all_models(self.ModelMergeOne)
        self.assertEqual(len(models_one), 2)
        
        models_two = self.get_all_models(self.ModelMergeTwo)
        self.assertEqual(len(models_two), 2)
        
        with self.assertRaises(CannotMergeModels):
            self.persister.merge_models(models_one)
        
        #--- x-to-one not allowed ----------------------------------------------
        merge_policy = MergePolicy(self.db_adapter, {
            self.ModelMergeOne: {
                'two_1_1': False
            }
        })
        with self.assertRaises(MergeModelsNotAllowed):
            self.persister.merge_models(models_one, merge_policy=merge_policy)
        
        #--- x-to-many allowed -------------------------------------------------
        bulk_two = self.ItemMergeTwo.Bulk()
        bulk_two.gen(f_integer=101,
                     one_1_x=[self.ItemMergeOne(f_integer=102)])
        bulk_two.gen(f_integer=103,
                     one_1_x=[self.ItemMergeOne(f_integer=104)])
        self.persister.persist(bulk_two)
        
        models_one = self.get_all_models(self.ModelMergeOne, sort_key=sort_func)
        self.assertEqual(len(models_one), 4)
        
        models_two = self.get_all_models(self.ModelMergeTwo, sort_key=sort_func)
        self.assertEqual(len(models_two), 4)
        
        models_two = [m for m in models_two if m.f_integer in [101, 103]]
        
        merged_model = self.persister.merge_models(models_two)
        
        models_one = self.get_all_models(self.ModelMergeOne, sort_key=sort_func)
        self.assertEqual(len(models_one), 4)
        
        models_two = self.get_all_models(self.ModelMergeTwo, sort_key=sort_func)
        self.assertEqual(len(models_two), 3)
        
        self.assertEqual(merged_model.f_integer, 101)
        one_1_x = self.get_related_x_to_many(merged_model, 'one_1_x',
                                             sort_key=sort_func)
        self.assertEqual(len(one_1_x), 2)
        
        self.assertEqual(one_1_x[0].f_integer, 102)
        self.assertEqual(one_1_x[1].f_integer, 104)
        
        #--- x-to many not allowed ---------------------------------------------
        bulk_two = self.ItemMergeTwoX.Bulk()
        bulk_two.gen(f_integer=201,
                     one_1_x=[self.ItemMergeOneX(f_integer=202)])
        bulk_two.gen(f_integer=203,
                     one_1_x=[self.ItemMergeOneX(f_integer=202)])
        self.persister.persist(bulk_two)
        
        models_one = self.get_all_models(self.ModelMergeOneX, sort_key=sort_func)
        self.assertEqual(len(models_one), 2)
        
        models_two = self.get_all_models(self.ModelMergeTwoX, sort_key=sort_func)
        self.assertEqual(len(models_two), 2)
        
        merge_policy = MergePolicy(self.db_adapter, {
            self.ModelMergeTwoX: {
                'one_1_x': False
            }
        })
        models_two = [m for m in models_two if m.f_integer in [201, 203]]
        with self.assertRaises(MergeModelsNotAllowed):
            self.persister.merge_models(models_two, merge_policy=merge_policy)
        
    
    def test_merging_1_to_1_first_none(self):
        sort_func = lambda model: model.f_integer
        
        bulk_one = self.ItemMergeOne.Bulk()
        bulk_one.gen(f_integer=1)  # two_1_1 is None
        bulk_one.gen(f_integer=2,
                     two_1_1=self.ItemMergeTwo(f_integer=3))
        self.persister.persist(bulk_one)
        
        model_ones = self.get_all_models(self.ModelMergeOne, sort_key=sort_func)
        self.assertEqual(len(model_ones), 2)
        model_twos = self.get_all_models(self.ModelMergeTwo, sort_key=sort_func)
        self.assertEqual(len(model_twos), 1)
        
        merged_model = self.persister.merge_models(model_ones)
        
        model_ones = self.get_all_models(self.ModelMergeOne, sort_key=sort_func)
        self.assertEqual(len(model_ones), 1)
        model_twos = self.get_all_models(self.ModelMergeTwo, sort_key=sort_func)
        self.assertEqual(len(model_twos), 1)
        
        self.assertEqual(merged_model.f_integer, 1)
        self.assertEqual(merged_model.two_1_1.f_integer, 3)
        
        