import datetime

from save_to_db.core.scope import Scope
from save_to_db.core.item import Item
from save_to_db.utils.test_base import TestBase



class TestPersist(TestBase):
    
    ModelGeneralOne = None
    ModelGeneralTwo = None
    
    ModelAutoReverseOne = None
    ModelAutoReverseTwoA = None
    ModelAutoReverseTwoB = None
    ModelAutoReverseThreeA = None
    ModelAutoReverseThreeB = None
    ModelAutoReverseFourA = None
    ModelAutoReverseFourB = None
    
    
    def test_forward_and_reverse_relations_filters_one(self):
        # referencing parent and two
        
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = [{'parent_1_1'}, {'parent_x_1'}, {'parent_x_x'},
                        {'two_1_1'}, {'two_1_x'}, {'two_x_1'}, {'two_x_x'},
                        {'f_integer'}]
            getters = [{'parent_1_1'}, {'parent_x_1'}, 
                       {'two_1_1'}, {'two_x_1'}]
        
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
            creators = [{'f_integer'}]
            getters = [{'f_integer'}]
            
        persister = self.persister
        
        # parent_1_1
        item_parent_1_1 = ItemGeneralOne(f_string='parent_1_1',
                                         f_integer='101')
        item_child_1_1 = ItemGeneralOne(f_string='child_1_1',
                                        parent_1_1=item_parent_1_1)
        persister.persist(item_child_1_1)
        models = self.get_all_models(self.ModelGeneralOne)
        model = [m for m in models if m.f_string=='child_1_1'][0]
        self.assertEqual(model.parent_1_1.f_string, 'parent_1_1')
        model = [m for m in models if m.f_string=='parent_1_1'][0]
        self.assertEqual(model.child_1_1.f_string, 'child_1_1')
        
        # parent_x_1
        item_parent_x_1 = ItemGeneralOne(f_string='parent_x_1',
                                         f_integer='901')
        item_child_1_x = ItemGeneralOne(f_string='child_1_x',
                                        parent_x_1=item_parent_x_1)
        persister.persist(item_child_1_x)
        models = self.get_all_models(self.ModelGeneralOne)
        model = [m for m in models if m.f_string=='child_1_x'][0]
        self.assertEqual(model.parent_x_1.f_string, 'parent_x_1')
        model = [m for m in models if m.f_string=='parent_x_1'][0]
        child_1_x = self.get_related_x_to_many(model, 'child_1_x')
        self.assertEqual(len(child_1_x), 1)
        self.assertEqual(child_1_x[0].f_string, 'child_1_x')
        
        # two_1_1
        item_two_1_1 = ItemGeneralTwo(f_string='two_1_1',
                                      f_integer='101')
        item_one_1_1 = ItemGeneralOne(f_string='one_1_1',
                                      two_1_1=item_two_1_1)
        persister.persist(item_one_1_1)
        
        models = self.get_all_models(self.ModelGeneralOne)
        model = [m for m in models if m.f_string=='one_1_1'][0]
        self.assertEqual(model.two_1_1.f_string, 'two_1_1')
        models = self.get_all_models(self.ModelGeneralTwo)
        model = [m for m in models if m.f_string=='two_1_1'][0]
        self.assertEqual(model.one_1_1.f_string, 'one_1_1')
        
        # two_x_1
        item_two_x_1 = ItemGeneralTwo(f_string='two_x_1',
                                      f_integer='901')
        item_one_1_x = ItemGeneralOne(f_string='one_1_x',
                                      two_x_1=item_two_x_1)
        persister.persist(item_one_1_x)
        models = self.get_all_models(self.ModelGeneralOne)
        model = [m for m in models if m.f_string=='one_1_x'][0]
        self.assertEqual(model.two_x_1.f_string, 'two_x_1') 
        models = self.get_all_models(self.ModelGeneralTwo)
        model = [m for m in models if m.f_string=='two_x_1'][0]
        one_1_x = self.get_related_x_to_many(model, 'one_1_x')
        self.assertEqual(len(one_1_x), 1)
        self.assertEqual(one_1_x[0].f_string, 'one_1_x')
    
    
    def test_forward_and_reverse_relations_filters_two(self):
        # referencing child and one
        
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = [{'child_1_1'}, {'child_x_x'},
                        {'f_integer'}]
            getters = [{'child_1_1'},
                       {'two_1_1'}, {'two_x_1'},
                       {'f_string'}]
        
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
            creators = [{'one_1_1'}, {'one_1_x'}, {'one_x_1'}, {'one_x_x'},
                        {'f_integer'}]
            getters = [{'one_1_1'}, {'one_x_1'},
                       {'f_integer'}]
        
        persister = self.persister
        
        # child_1_1
        item_child_1_1 = ItemGeneralOne(f_string='child_1_1',
                                        f_integer='101')
        item_parent_1_1 = ItemGeneralOne(f_string='parent_1_1',
                                         child_1_1=item_child_1_1)
        persister.persist(item_parent_1_1)
        models = self.get_all_models(self.ModelGeneralOne)
        model = [m for m in models if m.f_string=='parent_1_1'][0]
        self.assertEqual(model.child_1_1.f_string, 'child_1_1')
        model = [m for m in models if m.f_string=='child_1_1'][0]
        self.assertEqual(model.parent_1_1.f_string, 'parent_1_1')
        
        # one_1_1
        item_one_1_1 = ItemGeneralOne(f_string='one_1_1',
                                      f_integer='1101')
        item_two_1_1 = ItemGeneralTwo(f_string='two_1_1',
                                      one_1_1=item_one_1_1)
        persister.persist(item_two_1_1)
        models = self.get_all_models(self.ModelGeneralTwo)
        model = [m for m in models if m.f_string=='two_1_1'][0]
        self.assertEqual(model.one_1_1.f_string, 'one_1_1')
        models = self.get_all_models(self.ModelGeneralOne)
        model = [m for m in models if m.f_string=='one_1_1'][0]
        self.assertEqual(model.two_1_1.f_string, 'two_1_1')
        
        # one_x_1
        item_one_x_1 = ItemGeneralOne(f_string='one_x_1',
                                      f_integer='1901')
        item_two_1_x = ItemGeneralTwo(f_string='two_1_x',
                                      one_x_1=item_one_x_1)
        persister.persist(item_two_1_x)
        models = self.get_all_models(self.ModelGeneralTwo)
        model = [m for m in models if m.f_string=='two_1_x'][0]
        self.assertEqual(model.one_x_1.f_string, 'one_x_1') 
        models = self.get_all_models(self.ModelGeneralOne)
        model = [m for m in models if m.f_string=='one_x_1'][0]
        two_1_x = self.get_related_x_to_many(model, 'two_1_x')
        self.assertEqual(len(two_1_x), 1)
        self.assertEqual(two_1_x[0].f_string, 'two_1_x')
    
    
    def test_forward_and_reverse_relations_persist(self):
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
        
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
        
        persister = self.persister
        
        #--- from item_one ---
        item_one = ItemGeneralOne()
        item_one['two_1_1'] = ItemGeneralTwo(f_integer='101')
        item_one['two_x_1'] = ItemGeneralTwo(f_integer='901')
        item_one['two_x_x'].gen(f_integer='909')
        
        persister.persist(item_one)
        models = self.get_all_models(self.ModelGeneralOne)
        
        self.assertEqual(len(models), 1)
        model = models[0]
        self.assertEqual(model.two_1_1.f_integer, 101)
        self.assertEqual(model.two_x_1.f_integer, 901)
        two_x_x = self.get_related_x_to_many(model, 'two_x_x')
        self.assertEqual(len(two_x_x), 1)
        self.assertEqual(two_x_x[0].f_integer, 909)
        
        #--- from item two ---
        item_two = ItemGeneralTwo(f_string='second item')
        item_two['one_1_1'] = ItemGeneralOne(f_integer='2101')
        item_two['one_x_1'] = ItemGeneralOne(f_integer='2901')
        item_two['one_x_x'].gen(f_integer='2909')
        
        persister.persist(item_two)
        models = self.get_all_models(self.ModelGeneralTwo)
        
        #self.assertEqual(len(models), 4)  # 3 before and 1 now
        model = [m for m in models if m.f_string=='second item'][0]
        self.assertEqual(model.one_1_1.f_integer, 2101)
        self.assertEqual(model.one_x_1.f_integer, 2901)
        one_x_x = self.get_related_x_to_many(model, 'one_x_x')
        self.assertEqual(len(one_x_x), 1)
        self.assertEqual(one_x_x[0].f_integer, 2909)
        
        #--- from self to self ---
        item_one = ItemGeneralOne(f_string='third item')
        # parent
        item_one['parent_1_1'] = ItemGeneralOne(f_integer='3101')
        item_one['parent_x_1'] = ItemGeneralOne(f_integer='3901')
        item_one['parent_x_x'].gen(f_integer='3909')
        # child
        item_one['child_1_1'] = ItemGeneralOne(f_integer='4101')
        item_one['child_1_x'].gen(f_integer='4109')
        item_one['child_x_x'].gen(f_integer='4909')
        
        persister.persist(item_one)
        models = self.get_all_models(self.ModelGeneralOne)
        model = [m for m in models if m.f_string=='third item'][0]
        
        # parent
        self.assertEqual(model.parent_1_1.f_integer, 3101)
        self.assertEqual(model.parent_x_1.f_integer, 3901)
        parent_x_x = self.get_related_x_to_many(model, 'parent_x_x')
        self.assertEqual(len(parent_x_x), 1)
        self.assertEqual(parent_x_x[0].f_integer, 3909)
        
        # child
        self.assertEqual(model.child_1_1.f_integer, 4101)
        child_1_x = self.get_related_x_to_many(model, 'child_1_x')
        self.assertEqual(len(child_1_x), 1)
        self.assertEqual(child_1_x[0].f_integer, 4109)
        child_x_x = self.get_related_x_to_many(model, 'child_x_x')
        self.assertEqual(len(child_x_x), 1)
        self.assertEqual(child_x_x[0].f_integer, 4909)
    
    
    def test_persist_bulk_item(self):
        class ItemGeneralOne(Item):
            allow_merge_items = True
            model_cls = self.ModelGeneralOne
            creators = [{'f_integer'}]
            getters = [{'f_integer'}, {'f_float'}]
        
        class ItemGeneralTwo(Item):
            allow_merge_items = True
            model_cls = self.ModelGeneralTwo
            creators = [{'f_integer'}]
            getters = [{'f_integer'}, {'f_float'}]
        
        persister = self.persister
        
        # generating 10 simple items
        bulk_one = ItemGeneralOne.Bulk()
        for i in range(10):
            bulk_one.gen(id=i, f_integer=i+100, f_float=i+1000)
        
        previous_bulk = bulk_one.bulk[:]
        items, model_lists = persister.persist(bulk_one)
        self.assertEqual(bulk_one.bulk, previous_bulk,
                         'Bulk was not changed after persistence')
        
        self.assertEqual(len(items), 10)
        self.assertEqual(len(items), len(model_lists))
        models = [model_entries[0] for model_entries in model_lists
                  if self.assertEqual(len(model_entries), 1) is None]
        models.sort(key=lambda model: model.id)
        loaded_models = self.get_all_models(self.ModelGeneralOne)
        self.assertEqual(len(models), 10)
        for i, model in enumerate(models):
            self.assertIn(model, loaded_models)
            self.assertEqual(model.id, i)
            self.assertEqual(model.f_integer, i+100)
            self.assertEqual(model.f_float, i+1000)
            self.assertIs(model.f_boolean, None)  # for future tests
        
        # generating 10 items that has previous 5 and new 5 items as relations
        bulk_two = ItemGeneralTwo.Bulk()
        for i in range(10):
            item = bulk_two.gen(id=i, f_integer=i+200, f_float=i+2000)
            if i < 5:
                # last five item ones will have twos with IDs from 0 to 4
                # (all `i` values), item twos from 5 to 9
                item['one_x_x'] = bulk_one[5:]
                item['one_x_x__f_boolean'] = 'true'
                
                if i == 1:
                    # items are from previously saved bulk
                    # item one at index zero has ID = 0,
                    # item two has ID = 1 (current `i`, current item)
                    item['one_1_1'] = items[0]
                    item['one_1_x'].add(items[0])
            else:
                for j in range(5, 10):
                    # generated items are the same for all iterations,
                    # item twos from 5 to 9 will have item ones with IDs
                    # from 600 to 604, item ones on the other side will have
                    # item twos with IDs from 5 to 9 (all `i` values)
                    item['one_x_x'].gen(id=j+600-5, f_integer=j+200-5,
                                        f_float=j+2000-5)
        
        items, model_lists = persister.persist(bulk_two)
        self.assertEqual(len(items), 10)
        self.assertEqual(len(items), len(model_lists))
        models = [model_entries[0] for model_entries in model_lists
                  if self.assertEqual(len(model_entries), 1) is None]
        
        # checking item twos ---------------------------------------------------
        
        # 5 items were not changed, 5 items were updated, 5 items were created
        all_models = self.get_all_models(self.ModelGeneralOne)
        all_models.sort(key=lambda model: model.id)
        self.assertEqual(len(all_models), 15)
        
        # checking fields (using IDs for relations)
        expected_values = [
            # first 5 items that were not changed
            dict(id=0, f_integer=100, f_float=1000.0, f_boolean=None,
                 two_1_1=1, two_x_1=1),
            dict(id=1, f_integer=101, f_float=1001.0, f_boolean=None),
            dict(id=2, f_integer=102, f_float=1002.0, f_boolean=None),
            dict(id=3, f_integer=103, f_float=1003.0, f_boolean=None),
            dict(id=4, f_integer=104, f_float=1004.0, f_boolean=None),
            # 5 items that were updated
            dict(id=5, f_integer=105, f_float=1005.0, f_boolean=True,
                 two_x_x=[0,1,2,3,4]),
            dict(id=6, f_integer=106, f_float=1006.0, f_boolean=True,
                 two_x_x=[0,1,2,3,4]),
            dict(id=7, f_integer=107, f_float=1007.0, f_boolean=True,
                 two_x_x=[0,1,2,3,4]),
            dict(id=8, f_integer=108, f_float=1008.0, f_boolean=True,
                 two_x_x=[0,1,2,3,4]),
            dict(id=9, f_integer=109, f_float=1009.0, f_boolean=True,
                 two_x_x=[0,1,2,3,4]),
            # 5 items that were created
            dict(id=600, f_integer=200, f_float=2000.0, f_boolean=None,
                 two_x_x=[5,6,7,8,9]),
            dict(id=601, f_integer=201, f_float=2001.0, f_boolean=None,
                 two_x_x=[5,6,7,8,9]),
            dict(id=602, f_integer=202, f_float=2002.0, f_boolean=None,
                 two_x_x=[5,6,7,8,9]),
            dict(id=603, f_integer=203, f_float=2003.0, f_boolean=None,
                 two_x_x=[5,6,7,8,9]),
            dict(id=604, f_integer=204, f_float=2004.0, f_boolean=None,
                 two_x_x=[5,6,7,8,9]),
        ]
        relations = {
            fname: direction
            for fname, _, direction, _ in persister.db_adapter.iter_relations(
                all_models[0].__class__)
        }
        for i, (expected, model) in enumerate(zip(expected_values, all_models)):
            for key, value in expected.items():
                if key not in relations:
                    model_value = getattr(model, key)
                    err_msg = '{}: {} = {}'.format(i, key, model_value)
                    if key != 'f_boolean':
                        self.assertEqual(model_value, value, err_msg)
                    else:
                        self.assertIs(model_value, value, err_msg)
                else:
                    if relations[key].is_x_to_many():
                        model_value = self.get_related_x_to_many(model, key)
                        ids = list(m.id for m in model_value)
                        ids.sort()
                        self.assertEqual(
                            ids, value,
                            '{}: {} = {}'.format(i, key, ids))
                    else:
                        model_value = getattr(model, key)
                        self.assertEqual(
                            model_value.id, value,
                            '{}: {} = {}'.format(i, key, model_value.id))
        
        # checking item ones ---------------------------------------------------
        
        # 10 items were created, other creations or no changes were made
        # (5 items were reused, 5 items were created)
        all_models = self.get_all_models(self.ModelGeneralTwo)
        all_models.sort(key=lambda model: model.id)
        self.assertEqual(len(all_models), 10)
        
        expected_values = [
            dict(id=0, f_integer=200, f_float=2000.0,
                 one_x_x=[5,6,7,8,9]),
            dict(id=1, f_integer=201, f_float=2001.0,
                 one_x_x=[5,6,7,8,9],
                 one_1_1=0, one_1_x=[0]),
            dict(id=2, f_integer=202, f_float=2002.0,
                 one_x_x=[5,6,7,8,9]),
            dict(id=3, f_integer=203, f_float=2003.0,
                 one_x_x=[5,6,7,8,9]),
            dict(id=4, f_integer=204, f_float=2004.0,
                 one_x_x=[5,6,7,8,9]),
            
            dict(id=5, f_integer=205, f_float=2005.0,
                 one_x_x=[600,601,602,603,604]),
            dict(id=6, f_integer=206, f_float=2006.0,
                 one_x_x=[600,601,602,603,604]),
            dict(id=7, f_integer=207, f_float=2007.0,
                 one_x_x=[600,601,602,603,604]),
            dict(id=8, f_integer=208, f_float=2008.0,
                 one_x_x=[600,601,602,603,604]),
            dict(id=9, f_integer=209, f_float=2009.0,
                 one_x_x=[600,601,602,603,604]),
        ]
        relations = {
            fname: direction
            for fname, _, direction, _ in persister.db_adapter.iter_relations(
                all_models[0].__class__)
        }
        for i, (expected, model) in enumerate(zip(expected_values, all_models)):
            for key, value in expected.items():
                if key not in relations:
                    model_value = getattr(model, key)
                    err_msg = '{}: {} = {}'.format(i, key, model_value)
                    self.assertEqual(model_value, value, err_msg)
                else:
                    if relations[key].is_x_to_many():
                        model_value = self.get_related_x_to_many(model, key)
                        ids = list(m.id for m in model_value)
                        ids.sort()
                        self.assertEqual(
                            ids, value,
                            '{}: {} = {}'.format(i, key, ids))
                    else:
                        model_value = getattr(model, key)
                        self.assertEqual(
                            model_value.id, value,
                            '{}: {} = {}'.format(i, key, model_value.id))
    
    
    def test_persist_no_reverse_relations(self):
        class ItemAutoReverseOne(Item):
            model_cls = self.ModelAutoReverseOne
        
        class ItemAutoReverseTwoA(Item):
            model_cls = self.ModelAutoReverseTwoA
        
        class ItemAutoReverseTwoB(Item):
            model_cls = self.ModelAutoReverseTwoB
        
        class ItemAutoReverseThreeA(Item):
            model_cls = self.ModelAutoReverseThreeA
        
        class ItemAutoReverseThreeB(Item):
            model_cls = self.ModelAutoReverseThreeB
        
        class ItemAutoReverseFourA(Item):
            model_cls = self.ModelAutoReverseFourA
        
        class ItemAutoReverseFourB(Item):
            model_cls = self.ModelAutoReverseFourB

        
        item = ItemAutoReverseOne(f_string='one')
        
        item['two_b_1_1'] = ItemAutoReverseTwoB(f_string='two_b_1_1')
        item['three_b_x_1'] = ItemAutoReverseThreeB(f_string='three_b_x_1')
        item['four_b_x_x'].gen(f_string='four_b_x_x_first')
        item['four_b_x_x'].gen(f_string='four_b_x_x_second')
        
        persister = self.persister
        _, models_one_list = persister.persist(item)
        self.assertTrue(len(models_one_list), 1)
        models_one = models_one_list[0]
        self.assertTrue(len(models_one), 1)
        model_one_returned = models_one[0]
        
        # one
        models_one = self.get_all_models(self.ModelAutoReverseOne)
        self.assertEqual(len(models_one), 1)
        model_one = models_one[0]
        
        self.assertEqual(model_one, model_one_returned)
        
        # two
        models_two = self.get_all_models(self.ModelAutoReverseTwoB)
        self.assertEqual(len(models_two), 1)
        model_two = models_two[0]
        
        self.assertEqual(model_one.two_b_1_1, model_two)
        
        # three
        models_three = self.get_all_models(self.ModelAutoReverseThreeB)
        self.assertEqual(len(models_three), 1)
        model_three = models_three[0]
        
        self.assertEqual(model_one.three_b_x_1, model_three)
        
        # four
        sort_func = lambda model: model.f_string
        
        models_four = self.get_all_models(self.ModelAutoReverseFourB,
                                          sort_key=sort_func)
        self.assertEqual(len(models_four), 2)
        
        related_models_four = self.get_related_x_to_many(model_one,
                                                         'four_b_x_x',
                                                         sort_key=sort_func)
        self.assertEqual(len(related_models_four), 2)
        for model_four, related_model_for in zip(models_four,
                                                 related_models_four):
            self.assertEqual(model_four, related_model_for)
    
    
    def test_persist_single_item_no_related(self):
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = [{'f_integer'}]
            getters = [{'f_float'}, {'f_string', 'f_text'},
                       {'f_date'}]
        
        # need this for `ItemGeneralOne` (related field)
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
                
        persister = self.persister
        
        # creating and updating first model ------------------------------------
        
        # cannot create or get
        item = ItemGeneralOne(f_string='str-one')
        items, model_lists = persister.persist(item)
        self.assertFalse(items)
        self.assertFalse(model_lists)
        
        # can get but not create and not in database
        item['f_text'] = 'text-one'
        items, model_lists = persister.persist(item)
        self.assertFalse(items)
        self.assertFalse(model_lists)
        
        # can create
        item['f_integer'] = None  # `None` can create
        items, model_lists = persister.persist(item)
        self.assertEqual(len(items), 1)
        self.assertEqual(len(items), len(model_lists))
        models = model_lists[0]
        self.assertEqual(len(models), 1)
        self.assertIs(items[0], item)
        
        self.assertEqual(models[0].f_string, 'str-one')
        self.assertEqual(models[0].f_text, 'text-one')
        self.assertEqual(models[0].f_integer, None)
        self.assertEqual(models[0].f_date, None)
        
        # can update (`{'f_string', 'f_text'}` are the getters)
        
        # `f_date=None` will be used as getter later
        item['f_date'] = '2010-10-10'
        
        item['f_integer'] = '100'
        items, model_lists = persister.persist(item)
        self.assertEqual(len(items), 1)
        self.assertEqual(len(items), len(model_lists))
        models = model_lists[0]
        self.assertEqual(len(models), 1)
        self.assertIs(items[0], item)
        
        # checking that model got the same values
        self.assertEqual(models[0].f_string, 'str-one')
        self.assertEqual(models[0].f_text, 'text-one')
        self.assertEqual(models[0].f_integer, 100)
        self.assertEqual(models[0].f_date, datetime.date(2010, 10, 10))
        
        first_model = models[0]
        
        # creating second model ------------------------------------------------
        
        item = ItemGeneralOne(f_integer='200', f_string='str-one')
        items, model_lists = persister.persist(item)
        self.assertEqual(len(items), 1)
        self.assertEqual(len(items), len(model_lists))
        models = model_lists[0]
        self.assertEqual(len(models), 1)
        self.assertIs(items[0], item)
        
        second_model = models[0]
        self.assertNotEqual(models[0], first_model)
        self.assertEqual(models[0].f_string, 'str-one')
        self.assertEqual(models[0].f_integer, 200)
        
        # updating first and second model --------------------------------------
        
        # updating second model
        item = ItemGeneralOne(f_date=None)  # `None` value can be used
        items, model_lists = persister.persist(item)
        self.assertEqual(len(models), 1)
        self.assertIs(items[0], item)
        models = model_lists[0]
        self.assertEqual(len(models), 1)
        self.assertIs(items[0], item)
        
        self.assertEqual(models[0], second_model)
        self.assertEqual(models[0].f_integer, 200)
        self.assertEqual(models[0].f_string, 'str-one')
        self.assertEqual(models[0].f_text, None)
        self.assertIs(models[0].f_boolean, None)
        self.assertIs(models[0].f_date, None)
        
        # updating second model
        self.assertIs(first_model.f_boolean, None)  # will be `True` later
        item['f_string'] = 'str-one'
        item['f_text'] = 'text-one'
        item['f_boolean'] = True
        item['f_date'] = '2015-10-10'
        
        items, model_lists = persister.persist(item)
        self.assertEqual(len(items), 1)
        self.assertEqual(len(items), len(model_lists))
        models = model_lists[0]
        self.assertEqual(len(models), 1)
        self.assertIs(items[0], item)
        
        self.assertEqual(models[0], first_model)
        self.assertEqual(models[0].f_integer, 100)
        self.assertEqual(models[0].f_string, 'str-one')
        self.assertEqual(models[0].f_text, 'text-one')
        self.assertIs(models[0].f_boolean, True)
        self.assertEqual(models[0].f_date, datetime.date(2015, 10, 10))

        # return boolean to `None`
        item['f_boolean'] = None
        items, (models,) = persister.persist(item)
        self.assertEqual(models[0], first_model)
        self.assertIs(models[0].f_boolean, None)
    
    
    def test_persist_single_item_with_single_related(self):
        model_one_cls = self.ModelGeneralOne
        model_two_cls = self.ModelGeneralTwo
        
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = [{'f_integer', 'two_1_1'}]
            getters = [{'f_integer', 'two_1_1'},
                       {'f_float'},
                       {'f_string', 'f_text'},
                       {'f_date'}]
        
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
            creators = [{'f_integer'}]
            getters = [{'f_integer'}]
        
        persister = self.persister
        
        # cannot create any items
        # 'two_1_1' is not present 
        item_one = ItemGeneralOne(f_integer='100')
        items, model_lists = persister.persist(item_one)
        self.assertEqual(len(items), 0)
        self.assertEqual(len(items), len(model_lists))
        
        # 'two_1_1' cannot be created
        item_two = ItemGeneralTwo(f_float='20.20')
        items, model_lists = persister.persist(item_two)
        self.assertEqual(len(items), 0)
        self.assertEqual(len(items), len(model_lists))
        
        item_one['two_1_1'] = item_two
        items, model_lists = persister.persist(item_one)
        self.assertEqual(len(items), 0)
        self.assertEqual(len(items), len(model_lists))
        
        self.assertEqual(len(self.get_all_models(model_one_cls)), 0)
        self.assertEqual(len(self.get_all_models(model_two_cls)), 0)
        
        # 'two_1_1' can be created
        item_two['f_integer'] = '200'
        del item_one['f_integer']  # won't be persisted
        items, model_lists = persister.persist(item_one)
        self.assertEqual(len(items), 0)
        self.assertEqual(len(items), len(model_lists))
        
        self.assertEqual(len(self.get_all_models(model_one_cls)), 0)
        # but `item_two` was persisted
        models_two = self.get_all_models(model_two_cls)
        self.assertEqual(len(models_two), 1)
        self.assertEqual(models_two[0].f_integer, 200)
        self.assertEqual(models_two[0].f_float, 20.2)
        
        # persisting item_one with updating existing model
        self.assertIs(models_two[0].f_boolean, None)
        item_one['f_integer'] = '100'
        item_two['f_boolean'] = True
        
        items, model_lists = persister.persist(item_one)
        self.assertEqual(len(items), 1)
        self.assertEqual(len(items), len(model_lists))
        self.assertEqual(len(model_lists), 1)
        models = model_lists[0]
        self.assertEqual(len(models), 1)
        self.assertIs(items[0], item_one)
        
        self.assertEqual(models[0].f_integer, 100)
        self.assertIsNotNone(models[0].two_1_1)
        self.assertIsNotNone(models[0].two_1_1.f_integer, 200)
        self.assertIsNotNone(models[0].two_1_1.f_float, 20.2)
        self.assertIs(models[0].two_1_1.f_boolean, True)
        
        self.assertEqual(len(self.get_all_models(model_one_cls)), 1)
        self.assertEqual(len(self.get_all_models(model_two_cls)), 1)
        
        # persisting using related item as filter
        del item_two['one_1_1']  # old item
        item_one = ItemGeneralOne(f_integer='100', two_1_1=item_two)
        item_one['f_boolean'] = False
        
        items, model_lists = persister.persist(item_one)
        
        self.assertEqual(len(items), 1)
        self.assertEqual(len(items), len(model_lists))
        self.assertEqual(len(model_lists), 1)
        models = model_lists[0]
        self.assertEqual(len(models), 1)
        self.assertIs(items[0], item_one)
        self.assertIs(models[0].f_boolean, False)
        
        self.assertEqual(len(self.get_all_models(model_one_cls)), 1)
        self.assertEqual(len(self.get_all_models(model_two_cls)), 1)
    
    
    def test_persist_single_item_with_bulk_related(self):
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = [{'id'}]
            getters = [{'id'}]
        
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
            creators = [{'id'}]
            getters = [{'id'}]
        
        persister = self.persister
        
        item_one = ItemGeneralOne(id='5', f_float='50.50')
        item_one(two_1_1=ItemGeneralTwo(id='10', f_string='1-to-1'),
                 two_x_1=ItemGeneralTwo(id='20', f_string='X-to-1'))
        bulk = item_one['two_1_x']
        bulk.gen(id='30', f_string='1-to-x first')
        bulk.gen(id='40', f_string='1-to-x second')
        bulk = item_one['two_x_x']
        bulk.gen(id='50', f_string='x-to-x first')
        bulk.gen(id='60', f_string='x-to-x second')
        
        items, model_lists = persister.persist(item_one)
        
        self.assertEqual(len(items), 1)
        self.assertEqual(len(items), len(model_lists))
        models = model_lists[0]
        self.assertEqual(len(models), 1)
        self.assertIs(items[0], item_one)
        
        # checking model data
        model = models[0]
        self.assertEqual(model.id, 5)
        self.assertEqual(model.f_float, 50.5)
        
        self.assertIsNotNone(model.two_1_1)
        self.assertEqual(model.two_1_1.id, 10)
        self.assertEqual(model.two_1_1.f_string, '1-to-1')
        
        two_1_x = self.get_related_x_to_many(model, 'two_1_x')
        two_1_x.sort(key=lambda model: model.id)
        self.assertEqual(len(two_1_x), 2)
        self.assertEqual(two_1_x[0].id, 30)
        self.assertEqual(two_1_x[0].f_string, '1-to-x first')
        self.assertEqual(two_1_x[1].id, 40)
        self.assertEqual(two_1_x[1].f_string, '1-to-x second')
        
        two_x_x = self.get_related_x_to_many(model, 'two_x_x')
        two_x_x.sort(key=lambda model: model.id)
        self.assertEqual(len(two_x_x), 2)
        self.assertEqual(two_x_x[0].id, 50)
        self.assertEqual(two_x_x[0].f_string, 'x-to-x first')
        self.assertEqual(two_x_x[1].id, 60)
        self.assertEqual(two_x_x[1].f_string, 'x-to-x second')
    
    
    def test_persist_single_item_with_x_to_many_related(self):
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = [{'f_string'}]
            getters = [{'two_1_x'}, {'f_string'}]
        
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
            creators = [{'f_string'}]
            getters = [{'f_string'}]
        
        persister = self.persister
        
        # creating first set of items
        item_one_bulk = ItemGeneralOne.Bulk()
        for (item_name, known_names) in [['one', ['first', 'one',]],
                                         ['two', ['second', 'two']]]:
            item_one = item_one_bulk.gen(f_string=item_name)
            for known_name in known_names:
                item_one['two_1_x'].gen(f_string=known_name)
            
        persister.persist(item_one_bulk)
        
        # creating second set of items
        # (`item_one` instance with name "one" must match 
        #  item with name "one_more" through "first" known name)
        item_one_bulk = ItemGeneralOne.Bulk()
        for (item_name, known_names) in [['one_more', ['first', 'one_more',]],
                                         ['three', ['third', 'three']]]:
            item_one = item_one_bulk.gen(f_string=item_name)
            for known_name in known_names:
                item_one['two_1_x'].gen(f_string=known_name)
            
        persister.persist(item_one_bulk)
        
        # updating two models (testing mathing x-to-many)
        item_one_bulk = ItemGeneralOne.Bulk()
        for (item_name, known_names) in [['two_more', ['second', 'two',
                                                       'two_more',]],
                                         ['three_more', ['third', 'three',
                                                         'three_more']]]:
            item_one = item_one_bulk.gen(f_string=item_name)
            for known_name in known_names:
                item_one['two_1_x'].gen(f_string=known_name)
        
        persister.persist(item_one_bulk)
        
        # checking the models
        sort_func = lambda model: model.f_string
        models_one = self.get_all_models(self.ModelGeneralOne,
                                         sort_key=sort_func)
        self.assertEqual(len(models_one), 3)
        
        expected = [['one_more', ['first', 'one', 'one_more']],
                    ['two_more', ['second', 'two', 'two_more']],
                    ['three_more', ['third', 'three', 'three_more']]]
        expected.sort(key=lambda entry: entry[0])
        
        for i, (expected_name, expected_known_names) in enumerate(expected):
            
            model_one = models_one[i]
            self.assertEqual(model_one.f_string, expected_name)
            
            models_two = self.get_related_x_to_many(model_one, 'two_1_x',
                                                    sort_func)
            actual_known_names = [model_two.f_string
                                  for model_two in models_two]
            known_names.sort()
            self.assertEqual(actual_known_names, expected_known_names)
    
    
    def test_persist_with_scope(self):
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = [{'f_integer'}]
            getters = [{'f_integer'}]
        
        # need this for `ItemGeneralOne` (related field)
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
            creators = [{'f_integer'}]
            getters = [{'f_integer'}]
            
        scope = Scope(
            {
                ItemGeneralOne: {
                    'creators': ['f_integer', 'f_float'],
                    'getters': ['f_integer', 'f_float'],
                }
            },
            collection_id='test_persist_with_scope')
        
        self.assertNotIsInstance(scope[ItemGeneralOne], ItemGeneralOne)
        
        persister = self.persister
        
        # not scoped
        item_one = ItemGeneralOne(f_integer='100', f_float='200')
        item_one_dump = persister.dumps(item_one)
        item_one_load = persister.loads(item_one_dump)
        self.assertIsInstance(item_one_load, ItemGeneralOne)
        
        
        item_one_scoped = scope[ItemGeneralOne](f_integer='300', f_float='400')
        item_one_scoped_dump = persister.dumps(item_one_scoped)
        item_one_scoped_load = persister.loads(item_one_scoped_dump)
        self.assertIsInstance(item_one_scoped_load, scope[ItemGeneralOne])
    
    
    def test_one_to_many_creator(self):
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = ['two_1_x']
        
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
            creators = ['f_integer']
        
        persister = self.persister
        
        # failed creation    
        item_1 = ItemGeneralOne()
        item_1['two_1_x']  # access creates
        
        items, model_lists = persister.persist(item_1)
        self.assertEqual(len(items), 0)
        self.assertEqual(len(model_lists), 0)
        
        # successful creation
        item_1['two_1_x'].gen(f_integer=10)
        items, model_lists = persister.persist(item_1)
        self.assertEqual(len(items), 1)
        self.assertEqual(len(model_lists), 1)
        self.assertEqual(len(model_lists[0]), 1)
        self.assertEqual(len(self.get_all_models(self.ModelGeneralOne)), 1)
        self.assertEqual(len(self.get_all_models(self.ModelGeneralTwo)), 1)
        
        model = model_lists[0][0]
        two_1_x = self.get_related_x_to_many(model, 'two_1_x')
        self.assertEqual(len(two_1_x), 1)
        self.assertEqual(two_1_x[0].f_integer, 10)
    
    
    def test_many_to_many_creator(self):
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = ['two_x_x']
        
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
            creators = ['f_integer']
        
        persister = self.persister
        
        # failed creation    
        item_1 = ItemGeneralOne()
        item_1['two_x_x']  # access creates
        
        items, model_lists = persister.persist(item_1)
        self.assertEqual(len(items), 0)
        self.assertEqual(len(model_lists), 0)
        
        # successful creation
        item_1['two_x_x'].gen(f_integer=10)
        items, model_lists = persister.persist(item_1)
        self.assertEqual(len(items), 1)
        self.assertEqual(len(model_lists), 1)
        self.assertEqual(len(model_lists[0]), 1)
        self.assertEqual(len(self.get_all_models(self.ModelGeneralOne)), 1)
        self.assertEqual(len(self.get_all_models(self.ModelGeneralTwo)), 1)
        
        model = model_lists[0][0]
        two_x_x = self.get_related_x_to_many(model, 'two_x_x')
        self.assertEqual(len(two_x_x), 1)
        self.assertEqual(two_x_x[0].f_integer, 10)
    
    
    def test_x_to_many_getters(self):
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = ['f_integer']
            getters = ['f_string']
        
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
            creators = ['f_integer']
            getters = ['one_x_x']
        
        persister = self.persister
        
        item_one = ItemGeneralOne(f_integer='1', f_string='str-1')
        item_two = ItemGeneralTwo(f_integer='2', one_x_x=[item_one])

        persister.persist(item_two)
        self.assertEqual(len(self.get_all_models(self.ModelGeneralOne)), 1)
        self.assertEqual(len(self.get_all_models(self.ModelGeneralTwo)), 1)
        
        item_one = ItemGeneralOne(f_string='str-1')
        item_two = ItemGeneralTwo(f_string='str-2', one_x_x=[item_one])
        
        persister.persist(item_two)
        self.assertEqual(len(self.get_all_models(self.ModelGeneralOne)), 1)
        self.assertEqual(len(self.get_all_models(self.ModelGeneralTwo)), 1)
        
        model_one = self.get_all_models(self.ModelGeneralOne)[0]
        model_two = self.get_all_models(self.ModelGeneralTwo)[0]
        
        self.assertEqual(model_one.f_integer, 1)
        self.assertEqual(model_one.f_string, 'str-1')
        related_two = self.get_related_x_to_many(model_one, 'two_x_x')
        self.assertEqual(len(related_two), 1)
        self.assertEqual(model_two, related_two[0])
        
        self.assertEqual(model_two.f_integer, 2)
        self.assertEqual(model_two.f_string, 'str-2')
        related_one = self.get_related_x_to_many(model_two, 'one_x_x')
        self.assertEqual(len(related_one), 1)
        self.assertEqual(model_one, related_one[0])
    
    
    def test_null_getters_and_creators(self):
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = [{'f_integer', 'f_float', 'f_string', 'f_text'}]
            getters = [{'f_integer', 'f_string'}]
            nullables = ['f_string']
        
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
        
        persister = self.persister
        get_key = lambda model: (model.f_string if model.f_string else '-',
                                 model.f_float,
                                 model.f_integer,
                                 model.f_text)
        
        bulk_item = ItemGeneralOne.Bulk()
        for i in range(3):
            item = bulk_item.gen(
                f_integer=i+1,
                f_string='str-{}'.format(i+1) if i > 1 else None,
                f_text='text-{}'.format(i+1))
            if i != 0:
                item['f_float'] = i+1 + (i+1)/10
        persister.persist(bulk_item)
        
        model_ones = self.get_all_models(self.ModelGeneralOne,
                                         sort_key=get_key)
        model_one_keys = [get_key(model) for model in model_ones]
        expect = [
            # first item cannot be created (missing `f_float`)
            # '-' stands for `None` string (otherwise not sortable)
            ('-', 2.2, 2, 'text-2'),
            ('str-3', 3.3, 3, 'text-3'),
        ]
        self.assertEqual(model_one_keys, expect)
        
        bulk_item = ItemGeneralOne.Bulk()
        for i in range(3):
            item = bulk_item.gen(
                f_integer=i+1,
                f_string='str-{}'.format(i+1) if i > 1 else None,
                f_text='text-{}'.format(i+1 + 100))
            if i != 0:
                item['f_float'] = i+1 + (i+1)/10
        persister.persist(bulk_item)
        
        model_ones = self.get_all_models(self.ModelGeneralOne,
                                         sort_key=get_key)
        model_one_keys = [get_key(model) for model in model_ones]
        expect = [
            ('-', 2.2, 2, 'text-102'),
            ('str-3', 3.3, 3, 'text-103'),
        ]
        self.assertEqual(model_one_keys, expect)
    
    
    def test_one_to_many_getter(self):
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = ['f_integer']
            getters = ['f_integer', 'two_1_x']
        
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
            creators = ['f_integer']
            getters = ['f_integer']
        
        persister = self.persister
        
        # creating dummy records
        bulk_item_one = ItemGeneralOne.Bulk()
        bulk_item_two = ItemGeneralTwo.Bulk()
        for f_integer in range(1, 4):  # 1..3
            bulk_item_one.gen(f_integer=1000+f_integer)
            bulk_item_two.gen(f_integer=1000+f_integer)
        
        persister.persist(bulk_item_one)
        persister.persist(bulk_item_two)
        
        #--- one-to-many -------------------------------------------------------
        
        # creating item one
        item_one = ItemGeneralOne(f_integer=2001)  # new
        item_one['two_1_x'].gen(f_integer=1003)  # old
        item_one['two_1_x'].gen(f_integer=1004)  # new
        
        _, model_lists = persister.persist(item_one)
        
        self.assertEqual(len(self.get_all_models(self.ModelGeneralOne)), 4)
        self.assertEqual(len(self.get_all_models(self.ModelGeneralTwo)), 4)
        self.assertEqual(len(model_lists), 1)
        self.assertEqual(len(model_lists[0]), 1)
        
        model = model_lists[0][0]
        two_1_x = self.get_related_x_to_many(model, 'two_1_x')
        self.assertEqual(len(two_1_x), 2)
        two_1_x.sort(key=lambda m: m.f_integer)
        self.assertEqual(two_1_x[0].f_integer, 1003)
        self.assertEqual(two_1_x[1].f_integer, 1004)
        
        # updating item one
        item_one = ItemGeneralOne()  # old, will be found by "two_1_x"
        item_one['two_1_x'].gen(f_integer=1004)  # old
        item_one['two_1_x'].gen(f_integer=1005)  # new
        
        _, model_lists = persister.persist(item_one)
        self.assertEqual(len(self.get_all_models(self.ModelGeneralOne)), 4)
        self.assertEqual(len(self.get_all_models(self.ModelGeneralTwo)), 5)
        self.assertEqual(len(model_lists), 1)
        self.assertEqual(len(model_lists[0]), 1)
        
        model = model_lists[0][0]
        self.assertEqual(model.f_integer, 2001)
        two_1_x = self.get_related_x_to_many(model, 'two_1_x')
        self.assertEqual(len(two_1_x), 3)
        two_1_x.sort(key=lambda m: m.f_integer)
        self.assertEqual(two_1_x[0].f_integer, 1003)
        self.assertEqual(two_1_x[1].f_integer, 1004)
        self.assertEqual(two_1_x[2].f_integer, 1005)
        
        # empty bulk must be ignored
        item_one = ItemGeneralOne()
        item_one['two_1_x']  # accessing the bulk creates it
        items, model_lists = persister.persist(item_one)
        self.assertEqual(len(items), 0)
        self.assertEqual(len(model_lists), 0)
        # nothing changed
        self.assertEqual(len(self.get_all_models(self.ModelGeneralOne)), 4)
        self.assertEqual(len(self.get_all_models(self.ModelGeneralTwo)), 5)
        
        
    def test_many_to_many_getter(self):
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = ['f_integer']
            getters = ['f_integer']
        
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
            creators = ['f_integer']
            getters = ['f_integer', 'one_x_x']
        
        persister = self.persister
        
        # creating dummy records
        bulk_item_one = ItemGeneralOne.Bulk()
        bulk_item_two = ItemGeneralTwo.Bulk()
        for f_integer in range(1, 4):  # 1..3
            bulk_item_one.gen(f_integer=1000+f_integer)
            bulk_item_two.gen(f_integer=1000+f_integer)
        
        persister.persist(bulk_item_one)
        persister.persist(bulk_item_two)
        
        #--- many-to-many ------------------------------------------------------
        
        # creating item two
        item_two = ItemGeneralTwo(f_integer=2001)  # new
        item_two['one_x_x'].gen(f_integer=1003)  # old
        item_two['one_x_x'].gen(f_integer=1004)  # new
        
        _, model_lists = persister.persist(item_two)
        
        self.assertEqual(len(self.get_all_models(self.ModelGeneralOne)), 4)
        self.assertEqual(len(self.get_all_models(self.ModelGeneralTwo)), 4)
        self.assertEqual(len(model_lists), 1)
        self.assertEqual(len(model_lists[0]), 1)
        
        model = model_lists[0][0]
        one_x_x = self.get_related_x_to_many(model, 'one_x_x')
        self.assertEqual(len(one_x_x), 2)
        one_x_x.sort(key=lambda m: m.f_integer)
        self.assertEqual(one_x_x[0].f_integer, 1003)
        self.assertEqual(one_x_x[1].f_integer, 1004)
        
        # updating item one
        item_two = ItemGeneralTwo()  # old, will be found by "one_x_x"
        item_two['one_x_x'].gen(f_integer=1004)  # old
        item_two['one_x_x'].gen(f_integer=1005)  # new
        
        _, model_lists = persister.persist(item_two)
        self.assertEqual(len(self.get_all_models(self.ModelGeneralOne)), 5)
        self.assertEqual(len(self.get_all_models(self.ModelGeneralTwo)), 4)
        self.assertEqual(len(model_lists), 1)
        self.assertEqual(len(model_lists[0]), 1)
        
        model = model_lists[0][0]
        self.assertEqual(model.f_integer, 2001)
        one_x_x = self.get_related_x_to_many(model, 'one_x_x')
        self.assertEqual(len(one_x_x), 3)
        one_x_x.sort(key=lambda m: m.f_integer)
        self.assertEqual(one_x_x[0].f_integer, 1003)
        self.assertEqual(one_x_x[1].f_integer, 1004)
        self.assertEqual(one_x_x[2].f_integer, 1005)
        
        # empty bulk must be ignored
        item_two = ItemGeneralTwo()
        item_two['one_x_x']  # accessing the bulk creates it
        items, model_lists = persister.persist(item_two)
        self.assertEqual(len(items), 0)
        self.assertEqual(len(model_lists), 0)
        # nothing changed
        self.assertEqual(len(self.get_all_models(self.ModelGeneralOne)), 5)
        self.assertEqual(len(self.get_all_models(self.ModelGeneralTwo)), 4)
    
    
    def test_one_to_many_getter_mix(self):
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = ['f_integer']
            getters = ['f_integer']
        
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
            creators = ['f_integer']
            getters = ['f_integer', {'f_float', 'one_1_x'}]
        
        persister = self.persister
        
        # creating dummy records
        bulk_item_one = ItemGeneralOne.Bulk()
        bulk_item_two = ItemGeneralTwo.Bulk()
        for f_integer in range(1, 4):  # 1..3
            bulk_item_one.gen(f_integer=1000+f_integer,
                              f_float=1000.1+f_integer)
            bulk_item_two.gen(f_integer=1000+f_integer,
                              f_float=1000.1+f_integer)
        
        persister.persist(bulk_item_one)
        persister.persist(bulk_item_two)
        
        #--- mix with regular filter -------------------------------------------
        
        # creating item_two
        item_two = ItemGeneralTwo(f_integer=2001, f_float=2001.2)  # new
        item_two['one_1_x'].gen(f_integer=1003)  # old
        item_two['one_1_x'].gen(f_integer=1004)  # new
        
        _, model_lists = persister.persist(item_two)
        
        self.assertEqual(len(self.get_all_models(self.ModelGeneralOne)), 4)
        self.assertEqual(len(self.get_all_models(self.ModelGeneralTwo)), 4)
        self.assertEqual(len(model_lists), 1)
        self.assertEqual(len(model_lists[0]), 1)
        
        model = model_lists[0][0]
        one_1_x = self.get_related_x_to_many(model, 'one_1_x')
        self.assertEqual(len(one_1_x), 2)
        one_1_x.sort(key=lambda m: m.f_integer)
        self.assertEqual(one_1_x[0].f_integer, 1003)
        self.assertEqual(one_1_x[1].f_integer, 1004)
        
        # updating item
        # (can find by `f_float`, but item from `one_1_x` is not there)
        item_two = ItemGeneralTwo(f_float=2001.2)
        item_two['one_1_x'].gen(f_integer=1001)  # old
        
        _, model_lists = persister.persist(item_two)
        self.assertEqual(len(self.get_all_models(self.ModelGeneralOne)), 4)
        self.assertEqual(len(self.get_all_models(self.ModelGeneralTwo)), 4)
        self.assertEqual(len(model_lists), 0)
        
        # (can find by `one_1_x`, but `f_float` does not match)
        item_two = ItemGeneralTwo(f_float=2002.2)
        item_two['one_1_x'].gen(f_integer=1004)  # old
        
        _, model_lists = persister.persist(item_two)
        self.assertEqual(len(self.get_all_models(self.ModelGeneralOne)), 4)
        self.assertEqual(len(self.get_all_models(self.ModelGeneralTwo)), 4)
        self.assertEqual(len(model_lists), 0)
        
        # (empty bulk)
        item_two = ItemGeneralTwo(f_float=2002.2)
        item_two['one_1_x']  # accessing bulk creates it
        
        _, model_lists = persister.persist(item_two)
        self.assertEqual(len(self.get_all_models(self.ModelGeneralOne)), 4)
        self.assertEqual(len(self.get_all_models(self.ModelGeneralTwo)), 4)
        
        # now update must succeed
        item_two = ItemGeneralTwo(f_float=2001.2)
        item_two['one_1_x'].gen(f_integer=1004)  # old
        item_two['one_1_x'].gen(f_integer=1005)  # new
        
        _, model_lists = persister.persist(item_two)
        self.assertEqual(len(self.get_all_models(self.ModelGeneralOne)), 5)
        self.assertEqual(len(self.get_all_models(self.ModelGeneralTwo)), 4)
        
        self.assertEqual(len(model_lists), 1)
        self.assertEqual(len(model_lists[0]), 1)
        model = model_lists[0][0]
        one_1_x = self.get_related_x_to_many(model, 'one_1_x')
        self.assertEqual(len(one_1_x), 3)
        one_1_x.sort(key=lambda m: m.f_integer)
        self.assertEqual(one_1_x[0].f_integer, 1003)
        self.assertEqual(one_1_x[1].f_integer, 1004)
        self.assertEqual(one_1_x[2].f_integer, 1005)
        
    
    def test_many_to_many_getter_mix(self):
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = ['f_integer']
            getters = ['f_integer']
        
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
            creators = ['f_integer']
            getters = ['f_integer', {'f_float', 'one_x_x'}]
        
        persister = self.persister
        
        # creating dummy records
        bulk_item_one = ItemGeneralOne.Bulk()
        bulk_item_two = ItemGeneralTwo.Bulk()
        for f_integer in range(1, 4):  # 1..3
            bulk_item_one.gen(f_integer=1000+f_integer,
                              f_float=1000.1+f_integer)
            bulk_item_two.gen(f_integer=1000+f_integer,
                              f_float=1000.1+f_integer)
        
        persister.persist(bulk_item_one)
        persister.persist(bulk_item_two)
        
        #--- mix with regular filter -------------------------------------------
        
        # creating item_two
        item_two = ItemGeneralTwo(f_integer=2001, f_float=2001.2)  # new
        item_two['one_x_x'].gen(f_integer=1003)  # old
        item_two['one_x_x'].gen(f_integer=1004)  # new
        
        _, model_lists = persister.persist(item_two)
        
        self.assertEqual(len(self.get_all_models(self.ModelGeneralOne)), 4)
        self.assertEqual(len(self.get_all_models(self.ModelGeneralTwo)), 4)
        self.assertEqual(len(model_lists), 1)
        self.assertEqual(len(model_lists[0]), 1)
        
        model = model_lists[0][0]
        one_x_x = self.get_related_x_to_many(model, 'one_x_x')
        self.assertEqual(len(one_x_x), 2)
        one_x_x.sort(key=lambda m: m.f_integer)
        self.assertEqual(one_x_x[0].f_integer, 1003)
        self.assertEqual(one_x_x[1].f_integer, 1004)
        
        # updating item
        # (can find by `f_float`, but item from `one_x_x` is not there)
        item_two = ItemGeneralTwo(f_float=2001.2)
        item_two['one_x_x'].gen(f_integer=1001)  # old
        
        _, model_lists = persister.persist(item_two)
        self.assertEqual(len(self.get_all_models(self.ModelGeneralOne)), 4)
        self.assertEqual(len(self.get_all_models(self.ModelGeneralTwo)), 4)
        self.assertEqual(len(model_lists), 0)
        
        # (can find by `one_x_x`, but `f_float` does not match)
        item_two = ItemGeneralTwo(f_float=2002.2)
        item_two['one_x_x'].gen(f_integer=1004)  # old
        
        _, model_lists = persister.persist(item_two)
        self.assertEqual(len(self.get_all_models(self.ModelGeneralOne)), 4)
        self.assertEqual(len(self.get_all_models(self.ModelGeneralTwo)), 4)
        self.assertEqual(len(model_lists), 0)
        
        # (empty bulk)
        item_two = ItemGeneralTwo(f_float=2002.2)
        item_two['one_x_x']  # accessing bulk creates it
        
        _, model_lists = persister.persist(item_two)
        self.assertEqual(len(self.get_all_models(self.ModelGeneralOne)), 4)
        self.assertEqual(len(self.get_all_models(self.ModelGeneralTwo)), 4)
        
        # now update must succeed
        item_two = ItemGeneralTwo(f_float=2001.2)
        item_two['one_x_x'].gen(f_integer=1004)  # old
        item_two['one_x_x'].gen(f_integer=1005)  # new
        
        _, model_lists = persister.persist(item_two)
        self.assertEqual(len(self.get_all_models(self.ModelGeneralOne)), 5)
        self.assertEqual(len(self.get_all_models(self.ModelGeneralTwo)), 4)
        
        self.assertEqual(len(model_lists), 1)
        self.assertEqual(len(model_lists[0]), 1)
        model = model_lists[0][0]
        one_x_x = self.get_related_x_to_many(model, 'one_x_x')
        self.assertEqual(len(one_x_x), 3)
        one_x_x.sort(key=lambda m: m.f_integer)
        self.assertEqual(one_x_x[0].f_integer, 1003)
        self.assertEqual(one_x_x[1].f_integer, 1004)
        self.assertEqual(one_x_x[2].f_integer, 1005)
    
    
    def test_related_overwrite_with_none(self):
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = ['two_x_1']
            getters = ['two_x_1']
        
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
            creators = ['f_integer']
            getters = ['f_integer']
        
        item_one = ItemGeneralOne(two_x_1=ItemGeneralTwo(f_integer=1))
        _, model_list = self.persister.persist(item_one)
        model_one = model_list[0][0]
        self.assertEqual(model_one.two_x_1.f_integer, 1)
        
        item_one = ItemGeneralOne(two_x_1=None)
        _, model_list = self.persister.persist(item_one)
        self.assertEqual(len(model_list), 1)
        model_one = model_list[0][0]
        self.assertIsNone(model_one.two_x_1)
    
    
    def test_related_none_creator_and_getter(self):
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = ['two_1_1']
            getters = ['two_1_1']
        
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
            creators = ['f_integer']
            getters = ['f_integer']
        
        # no value - no model created
        item_one = ItemGeneralOne()
        _, model_list = self.persister.persist(item_one)
        self.assertEqual(len(model_list), 0)
        
        # can use `None` as creator
        item_one = ItemGeneralOne(two_1_1=None)
        _, model_list = self.persister.persist(item_one)
        self.assertEqual(len(model_list), 1)
        model_one = model_list[0][0]
        self.assertTrue(not hasattr(model_one, 'two_1_1') or
                        model_one.two_1_1 is None)
        
        model_one_list = self.get_all_models(self.ModelGeneralOne)
        self.assertEqual(len(model_one_list), 1)
        
        # updating using `None` getter
        original_model = model_one
        item_one = ItemGeneralOne(two_1_1=None, f_integer=10)
        _, model_list = self.persister.persist(item_one)
        self.assertEqual(len(model_list), 1)
        model_one = model_list[0][0]
        self.assertEqual(original_model, model_one)
        self.assertTrue(not hasattr(model_one, 'two_1_1') or
                        model_one.two_1_1 is None)
        self.assertEqual(model_one.f_integer, 10)
        
        model_one_list = self.get_all_models(self.ModelGeneralOne)
        self.assertEqual(len(model_one_list), 1)