from save_to_db.adapters.utils.adapter_manager import get_adapter_cls
from save_to_db.adapters.utils.column_type import ColumnType
from save_to_db.adapters.utils.relation_type import RelationType
from save_to_db.exceptions import (
    InvalidFieldName,
    RelatedItemNotFound,
    MultipleRelatedItemsFound,
    NonExistentRelationDefined,
    NonExistentFieldUsed,
    WrongAlias,
    FieldsFromRelationNotAllowed,
    NorewriteRelationException,
    NorewriteKeyUsedTwice,
    DeleterSelectorsOrKeepersEmpty,
    DeleterXToManyRelationUsed,
    UnrefNonXToManyFieldUsed)
from save_to_db.core.item import Item
from save_to_db.utils.test_base import TestBase


class TestItemSetup(TestBase):
    
    ModelFieldTypes = None
    
    ModelGeneralOne = None
    ModelGeneralTwo = None
    
    ModelInvalidFieldNames = None
    
    ModelAutoReverseOne = None
    ModelAutoReverseTwoA = None
    ModelAutoReverseTwoB = None
    ModelAutoReverseThreeA = None
    ModelAutoReverseThreeB = None
    ModelAutoReverseFourA = None
    ModelAutoReverseFourB = None
    
    ModelConstraintsOne = None
    ModelConstraintsTwo = None
    ModelConstraintsThree = None
    ModelConstraintsFour = None
    ModelConstraintsFive = None
    ModelConstraintsSix = None
    ModelConstraintsSelf = None
    
    
    def setup_models(self, one=True, two=True, one_conf=None, two_conf=None,
                     clear_registry=False, complete_setup=None):
        if clear_registry:
            self.item_cls_manager.clear()
        
        if one:
            dct = {'model_cls': self.ModelGeneralOne, }
            if one_conf:
                dct.update(one_conf)
            self.ItemGeneralOne = type('ItemGeneralOne', (Item,), dct)
        if two:
            dct = {'model_cls': self.ModelGeneralTwo, }
            if two_conf:
                dct.update(two_conf)
            self.ItemGeneralTwo = type('ItemGeneralTwo', (Item,), dct)
        
        if complete_setup or (complete_setup is None and one and two):
            self.ItemGeneralOne.complete_setup()
            self.ItemGeneralTwo.complete_setup()
    
    
    def test_auto_reverse_relations(self):
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


        for item_cls in (ItemAutoReverseOne,
                         ItemAutoReverseTwoA, ItemAutoReverseTwoB,
                         ItemAutoReverseThreeA, ItemAutoReverseThreeB,
                         ItemAutoReverseFourA, ItemAutoReverseFourB,):
            item_cls()  # completes relations
            relations_and_reverse = {}
            
            for key, relations in item_cls.relations.items():
                relations_and_reverse[key] = (
                    relations['reverse_key'],
                    relations['relation_type'],
                )
            
            self.assertEqual(relations_and_reverse,
                             item_cls.model_cls.ITEM_RELATIONS)
    
    
    def test_nonexistent_field(self):
        # proper configuration (no nonexistent fields)
        self.setup_models(
            one_conf={
                'creators': ['f_text', 'child_1_1'],  # field and relation
                'getters': ['f_float', 'parent_1_1'],
                'nullables': ['f_date', 'child_1_x'],
                'defaults': {'f_integer': None},
                'norewrite_fields': {'f_integer': True},
                'unref_x_to_many': {
                    'two_x_x': {
                        'selectors': ['f_integer', 'f_float'],
                        'keepers': ['f_float', 'one_1_1']
                    },
                    'two_1_x': ['f_integer', 'f_text'],
                    'child_1_x': {
                        'selectors': ['f_integer', 'f_float', 'two_1_1'],
                    },
                },
                'remove_null_fields': ['f_text', 'child_1_1'],
            },
            clear_registry=True)
        item_one_cls = self.ItemGeneralOne
        self.assertEqual(item_one_cls.creators, [{'f_text'}, {'child_1_1'}])
        self.assertEqual(item_one_cls.getters, [{'f_float'}, {'parent_1_1'}])
        self.assertEqual(item_one_cls.nullables, {'child_1_x', 'f_date'})
        self.assertEqual(item_one_cls.remove_null_fields,
                         {'f_text', 'child_1_1'})
        self.assertEqual(item_one_cls.norewrite_fields, {'f_integer': True})
        
        # nonexistent field
        for key in ('creators', 'getters', 'nullables', 'remove_null_fields',
                    'deleter_selectors', 'deleter_keepers'):
            with self.assertRaises(NonExistentFieldUsed):
                self.setup_models(two_conf={key: ['nonexistent']},
                                  clear_registry=True)
        
        with self.assertRaises(NonExistentFieldUsed):
            self.setup_models(two_conf={'defaults': {'nonexistent': None}},
                              clear_registry=True)
        
        with self.assertRaises(NonExistentFieldUsed):
            self.setup_models(
                two_conf={
                    'norewrite_fields': {
                        'nonexistent': True
                    }
                },
                clear_registry=True)
        
        with self.assertRaises(NonExistentFieldUsed):
            self.setup_models(
                two_conf={
                    'unref_x_to_many': {
                        'nonexistent': ['field_1', 'field_2']
                    }
                },
                clear_registry=True)
        
        with self.assertRaises(NonExistentFieldUsed):
            self.setup_models(
                two_conf={
                    'unref_x_to_many': {
                        'one_x_x': ['nonexistent']
                    }
                },
                clear_registry=True)
           
        with self.assertRaises(NonExistentFieldUsed):
            self.setup_models(
                two_conf={
                    'unref_x_to_many': {
                        'one_x_x': {
                            'keepers': ['nonexistent'],
                        }
                    }
                },
                clear_registry=True)
    
    
    def test_unref_x_to_many_non_x_to_many_field(self):
        # proper configuration
        self.setup_models(
            one_conf={
                'unref_x_to_many': {
                    'two_x_x': {
                        'selectors': ['one_x_1'],
                        'keepers': ['one_1_1']
                    },
                    'two_1_x': ['one_x_1', 'one_1_1'],
                    'child_1_x': {
                        'selectors': ['parent_x_1', 'parent_1_1'],
                    },
                }
            },
            clear_registry=True)
        
        with self.assertRaises(UnrefNonXToManyFieldUsed):
            self.setup_models(
                two_conf={
                    'unref_x_to_many': {
                        'f_integer': ['field']
                    }
                },
                clear_registry=True)
        
        with self.assertRaises(UnrefNonXToManyFieldUsed):
            self.setup_models(
                two_conf={
                    'unref_x_to_many': {
                        'one_x_1': ['f_integer']
                    }
                },
                clear_registry=True)
        
        with self.assertRaises(UnrefNonXToManyFieldUsed):
            self.setup_models(
                two_conf={
                    'unref_x_to_many': {
                        'one_1_1': ['f_integer']
                    }
                },
                clear_registry=True)
    
    
    def test_norewrite_relations(self):
        self.setup_models(
            one_conf={
                'norewrite_fields': {
                    'f_integer': True,
                    'two_1_1': True,
                    'two_x_1': True,
                    'two_x_x': True,
                },
            },
            two_conf={
                'norewrite_fields': {
                    'f_integer': False,
                    'one_x_1': False,
                },
            },
            clear_registry=True)
        
        expected = {
            'f_integer': True,
            'two_1_1': True,
            'two_x_1': True,
            'two_x_x': True,
            'two_1_x': False,  # reverse from two
        }
        self.assertEqual(self.ItemGeneralOne.norewrite_fields, expected)
        
        expected = {
            'f_integer': False,
            'one_1_1': True, # reverse from one
            'one_x_1': False,
            'one_1_x': True,  # reverse from one
            'one_x_x': True,  # reverse from one
        }
        self.assertEqual(self.ItemGeneralTwo.norewrite_fields, expected)
        
        with self.assertRaises(NorewriteRelationException):
            self.setup_models(
                one_conf={
                    'norewrite_fields': {
                        'two_1_1': True,
                    },
                },
                two_conf={
                    'norewrite_fields': {
                        'one_1_1': False,
                    },
                },
                clear_registry=True)
    
    
    def test_norewrite_for_general_key(self):
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            norewrite_fields = {
                'f_integer': True,
                True: False,
            }
         
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
        
        # first checking item two, it must have values from item one
        ItemGeneralTwo()
        expect = {
            'one_x_x': False,
            'one_1_x': False,
            'one_1_1': False,
            'one_x_1': False,
        }
        self.assertEqual(ItemGeneralTwo.norewrite_fields, expect)
        
        ItemGeneralOne()
        expect = {
            'f_integer': True,
            'f_binary': False,
            'f_date': False,
            'parent_x_x': False,
            'two_1_1': False,
            'f_text': False,
            'child_1_1': False,
            'two_x_1': False,
            'id': False,
            'child_x_x': False,
            'two_1_x': False,
            'f_boolean': False,
            'f_string': False,
            'parent_1_1': False,
            'f_datetime': False,
            'child_1_x': False,
            'f_float': False,
            'f_decimal': False,
            'two_x_x': False,
            'f_time': False,
            'parent_x_1': False}
        self.assertEqual(ItemGeneralOne.norewrite_fields, expect)
    
    
    def test_field_from_relations_not_allowed(self):
        # proper configuration (no nonexistent fields)
        self.setup_models(
            one_conf={
                'creators': ['f_text', 'child_1_1'],  # field and relation
                'getters': ['f_float', 'parent_1_1'],
                'nullables': ['f_date', 'child_1_x'],
                'defaults': {'f_integer': None},
                'norewrite_fields': {'f_integer': True},
                'remove_null_fields': ['f_text', 'child_1_1'],
            },
            two_conf={
                'creators': ['f_integer'],
                'getters': ['child_1_1'],
            },           
            clear_registry=True)
        item_one_cls = self.ItemGeneralOne
        item_two_cls = self.ItemGeneralTwo
        
        self.assertEqual(item_one_cls.creators, [{'f_text'}, {'child_1_1'}])
        self.assertEqual(item_one_cls.getters, [{'f_float'}, {'parent_1_1'}])
        self.assertEqual(item_one_cls.nullables, {'child_1_x', 'f_date'})
        self.assertEqual(item_one_cls.norewrite_fields, {'f_integer': True})
        self.assertEqual(item_one_cls.remove_null_fields,
                         {'f_text', 'child_1_1'})
        self.assertEqual(item_two_cls.creators, [{'f_integer'}])
        self.assertEqual(item_two_cls.getters, [{'child_1_1'}])
        
         
        # field_from_relations_not_allowed
        for key in ('creators', 'getters',):
            with self.assertRaises(FieldsFromRelationNotAllowed):
                self.setup_models(two_conf={key: [{'child_1_1__f_integer'}]},
                                  clear_registry=True)
        
        for key in ('nullables', 'remove_null_fields',
                    'deleter_selectors', 'deleter_keepers'):
            with self.assertRaises(FieldsFromRelationNotAllowed):
                self.setup_models(two_conf={key: ['child_1_1__f_integer']},
                                  clear_registry=True)
        
        with self.assertRaises(FieldsFromRelationNotAllowed):
            self.setup_models(
                two_conf={
                    'defaults': {
                        'child_1_1__f_integer': None
                    }
                },
                clear_registry=True)
            
        with self.assertRaises(FieldsFromRelationNotAllowed):
            self.setup_models(
                two_conf={
                    'norewrite_fields': {
                        'child_1_1__f_integer': True
                    }
                },
                clear_registry=True)
        
        with self.assertRaises(FieldsFromRelationNotAllowed):
            self.setup_models(
                one_conf={
                    'unref_x_to_many': {
                        'two_x_x__one_x_x': ['f_integer']
                    }
                },
                clear_registry=True)
        
        with self.assertRaises(FieldsFromRelationNotAllowed):
            self.setup_models(
                one_conf={
                    'unref_x_to_many': {
                        'two_x_x': ['one_x_x__f_integer']
                    }
                },
                clear_registry=True)
    
    
    def test_norewrite_fields_config(self):
        self.setup_models(
            one_conf={
                'norewrite_fields': {
                    'f_integer': True,
                    True: False,
                },
            },           
            clear_registry=True)
        
        expect = {
            'id': False,
            'f_binary': False,
            'f_boolean': False,
            'f_date': False,
            'f_datetime': False,
            'f_float': False,
            'f_decimal': False,
            'f_integer': True, 
            'f_string': False,
            'f_text': False, 
            'f_time': False,
            'child_1_1': False,
            'child_1_x': False,
            'child_x_x': False,
            'parent_1_1': False,
            'parent_x_1': False,
            'parent_x_x': False,
            'two_1_1': False,
            'two_1_x': False,
            'two_x_1': False,
            'two_x_x': False,
        }
        
        self.assertEqual(self.ItemGeneralOne.norewrite_fields, expect)
        
        self.setup_models(
            one_conf={
                'norewrite_fields': {
                    'f_integer': True,
                    # tuple
                    ('f_string', 'f_text'): None,
                    # RelationType
                    RelationType.MANY_TO_MANY: True,
                    RelationType.ONE_TO_ONE: True,
                    # RelationType overwritten
                    'parent_x_x': None,
                    # the rest
                    True: False,
                },
            },           
            clear_registry=True)
        
        excpext = {
            'f_integer': True,      # 'f_integer
            'f_binary': False,      # True
            'parent_x_1': False,    # True
            'f_datetime': False,    # True
            'f_text': None,         # ('f_string', 'f_text')
            'f_string': None,       # ('f_string', 'f_text')
            'two_1_x': False,       # True
            'two_x_x': True,        # RelationType.MANY_TO_MANY
            'child_x_x': None,      # 'parent_x_x' (reverse)
            'parent_1_1': True,     # RelationType.ONE_TO_ONE
            'id': False,            # True
            'f_boolean': False,     # True
            'f_float': False,       # True
            'f_decimal': False,     # True
            'two_x_1': False,       # True
            'f_time': False,        # True
            'child_1_1': True,      # RelationType.ONE_TO_ONE
            'two_1_1': True,        # RelationType.ONE_TO_ONE
            'child_1_x': False,     # True
            'f_date': False,        # True
            'parent_x_x': None,     # 'parent_x_x'
        }
        self.assertEqual(self.ItemGeneralOne.norewrite_fields, excpext)
    
    
    def test_no_rewrite_field_used_twice(self):
        with self.assertRaises(NorewriteKeyUsedTwice):
            self.setup_models(
            one_conf={
                'norewrite_fields': {
                    'f_integer': True,
                    ('f_integer', 'f_float'): None,
                },
            },           
            clear_registry=True)
        
        with self.assertRaises(NorewriteKeyUsedTwice):
            self.setup_models(
            one_conf={
                'norewrite_fields': {
                    ('f_string', 'f_integer'): True,
                    ('f_integer', 'f_float'): None,
                },
            },           
            clear_registry=True)
    
    
    def test_relations_config_excpetions(self):
        # NonExistentRelationDefined
        class WithNonExistantRelation(Item):
            model_cls = self.ModelFieldTypes
            relations = {
                'non_existant': self.ModelGeneralOne,
            }

        with self.assertRaises(NonExistentRelationDefined):
            WithNonExistantRelation.complete_setup()
        
        # RelatedItemNotFound
        self.setup_models(one=True, two=False)
        with self.assertRaises(RelatedItemNotFound):
            self.ItemGeneralOne.complete_setup()
        
        # MultipleRelatedItemsFound
        self.setup_models(one=False, two=True)
        self.setup_models(one=False, two=True)  # second model
        
        with self.assertRaises(MultipleRelatedItemsFound):
            self.ItemGeneralOne.complete_setup()
    

    def test_fields_autoconfig(self):
        self.setup_models()
        
        extected_fields = {
            'id': ColumnType.INTEGER,
            'f_binary': ColumnType.BINARY,
            'f_boolean': ColumnType.BOOLEAN,
            'f_text': ColumnType.TEXT,
            'f_string': ColumnType.STRING,
            'f_integer': ColumnType.INTEGER,
            'f_float': ColumnType.FLOAT,
            'f_decimal': ColumnType.DECIMAL,
            'f_date': ColumnType.DATE,
            'f_time': ColumnType.TIME,
            'f_datetime': ColumnType.DATETIME,
        }
        self.assertEqual(self.ItemGeneralOne.fields, extected_fields)
    
    
    def test_relations_autoconfig(self):
        self.setup_models(two_conf={
            'relations': {
                    'parent_x_x': {
                        'replace_x_to_many': True,
                    },
                },
            })
        
        #--- one ---
        expected_relations = {
            'parent_1_1': {
                'relation_type': RelationType.ONE_TO_ONE,
                'item_cls': self.ItemGeneralOne,
                'replace_x_to_many': False,
                'reverse_key': 'child_1_1',
            },
            'child_1_1': {
                'relation_type': RelationType.ONE_TO_ONE,
                'item_cls': self.ItemGeneralOne,
                'replace_x_to_many': False,
                'reverse_key': 'parent_1_1',
            },
            'parent_x_1': {
                'relation_type': RelationType.MANY_TO_ONE,
                'item_cls': self.ItemGeneralOne,
                'replace_x_to_many': False,
                'reverse_key': 'child_1_x',
            },
            'child_1_x': {
                'relation_type': RelationType.ONE_TO_MANY,
                'item_cls': self.ItemGeneralOne,
                'replace_x_to_many': False,
                'reverse_key': 'parent_x_1',
            },
            'parent_x_x': {
                'relation_type': RelationType.MANY_TO_MANY,
                'item_cls': self.ItemGeneralOne,
                'replace_x_to_many': False,
                'reverse_key': 'child_x_x',
            },
            'child_x_x': {
                'relation_type': RelationType.MANY_TO_MANY,
                'item_cls': self.ItemGeneralOne,
                'replace_x_to_many': False,
                'reverse_key': 'parent_x_x',
            },
            'two_1_1': {
                'relation_type': RelationType.ONE_TO_ONE,
                'item_cls': self.ItemGeneralTwo,
                'replace_x_to_many': False,
                'reverse_key': 'one_1_1',
            },
            'two_1_x': {
                'relation_type': RelationType.ONE_TO_MANY,
                'item_cls': self.ItemGeneralTwo,
                'replace_x_to_many': False,
                'reverse_key': 'one_x_1',
            },
            'two_x_1': {
                'relation_type': RelationType.MANY_TO_ONE,
                'item_cls': self.ItemGeneralTwo,
                'replace_x_to_many': False,
                'reverse_key': 'one_1_x',
            },
            'two_x_x': {
                'relation_type': RelationType.MANY_TO_MANY,
                'item_cls': self.ItemGeneralTwo,
                'replace_x_to_many': False,
                'reverse_key': 'one_x_x',
            },
        }
        self.assertEqual(self.ItemGeneralOne.relations, expected_relations)
        
        #--- two ---
        expected_relations = {
            'parent_1_1': {
                'relation_type': RelationType.ONE_TO_ONE,
                'item_cls': self.ItemGeneralTwo,
                'replace_x_to_many': False,
                'reverse_key': 'child_1_1',
            },
            'child_1_1': {
                'relation_type': RelationType.ONE_TO_ONE,
                'item_cls': self.ItemGeneralTwo,
                'replace_x_to_many': False,
                'reverse_key': 'parent_1_1',
            },
            'parent_x_1': {
                'relation_type': RelationType.MANY_TO_ONE,
                'item_cls': self.ItemGeneralTwo,
                'replace_x_to_many': False,
                'reverse_key': 'child_1_x',
            },
            'child_1_x': {
                'relation_type': RelationType.ONE_TO_MANY,
                'item_cls': self.ItemGeneralTwo,
                'replace_x_to_many': False,
                'reverse_key': 'parent_x_1',
            },
            'parent_x_x': {
                'relation_type': RelationType.MANY_TO_MANY,
                'item_cls': self.ItemGeneralTwo,
                'replace_x_to_many': True,  # default overwritten
                'reverse_key': 'child_x_x',
            },
            'child_x_x': {
                'relation_type': RelationType.MANY_TO_MANY,
                'item_cls': self.ItemGeneralTwo,
                'replace_x_to_many': False,
                'reverse_key': 'parent_x_x',
            },
            'one_1_1': {
                'relation_type': RelationType.ONE_TO_ONE,
                'item_cls': self.ItemGeneralOne,
                'replace_x_to_many': False,
                'reverse_key': 'two_1_1',
            },
            'one_1_x': {
                'relation_type': RelationType.ONE_TO_MANY,
                'item_cls': self.ItemGeneralOne,
                'replace_x_to_many': False,
                'reverse_key': 'two_x_1',
            },
            'one_x_1': {
                'relation_type': RelationType.MANY_TO_ONE,
                'item_cls': self.ItemGeneralOne,
                'replace_x_to_many': False,
                'reverse_key': 'two_1_x',
            },
            'one_x_x': {
                'relation_type': RelationType.MANY_TO_MANY,
                'item_cls': self.ItemGeneralOne,
                'replace_x_to_many': False,
                'reverse_key': 'two_x_x',
            },
        }
        self.assertEqual(self.ItemGeneralTwo.relations, expected_relations)
    
    
    def __to_sorted_lists(self, iterable_of_iterables):
        result = []
        for iterable in iterable_of_iterables:
            element = list(iterable)
            element.sort()
            result.append(element)
        result.sort()
        return result
    
    
    def test_creators_getter_autoconfig(self):
        # generating items for models
        models_for_items = (
            self.ModelConstraintsOne,
            self.ModelConstraintsTwo,
            self.ModelConstraintsThree,
            self.ModelConstraintsFour,
            self.ModelConstraintsFive,
            self.ModelConstraintsSix,
            self.ModelConstraintsSelf,
        )
        item_classes = []
        for model_cls in models_for_items:
            item_classes.append(type(
                model_cls.__name__.replace('Model', 'Item'), (Item,), {
                    'model_cls': model_cls
                }
            ))
            
        for item_cls in item_classes:
            item_cls.complete_setup()
        (ItemConstraintsOne, ItemConstraintsTwo, ItemConstraintsThree,
         ItemConstraintsFour, ItemConstraintsFive, ItemConstraintsSix,
         ItemConstraintsSelf) = item_classes
        
        # checking configuration
        adapter_cls = get_adapter_cls(ItemConstraintsOne.model_cls)
        composites = adapter_cls.COMPOSITE_KEYS_SUPPORTED
        
        expected = {
            ItemConstraintsOne: {
                'creators': [{'f_text', 'f_string'}],
                'getters': [{'id'}, {'f_integer'}, {'f_string'}, {'five_1_1'}],
            },
            ItemConstraintsTwo: {
                'creators': [{'four_x_1'}],
                'getters': [{'id'}],
            },
            ItemConstraintsThree: {
                'creators': [{'one_x_1'}],
                'getters': [{'id'}],
            },
            ItemConstraintsFour: {
                'creators':
                    [{'primary_two', 'primary_one'}]
                        if composites else [],
                'getters':
                    [{'primary_two', 'primary_one'} if composites else {'id'},
                     {'five_1_1'}, {'f_integer', 'f_string'}],
            },
            ItemConstraintsFive: {
                'creators': [],
                'getters': [{'id'}, {'one_1_1'}, {'four_1_1'}, {'six_1_1'}],
            },
            ItemConstraintsSix: {
                'creators': [{'five_1_1'}],
                'getters': [{'id'}, {'f_integer', 'five_1_1'}, {'five_1_1'}],
            },
            ItemConstraintsSelf: {
                'creators': [{'code', 'second_parent_1_1', 'parent_x_1'}],
                'getters': [{'code'},
                            {'first_parent_1_1'}, {'first_child_1_1'},
                            {'second_parent_1_1'}, {'second_child_1_1'},],
            },
        }
        
        for item_cls in item_classes:
            #--- getters ---
            item_getters = self.__to_sorted_lists(
                item_cls.getters)
            expected_getters = self.__to_sorted_lists(
                expected[item_cls]['getters'])
            self.assertEqual(item_getters, expected_getters, item_cls)
            
            #--- creators ---
            item_creators = self.__to_sorted_lists(
                item_cls.creators)
            expected_creators = self.__to_sorted_lists(
                expected[item_cls]['creators'])
            
            self.assertEqual(item_creators, expected_creators, item_cls)
    
    
    def test_creators_getter_autoconfig_overwrite(self):
        # default overwritten
        class ItemConstraintsSelf_A(Item):
            model_cls = self.ModelConstraintsSelf
            creators = [{'parent_x_1'}]
            getters = [{'first_parent_1_1'}]
        ItemConstraintsSelf_A.complete_setup()
        
        self.assertEqual(ItemConstraintsSelf_A.creators,
                         [{'parent_x_1'}])
        self.assertEqual(ItemConstraintsSelf_A.getters,
                         [{'first_parent_1_1'}])
    

        # default not overwritten
        self.item_cls_manager.clear()
        class ItemConstraintsSelf_B(Item):
            model_cls = self.ModelConstraintsSelf
        ItemConstraintsSelf_B.complete_setup()
        
        self.assertEqual(self.__to_sorted_lists(ItemConstraintsSelf_B.creators),
                         self.__to_sorted_lists(
                             [{'code', 'second_parent_1_1', 'parent_x_1'}]))
        self.assertEqual(self.__to_sorted_lists(ItemConstraintsSelf_B.getters),
                         self.__to_sorted_lists(
                            [{'code'},
                             {'first_parent_1_1'}, {'first_child_1_1'},
                             {'second_parent_1_1'}, {'second_child_1_1'},]))
        
        # default creators merge
        self.item_cls_manager.clear()
        class ItemConstraintsSelf_C(Item):
            model_cls = self.ModelConstraintsSelf
            creators = [{'f_binary'}]
            creators_autoconfig = True
            autoinject_creators = False
            getters = [{'f_boolean'}]
            getters_autoconfig = False
        ItemConstraintsSelf_C.complete_setup()
        
        self.assertEqual(self.__to_sorted_lists(ItemConstraintsSelf_C.creators),
                         self.__to_sorted_lists(
                            [{'f_binary'},
                             {'code', 'second_parent_1_1', 'parent_x_1'}]))
        self.assertEqual(self.__to_sorted_lists(ItemConstraintsSelf_C.getters),
                         self.__to_sorted_lists([{'f_boolean'}]))
        
        # default getters merge
        self.item_cls_manager.clear()
        class ItemConstraintsSelf_D(Item):
            model_cls = self.ModelConstraintsSelf
            creators = [{'f_binary'}]
            creators_autoconfig = False
            autoinject_creators = False
            getters = [{'f_boolean'}]
            getters_autoconfig = True
        ItemConstraintsSelf_D.complete_setup()
        
        self.assertEqual(self.__to_sorted_lists(ItemConstraintsSelf_D.creators),
                         self.__to_sorted_lists([{'f_binary'}]))
        self.assertEqual(self.__to_sorted_lists(ItemConstraintsSelf_D.getters),
                         self.__to_sorted_lists(
                            [{'f_boolean'},
                             {'code'},
                             {'first_parent_1_1'}, {'first_child_1_1'},
                             {'second_parent_1_1'}, {'second_child_1_1'},]))
        
        # creators extended
        self.item_cls_manager.clear()
        class ItemConstraintsSelf_E(Item):
            model_cls = self.ModelConstraintsSelf
        ItemConstraintsSelf_E.complete_setup()
        
        self.assertEqual(self.__to_sorted_lists(ItemConstraintsSelf_E.creators),
                         self.__to_sorted_lists([{'code',
                                                  'second_parent_1_1',
                                                  'parent_x_1'}]))
        
        self.item_cls_manager.clear()
        class ItemConstraintsSelf_F(Item):
            model_cls = self.ModelConstraintsSelf
            creators = [{'f_binary'}, {'f_boolean', 'code'}]
            creators_autoconfig = False
            autoinject_creators = True  # prevented by `autoinject_creators`
        ItemConstraintsSelf_F.complete_setup()
        
        self.assertEqual(self.__to_sorted_lists(ItemConstraintsSelf_F.creators),
                         self.__to_sorted_lists([{'f_binary'},
                                                 {'f_boolean', 'code'}]))
        
        self.item_cls_manager.clear()
        class ItemConstraintsSelf_G(Item):
            model_cls = self.ModelConstraintsSelf
            creators = [{'f_binary'}, {'f_boolean', 'code'}]
            creators_autoconfig = True
            autoinject_creators = True  # creator groups must be extended
        ItemConstraintsSelf_G.complete_setup()
         
        self.assertEqual(self.__to_sorted_lists(ItemConstraintsSelf_G.creators),
                         self.__to_sorted_lists([{'f_binary',
                                                  'code',
                                                  'second_parent_1_1',
                                                  'parent_x_1'},
                                                 {'f_boolean',
                                                  'code',
                                                  'second_parent_1_1',
                                                  'parent_x_1'}]))
        
        # but do not extend if group already there
        self.item_cls_manager.clear()
        class ItemConstraintsSelf_H(Item):
            model_cls = self.ModelConstraintsSelf
            creators = [{'code',
                         'second_parent_1_1', 'parent_x_1'}]
            creators_autoconfig = True
            autoinject_creators = True
        ItemConstraintsSelf_H.complete_setup()
         
        self.assertEqual(self.__to_sorted_lists(ItemConstraintsSelf_H.creators),
                         self.__to_sorted_lists([{'code',
                                                  'second_parent_1_1',
                                                  'parent_x_1'}]))
    
    
    def test_invalid_field_name(self):
        class InvalidItem(Item):
            model_cls = self.ModelInvalidFieldNames

        with self.assertRaises(InvalidFieldName):
            InvalidItem()
    
    
    def test_invalid_alias(self):
        with self.assertRaises(WrongAlias):
            self.setup_models(
                one_conf={
                    'aliases': {
                        'alias_1': 'two_1_1__f_integer',
                        'alias_2': 'two_x_x__one_1_1__f_integer__invaliad_alias',
                    }
                },
                clear_registry=True)
        
        
    def test_creators_and_getters_mix(self):
        self.item_cls_manager.autogenerate = True
        
        class ItemConstraintsOne(Item):
            model_cls = self.ModelConstraintsOne
            
            getters = ['three_1_x', 'f_integer']
            getters_autoconfig = True
            
            creators = ['three_1_x', 'f_integer']
            creators_autoconfig = True

            
        class ItemConstraintsThree(Item):
            model_cls = self.ModelConstraintsThree
        
        ItemConstraintsOne.complete_setup()
        ItemConstraintsThree.complete_setup()
        
        expected_getters = [{'three_1_x'}, {'f_integer'},
                            {'five_1_1'}, {'f_string'}, {'id'}]
        expected_creators = [{'three_1_x'}, {'f_integer'},
                             {'f_text', 'f_string'}]
        
        def sorted_groups(groups):
            subgroups = []
            for subgroup in groups:
                subgroup = list(subgroup)
                subgroup.sort()
                subgroups.append(subgroup)
            subgroups.sort()
        
        self.assertEqual(sorted_groups(ItemConstraintsOne.getters),
                         sorted_groups(expected_getters))
        self.assertEqual(sorted_groups(ItemConstraintsOne.creators),
                         sorted_groups(expected_creators))

        
    def test_model_deleter(self):
        # DeleterXToManyRelationUsed
        for key in ['deleter_selectors', 'deleter_keepers']:
            one_conf = {
                'deleter_selectors': {'f_integer'},
                'deleter_keepers': {'f_string'},
            }
            one_conf[key] = {'two_1_x'}
            with self.assertRaises(DeleterXToManyRelationUsed):
                self.setup_models(
                    one_conf=one_conf,
                    clear_registry=True)
        
        # DeleterSelectorsOrKeepersEmpty
        for key in ['deleter_selectors', 'deleter_keepers']:
            one_conf = {
                'deleter_selectors': {'f_integer'},
                'deleter_keepers': {'f_string'},
            }
            one_conf[key] = []
            with self.assertRaises(DeleterSelectorsOrKeepersEmpty):
                self.setup_models(
                    one_conf=one_conf,
                    clear_registry=True)
                
        # normal setup
        self.setup_models(clear_registry=True)
        self.assertIsNone(self.ItemGeneralOne.metadata['model_deleter'])
        self.assertIsNone(self.ItemGeneralTwo.metadata['model_deleter'])
        
        self.setup_models(
            one_conf = {
                'deleter_selectors': {'f_integer'},
                'deleter_keepers': {'f_string'},
            },
            clear_registry=True)
        self.assertIsNotNone(self.ItemGeneralOne.metadata['model_deleter'])
        model_deleter = self.ItemGeneralOne.metadata['model_deleter']
        self.assertIs(model_deleter.model_cls, self.ItemGeneralOne.model_cls)
        self.assertEqual(model_deleter.selector_fields, {'f_integer'})
        self.assertEqual(model_deleter.keeper_fields, {'f_string'})
        self.assertIsNone(self.ItemGeneralTwo.metadata['model_deleter'])
        
        # default keepers
        self.setup_models(
            one_conf = {
                'deleter_selectors': {'f_integer'},
            },
            clear_registry=True)
        self.assertIsNotNone(self.ItemGeneralOne.metadata['model_deleter'])
        model_deleter = self.ItemGeneralOne.metadata['model_deleter']
        self.assertIs(model_deleter.model_cls, self.ItemGeneralOne.model_cls)
        self.assertEqual(model_deleter.selector_fields, {'f_integer'})
        self.assertEqual(model_deleter.keeper_fields, {'id'})  # primary keys
        self.assertIsNone(self.ItemGeneralTwo.metadata['model_deleter'])
        
        
    def test_model_deleter_unref(self):
        # DeleterXToManyRelationUsed
        for key in ['selectors', 'keepers']:
            with self.assertRaises(DeleterXToManyRelationUsed):
                value = {
                    'selectors': ['f_integer'],
                    'keepers': ['f_integer'],
                }
                value[key] = ['one_1_x']
                self.setup_models(
                    one_conf={
                        'unref_x_to_many': {
                            'two_x_x': value,
                        }
                    },
                    clear_registry=True)
        
        # DeleterSelectorsOrKeepersEmpty
        for key in ['selectors', 'keepers']:
            with self.assertRaises(DeleterSelectorsOrKeepersEmpty):
                value = {
                    'selectors': ['f_integer'],
                    'keepers': ['f_integer'],
                }
                value[key] = []
                self.setup_models(
                    one_conf={
                        'unref_x_to_many': {
                            'two_x_x': value,
                        }
                    },
                    clear_registry=True)
        
        # normal setup
        self.setup_models(clear_registry=True)
        self.assertFalse(self.ItemGeneralOne.metadata['model_unrefs'])
        self.assertFalse(self.ItemGeneralTwo.metadata['model_unrefs'])
        
        self.setup_models(
            one_conf = {
                'unref_x_to_many': {
                    'two_x_x': {
                        'selectors': {'f_string'},
                        'keepers': {'f_text'},
                    },
                    'parent_x_x': {
                        'selectors': {'f_integer'},
                        'keepers': {'f_float'},
                    }
                }
            },
            clear_registry=True)
        self.assertIn('two_x_x',
                      self.ItemGeneralOne.metadata['model_unrefs'])
        self.assertIn('parent_x_x',
                      self.ItemGeneralOne.metadata['model_unrefs'])
        self.assertFalse(self.ItemGeneralTwo.metadata['model_unrefs'])
        
        two_x_x_deleter = \
            self.ItemGeneralOne.metadata['model_unrefs']['two_x_x']
        self.assertIs(two_x_x_deleter.model_cls, self.ItemGeneralTwo.model_cls)
        self.assertEqual(two_x_x_deleter.selector_fields, {'f_string'})
        self.assertEqual(two_x_x_deleter.keeper_fields, {'f_text'})
            
        parent_x_x_deleter = \
            self.ItemGeneralOne.metadata['model_unrefs']['parent_x_x']
        self.assertIs(parent_x_x_deleter.model_cls,
                      self.ItemGeneralOne.model_cls)
        self.assertEqual(parent_x_x_deleter.selector_fields, {'f_integer'})
        self.assertEqual(parent_x_x_deleter.keeper_fields, {'f_float'})
        
        # default keepers
        self.setup_models(
            one_conf = {
                'unref_x_to_many': {
                    'two_x_x': {'f_string'},
                }
            },
            clear_registry=True)
        self.assertIn('two_x_x',
                      self.ItemGeneralOne.metadata['model_unrefs'])
        self.assertFalse(self.ItemGeneralTwo.metadata['model_unrefs'])
        
        two_x_x_deleter = \
            self.ItemGeneralOne.metadata['model_unrefs']['two_x_x']
        self.assertIs(two_x_x_deleter.model_cls, self.ItemGeneralTwo.model_cls)
        self.assertEqual(two_x_x_deleter.selector_fields, {'f_string'})
        self.assertEqual(two_x_x_deleter.keeper_fields, {'id'})  # primary keys
    
    
    def test_remove_null_fields_autoconfig(self):
        self.item_cls_manager.autogenerate = True
        
        # normal defaults ------------------------------------------------------
        self.item_cls_manager.clear()
        
        # normal fields
        ItemConstraintsOne = type('ItemConstraintsOne', (Item,), {
            'model_cls': self.ModelConstraintsOne,
        })
        # relations
        ItemConstraintsTwo = type('ItemConstraintsTwo', (Item,), {
            'model_cls': self.ModelConstraintsTwo,
        })
        # nothing
        ModelConstraintsFive = type('ModelConstraintsFive', (Item,), {
            'model_cls': self.ModelConstraintsFive,
        })
        
        ItemConstraintsOne.complete_setup()
        self.assertEqual(ItemConstraintsOne.remove_null_fields,
                         {'f_text', 'f_string'})
        ItemConstraintsTwo.complete_setup()
        self.assertEqual(ItemConstraintsTwo.remove_null_fields,
                         {'four_x_1'})
        ModelConstraintsFive.complete_setup()
        self.assertEqual(ModelConstraintsFive.remove_null_fields, set())
    
    
        # remove_null_fields_autoconfig off ------------------------------------
        self.item_cls_manager.clear()
        
        # no manual setup
        ItemConstraintsOne = type('ItemConstraintsOne', (Item,), {
            'model_cls': self.ModelConstraintsOne,
            'remove_null_fields_autoconfig': False,
        })
        # manual setup
        ItemConstraintsTwo = type('ItemConstraintsTwo', (Item,), {
            'model_cls': self.ModelConstraintsTwo,
            'remove_null_fields_autoconfig': False,
            'remove_null_fields': {'f_integer', 'f_string'}
        })

        ItemConstraintsOne.complete_setup()
        self.assertEqual(ItemConstraintsOne.remove_null_fields, set())
        ItemConstraintsTwo.complete_setup()
        self.assertEqual(ItemConstraintsTwo.remove_null_fields,
                         {'f_integer', 'f_string'})
        
        # remove_null_fields_autoconfig on -------------------------------------
        self.item_cls_manager.clear()
        
        # no manual setup
        ItemConstraintsOne = type('ItemConstraintsOne', (Item,), {
            'model_cls': self.ModelConstraintsOne,
            'remove_null_fields_autoconfig': True,
        })
        # manual setup
        ItemConstraintsTwo = type('ItemConstraintsTwo', (Item,), {
            'model_cls': self.ModelConstraintsTwo,
            'remove_null_fields_autoconfig': True,
            'remove_null_fields': {'f_integer', 'f_string'}
        })

        ItemConstraintsOne.complete_setup()
        self.assertEqual(ItemConstraintsOne.remove_null_fields,
                         {'f_text', 'f_string'})
        ItemConstraintsTwo.complete_setup()
        self.assertEqual(ItemConstraintsTwo.remove_null_fields,
                         {'f_integer', 'f_string', 'four_x_1'})
        
        # remove_null_fields_autoconfig default --------------------------------
        self.item_cls_manager.clear()
        
        # no manual setup
        ItemConstraintsOne = type('ItemConstraintsOne', (Item,), {
            'model_cls': self.ModelConstraintsOne,
            'remove_null_fields': {}
        })
        # manual setup
        ItemConstraintsTwo = type('ItemConstraintsTwo', (Item,), {
            'model_cls': self.ModelConstraintsTwo,
            'remove_null_fields': {'f_integer', 'f_string'}
        })

        ItemConstraintsOne.complete_setup()
        self.assertEqual(ItemConstraintsOne.remove_null_fields, set())
        ItemConstraintsTwo.complete_setup()
        self.assertEqual(ItemConstraintsTwo.remove_null_fields,
                         {'f_integer', 'f_string'})
        
