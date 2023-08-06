from save_to_db.core.item import Item
from save_to_db.core.merge_policy import MergePolicy
from save_to_db.utils.test_base import TestBase

from save_to_db.exceptions import (ModelClsAlreadyRegistered,
                                   UnknownRelationFieldNames,
                                   UnknownModelDefaultKey,)


class TestPolicySetup(TestBase):
    
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
    
    
   
    def test_creation_and_addition(self):
        # NOTE: In this test we are using string values as dunny functions

        #--- creation test ---
        merge_policy_one = MergePolicy(
            self.db_adapter,
            policy={
                self.ModelMergeOne: {
                    'two_1_1': 'resolve_two_one',
                },
                self.ModelMergeThree: {
                    'two_1_x': 'resolve_two_many',
                },
            },
            defaults={
                self.ModelMergeOne: {
                    MergePolicy.REL_ONE: 'resolve_one_one_default',
                    MergePolicy.REL_MANY: 'resolve_one_many_default',
                },
            })
        expected_one = {
            self.ModelMergeOne: {
                'two_1_1': 'resolve_two_one',
            },
            # defaults
            self.ModelMergeTwo: {
                'one_1_1': 'resolve_one_one_default',
                'one_1_x': 'resolve_one_many_default',
            },
            self.ModelMergeThree: {
                'two_1_x': 'resolve_two_many',
            }
        }
        self.assertEqual(merge_policy_one, expected_one)
         
        merge_policy_two = MergePolicy(
            self.db_adapter,
            policy={
                self.ModelMergeOne: {
                    'two_1_1': 'resolve_two_one',
                },
            },
            defaults={
                self.ModelMergeTwo: {
                    MergePolicy.REL_ONE: 'resolve_two_one_default',
                },
            })
        expected_two = {
            self.ModelMergeOne: {
                'two_1_1': 'resolve_two_one',  # default must not overwrite
                'two_x_1': 'resolve_two_one_default',
            },
            self.ModelMergeThree: {
                'two_1_1': 'resolve_two_one_default',
            }
        }
        self.assertEqual(merge_policy_two, expected_two)
        
        #--- addition test ---
        
        # overwriting model two
        merge_policy_one.add_model_policy(
            self.ModelMergeTwo,
            model_policy={
                'one_1_1': 'resolve_one_one',
            },
            model_defaults={
                MergePolicy.REL_ONE: 'resolve_two_one_default',
            }
        )
        expected_one_new = {
            self.ModelMergeOne: {
                'two_1_1': 'resolve_two_one',
                'two_x_1': 'resolve_two_one_default',  # injected new
            },
            # defaults
            self.ModelMergeTwo: {
                'one_1_1': 'resolve_one_one',  # overwritten
                'one_1_x': 'resolve_one_many_default',  # injected old
            },
            self.ModelMergeThree: {
                'two_1_1': 'resolve_two_one_default',  # injected new
                'two_1_x': 'resolve_two_many',
            }
        }
        self.assertEqual(merge_policy_one, expected_one_new)
    
        # adding model two
        merge_policy_two.add_model_policy(
            self.ModelMergeThree,
            model_policy={
                'two_1_1': 'resolve_two_one',
            },
            model_defaults={
                MergePolicy.REL_ONE: 'resolve_three_one_default',
            }
        )
        expect_two_new = {
            self.ModelMergeOne: {
                'two_1_1': 'resolve_two_one',
                'two_x_1': 'resolve_two_one_default',
            },
            self.ModelMergeTwo: {
                'three_1_1': 'resolve_three_one_default',  # added
                'three_x_1': 'resolve_three_one_default',  # added
            },
            self.ModelMergeThree: {
                'two_1_1': 'resolve_two_one',  # overwritten
            }
        }
        self.assertEqual(merge_policy_two, expect_two_new)
    
    
    def test_exceptions(self):
        
        def create_policy():
            return MergePolicy(
                self.db_adapter,
                policy={
                    self.ModelMergeOne: {
                        'two_1_1': 'resolve_two_one',
                    },
                },
                defaults={
                    self.ModelMergeTwo: {
                        MergePolicy.REL_ONE: 'resolve_two_one_default',
                    },
                })
        
        #--- adding already resitered classes ---
        merge_policy = create_policy()
        
        # in policy
        with self.assertRaises(ModelClsAlreadyRegistered):
            merge_policy.add_model_policy(self.ModelMergeOne, model_policy={})
        
        # in defaults
        with self.assertRaises(ModelClsAlreadyRegistered):
            merge_policy.add_model_policy(self.ModelMergeTwo, model_policy={})
        
        #--- using wrong relation field names ---
        with self.assertRaises(UnknownRelationFieldNames):
            merge_policy = MergePolicy(
                self.db_adapter,
                policy={
                    self.ModelMergeOne: {
                        'unknown_field': 'resolve_unknown_field',
                    },
                })
        with self.assertRaises(UnknownRelationFieldNames):
            merge_policy.add_model_policy(
                self.ModelMergeThree,
                model_policy={
                    'unknown_field': 'resolve_unknown_field',
                })
            
        with self.assertRaises(UnknownRelationFieldNames):
            merge_policy = MergePolicy(
                self.db_adapter,
                policy={
                    self.ModelMergeOne: {
                        'f_integer': 'resolve_f_integer',  # not a relation
                    },
                })
        with self.assertRaises(UnknownRelationFieldNames):
            merge_policy.add_model_policy(
                self.ModelMergeThree,
                model_policy={
                    'f_integer': 'resolve_f_integer',  # not a relation
                })
            
        #--- wrong key for defaults
        with self.assertRaises(UnknownModelDefaultKey):
            merge_policy = MergePolicy(
                self.db_adapter,
                policy={},
                defaults={
                    self.ModelMergeTwo: {
                        'wrong_key': 'resolve_model_two',
                    },
                })
        with self.assertRaises(UnknownModelDefaultKey):
            merge_policy.add_model_policy(
                self.ModelMergeThree,
                model_policy={},
                model_defaults={
                    'wrong_key': 'resolve_model_two',
                })
        
        
        # merge policy must be the same as at the beginning
        clean_policy = create_policy()
        self.assertEqual(merge_policy, clean_policy)
        self.assertEqual(merge_policy.defaults, clean_policy.defaults)
        self.assertEqual(merge_policy.registered_models,
                         clean_policy.registered_models)