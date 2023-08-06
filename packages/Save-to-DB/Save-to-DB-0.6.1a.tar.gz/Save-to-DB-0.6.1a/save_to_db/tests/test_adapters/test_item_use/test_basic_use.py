from save_to_db.exceptions import BulkItemOnetoXDefaultError, WrongAlias
from save_to_db.core.item import Item
from save_to_db.utils.test_base import TestBase



class TestBasicUse(TestBase):
    
    ModelFieldTypes = None
    ModelGeneralOne = None
    ModelGeneralTwo = None
    
    
    @classmethod
    def setup_models(cls, aliased=False):
        cls.item_cls_manager.clear()
        
        class ItemFieldTypes(Item):
            model_cls = cls.ModelFieldTypes
            conversions = {
                'decimal_separator': ',',
            }
        cls.ItemFieldTypes = ItemFieldTypes
        
        dct_1 = {'model_cls': cls.ModelGeneralOne}
        dct_2 = {'model_cls': cls.ModelGeneralTwo}
        
        if aliased:
            dct_1.update({
                'aliases': {
                    'alias_1': 'two_1_1__f_integer',
                    'alias_2': 'two_x_x__one_1_1__f_integer',
                }
            })
            dct_2.update({
                'aliases': {
                    'alias_1__post': 'f_string',
                    'alias_2__post': 'one_x_1__alias_1',
                    'alias_3__post': 'one_x_x__two_1_x__alias_1__post',
                }
            })
        
        cls.ItemGeneralOne = type('ItemGeneralOne', (Item,), dct_1)
        cls.ItemGeneralTwo = type('ItemGeneralTwo', (Item,), dct_2)
        
        cls.ItemGeneralOne.complete_setup()
        cls.ItemGeneralTwo.complete_setup()
    
    
    def test_setting_fields(self):
        self.setup_models()

        #--- setting with correct keys ---
        item = self.ItemGeneralOne()
        item['f_integer'] = '10'
        item['two_1_1__f_string'] = 'one'
        item['two_1_1__one_1_x__f_string'] = 'two'
        item['two_1_1__one_x_x__two_x_1__f_string'] = 'three'
        bulk = item['two_1_1__one_x_x']
        bulk['f_integer'] = '20'
        bulk.gen(f_text='four')
        in_bulk_item = bulk.gen(f_text='five')
        # setting field by calling
        in_bulk_item(f_string='ITEM_CALL') 
        bulk(two_x_1__f_text='BULK_CALL')
        
        expected_value = {
            'item': {
                'f_integer': '10',
                'two_1_1': {
                    'item': {
                        'f_string': 'one',
                        'one_1_x': {
                            'bulk': [],
                            'defaults': {
                                'f_string': 'two'
                            }
                        },
                        'one_x_x': {
                            'bulk': [
                                {
                                    'item': {
                                        'f_text': 'four'
                                    }
                                },
                                {
                                    'item': {
                                        'f_string': 'ITEM_CALL',
                                        'f_text': 'five'
                                    }
                                }
                            ],
                            'defaults': {
                                'f_integer': '20',
                                'two_x_1__f_string': 'three',
                                'two_x_1__f_text': 'BULK_CALL'
                            }
                        }
                    }
                }
            }
        }
        self.assertEqual(item.to_dict(), expected_value)
        
        #--- setting with incorrect keys ---
        item = self.ItemGeneralOne()
        with self.assertRaises(WrongAlias):
            item['wrong_key'] = 'value'
        
        bulk = self.ItemGeneralOne.Bulk()
        with self.assertRaises(WrongAlias):
            bulk['wrong_key'] = 'value'
            
        #--- setting one-to-x default value in bulk
        
        # not items temselves, can belong to different items
        bulk['two_1_1__f_integer'] = '10'
        bulk['two_1_x__f_integer'] = '10'
        bulk['two_x_x__one_1_x__f_integer'] = '10'
         
        # direct
        with self.assertRaises(BulkItemOnetoXDefaultError):
            bulk['two_1_1'] = self.ItemGeneralTwo()
         
        with self.assertRaises(BulkItemOnetoXDefaultError):
            bulk['two_1_x'] = self.ItemGeneralTwo()
         
        with self.assertRaises(BulkItemOnetoXDefaultError):
            bulk['two_1_x'].gen()
         
        with self.assertRaises(BulkItemOnetoXDefaultError):
            bulk['two_x_x__one_1_x'].gen()
        
        #--- aliases -----------------------------------------------------------
        self.setup_models(aliased=True)
        
        item = self.ItemGeneralOne()
        item['alias_1'] = '1'
        item['alias_2'] = '2'
        item['two_1_1__alias_1__post'] = 'str-1'
        item['two_1_1__alias_2__post'] = '3'
        item['two_1_1__alias_3__post'] = '4'
        bulk = item['two_1_x']
        bulk['alias_1__post'] = 'str-2'
        
        expected_value = {
            'id': 1,
            'item': {
                'two_x_x': {
                    'bulk': [],
                    'defaults': {
                        'one_1_1__f_integer': '2'  # alias_1
                    }
                },
                'two_1_1': {
                    'item': {
                        'f_integer': '1',  # alias_1
                        'one_x_1': {
                            'item': {
                                'two_1_1': {
                                    'item': {
                                        # two_1_1__alias_2__post
                                        'f_integer': '3'
                                    }
                                }
                            }
                        },
                        'one_x_x': {
                            'bulk': [],
                            'defaults': {
                                'two_1_x__f_string': '4'
                            }
                        },
                        'f_string': 'str-1'  # two_1_1__alias_1__post
                    }
                },
                'two_1_x': {
                    'bulk': [],
                    'defaults': {
                        'one_x_1': {
                            'id': 1
                        },
                        'f_string': 'str-2'
                    }
                }
            }
        }
        
        self.assertEqual(item.to_dict(), expected_value)
    
    
    def test_getting_fields(self):
        self.setup_models()
        
        item = self.ItemGeneralOne()
        related_item = item['two_x_1__one_1_1__two_1_1'](f_integer='20',
                                                         f_string='value')
        self.assertIsInstance(related_item, self.ItemGeneralTwo)
        
        expected_value = {
            'id': 2,
            'item': {
                'two_x_1': {
                    'id': 1,
                    'item': {
                        'f_integer': '20',
                        'f_string': 'value',
                        'one_1_1': {
                            'item': {
                                'two_1_1': {
                                    'id': 1
                                }
                            }
                        },
                        'one_1_x': {
                            'bulk': [
                                {
                                    'id': 2
                                }
                            ],
                            'defaults': {
                                'two_x_1': {
                                    'id': 1
                                }
                            }
                        }
                    }
                }
            }
        }
        
        self.assertEqual(item.to_dict(), expected_value)
        
        #--- aliases -----------------------------------------------------------
        self.setup_models(aliased=True)
        
        item = self.ItemGeneralOne()
        item['alias_1'] = '1'
        item['alias_2'] = '2'
        item['two_1_1__alias_1__post'] = 'str-1'
        item['two_1_1__alias_2__post'] = '3'
        item['two_1_1__alias_3__post'] = '4'
        bulk = item['two_1_x']
        bulk['alias_1__post'] = 'str-2'
        
        self.assertEqual(item['alias_1'], '1')
        self.assertEqual(item['alias_2'], '2')
        self.assertEqual(item['two_1_1__alias_1__post'], 'str-1')
        self.assertEqual(item['two_1_1__alias_2__post'], '3')
        self.assertEqual(item['two_1_1__alias_3__post'], '4')
        self.assertEqual(bulk['alias_1__post'], 'str-2')
    
    
    def test_getting_fields_reverse_autocomplete(self):
        self.setup_models()
        
        # --- single item ---
        
        # one-to-one
        item_one = self.ItemGeneralOne()
        item_two = item_one['two_1_1']
        self.assertTrue(item_two.is_single_item())
        self.assertIs(item_two['one_1_1'], item_one)
        
        # one-to-many
        item_one = self.ItemGeneralOne()
        bulk_two = item_one['two_1_x']
        self.assertTrue(bulk_two.is_bulk_item())
        self.assertIs(bulk_two['one_x_1'], item_one)  # default value
        
        # many-to-one
        item_one = self.ItemGeneralOne()
        item_two = item_one['two_x_1']
        self.assertTrue(item_two.is_single_item())
        self.assertTrue(item_two['one_1_x'].is_bulk_item())
        # must contain the item
        self.assertEqual(len(item_two['one_1_x']), 1)  # only 1 item
        self.assertIs(item_two['one_1_x'][0], item_one)
        # that item must have a default
        self.assertIs(item_two['one_1_x']['two_x_1'], item_two)
        
        # many-to-many
        item_one = self.ItemGeneralOne()
        bulk_two = item_one['two_x_x']
        self.assertTrue(bulk_two.is_bulk_item())
        self.assertTrue(item_one['two_x_x'].is_bulk_item())
        self.assertEqual(len(bulk_two['one_x_x']), 1)  # only 1 item
        # bulk item must have a default
        self.assertEqual(len(bulk_two['one_x_x']), 1)
        self.assertIs(bulk_two['one_x_x'][0], item_one)
        # but no items two were created
        self.assertEqual(len(bulk_two), 0)
   
    
    def test_del_from_item(self):
        self.setup_models()
        
        item = self.ItemGeneralOne()
        item['f_integer'] = '10'
        item['f_string'] = 'str-10'
        item['two_1_1__f_integer'] = '20'
        item['two_1_1__f_string'] = 'str-20'
        item['two_x_x__one_1_1__f_integer'] = '30'
        item['two_x_x__one_1_1__f_string'] = 'str-30'
        bulk = item['two_1_x']
        bulk['f_string'] = 'str-2'
        
        expect = {
            'item': {
                'two_1_1': {
                    'item': {
                        'f_integer': '20',
                        'f_string': 'str-20'
                    }
                },
                'two_x_x': {
                    'bulk': [],
                    'defaults': {
                        'one_1_1__f_integer': '30',
                        'one_1_1__f_string': 'str-30'
                    }
                },
                'f_integer': '10',
                'f_string': 'str-10',
                'two_1_x': {
                    'bulk': [],
                    'defaults': {
                        'one_x_1': {
                            'id': 1
                        },
                        'f_string': 'str-2'
                    }
                }
            },
            'id': 1
        }

        self.assertEqual(item.to_dict(), expect)
        
        del expect['item']['f_string']
        del item['f_string']
        self.assertEqual(item.to_dict(), expect)
        
        del expect['item']['two_1_1']['item']['f_string']
        del item['two_1_1__f_string']
        self.assertEqual(item.to_dict(), expect)
        
        del expect['item']['two_x_x']['defaults']['one_1_1__f_string']
        del item['two_x_x__one_1_1__f_string']
        self.assertEqual(item.to_dict(), expect)
        
        del bulk['f_string']
        del expect['item']['two_1_x']['defaults']['f_string']
        self.assertEqual(item.to_dict(), expect)
        
        #--- aliases -----------------------------------------------------------
        self.setup_models(aliased=True)
        
        item = self.ItemGeneralOne()
        item['alias_1'] = '1'
        item['alias_2'] = '2'
        item['two_1_1__alias_1__post'] = 'str-1'
        item['two_1_1__alias_2__post'] = '3'
        item['two_1_1__alias_3__post'] = '4'
        bulk = item['two_1_x']
        bulk['alias_1__post'] = 'str-2'
        
        expected_value = {
            'item': {
                'two_1_x': {
                    'defaults': {
                        'f_string': 'str-2',
                        'one_x_1': {
                            'id': 1
                        }
                    },
                    'bulk': []
                },
                'two_x_x': {
                    'defaults': {
                        'one_1_1__f_integer': '2'
                    },
                    'bulk': []
                },
                'two_1_1': {
                    'item': {
                        'f_string': 'str-1',
                        'one_x_1': {
                            'item': {
                                'two_1_1': {
                                    'item': {
                                        'f_integer': '3'
                                    }
                                }
                            }
                        },
                        'one_x_x': {
                            'defaults': {
                                'two_1_x__f_string': '4'
                            },
                            'bulk': []
                        },
                        'f_integer': '1'
                    }
                }
            },
            'id': 1
        }

        self.assertEqual(item.to_dict(), expected_value)
        
        del item['alias_1']
        del expected_value['item']['two_1_1']['item']['f_integer']
        self.assertEqual(item.to_dict(), expected_value)
        
        del item['alias_2']
        del expected_value['item']['two_x_x']['defaults']['one_1_1__f_integer']
        self.assertEqual(item.to_dict(), expected_value)
        
        del item['two_1_1__alias_1__post']
        del expected_value['item']['two_1_1']['item']['f_string']
        self.assertEqual(item.to_dict(), expected_value)
        
        del item['two_1_1__alias_2__post']
        del expected_value['item']['two_1_1']['item']['one_x_1']['item']['two_1_1']['item']['f_integer']
        self.assertEqual(item.to_dict(), expected_value)
        
        del item['two_1_1__alias_3__post']
        del expected_value['item']['two_1_1']['item']['one_x_x']['defaults']['two_1_x__f_string']
        self.assertEqual(item.to_dict(), expected_value)
        
        del bulk['alias_1__post']
        del expected_value['item']['two_1_x']['defaults']['f_string']
        self.assertEqual(item.to_dict(), expected_value)
    
    
    def test_contains(self):
        self.setup_models()
        item = self.ItemGeneralOne()
        item['f_integer'] = '1'
        item['two_1_x__f_integer'] = '2'
        bulk = item['two_1_x']
        bulk['one_x_x__f_integer'] = '3'
        
        self.assertIn('f_integer', item)
        self.assertIn('two_1_x__f_integer', item)
        self.assertIn('two_1_x__one_x_x__f_integer', item)  # from bulk
        
        self.assertNotIn('wrong_key', item)
        self.assertNotIn('wrong_key__f_integer', item)
        self.assertNotIn('two_1_x__one_x_x__wrong_key', item)
        
        self.assertIn('f_integer', bulk)  # item
        self.assertIn('one_x_x__f_integer', bulk)
        
        self.assertNotIn('wrong_key', bulk)
        self.assertNotIn('wrong_key__f_integer', bulk)
        self.assertNotIn('two_1_x__one_x_x__wrong_key', bulk)
        
        #--- aliased -----------------------------------------------------------
        self.setup_models(aliased=True)
        
        item = self.ItemGeneralOne()
        item['alias_1'] = '1'
        item['alias_2'] = '2'
        item['two_1_1__alias_1__post'] = 'str-1'
        item['two_1_1__alias_2__post'] = '3'
        item['two_1_1__alias_3__post'] = '4'
        bulk = item['two_1_x']
        bulk['alias_1__post'] = 'str-2'
        
        self.assertIn('alias_1', item)
        self.assertIn('alias_2', item)
        self.assertIn('two_1_1__alias_1__post', item)
        self.assertIn('two_1_1__alias_2__post', item)
        self.assertIn('two_1_1__alias_3__post', item)
        
        self.assertNotIn('wrong_key', item)
        self.assertNotIn('wrong_key__f_integer', item)
        self.assertNotIn('two_1_x__one_x_x__wrong_key', item)
        
        self.assertIn('alias_1__post', bulk)
        
        self.assertNotIn('wrong_key', bulk)
        self.assertNotIn('wrong_key__f_integer', bulk)
        self.assertNotIn('two_1_x__one_x_x__wrong_key', bulk)
    
    
    def test_bulk_iter(self):
        self.setup_models()
        bulk = self.ItemGeneralOne.Bulk()
        items = [bulk.gen(f_integer=1),
                 bulk.gen(f_integer=2),
                 bulk.gen(f_integer=3),]
        items_in_bulk = list(bulk)
        self.assertEqual(items_in_bulk, items)
        
        for item_no, item_in_bulk in enumerate(bulk):
            self.assertIs(items[item_no], item_in_bulk)
            self.assertIs(items[item_no], bulk[item_no])
        
        self.assertEqual(item_no, len(items)-1)
        
        
    def test_bulk_item_slice(self):
        class ItemsGeneralOne(Item):
            model_cls = self.ModelGeneralOne
                
        class ItemsGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
                
        
        bulk = ItemsGeneralOne.Bulk()
        bulk['f_string'] = 'str-value'
        
        items = []
        for i in range(10):
            item = ItemsGeneralOne(f_integer=i)
            items.append(item)
            bulk.add(item)
        
        first_slice = bulk[0:5]
        self.assertEqual(items[:5], first_slice.bulk)
        self.assertEqual(first_slice['f_string'], 'str-value')
        
        first_slice['f_text'] = 'text-value'
        self.assertNotIn('f_text', bulk)
        
        second_slice = bulk[0::2]
        self.assertEqual(items[0::2], second_slice.bulk)
        self.assertEqual(second_slice['f_string'], 'str-value')
        
        bulk['f_float'] = '10.10'
        self.assertNotIn('f_float', second_slice)
    
    
#     def test_x(self):
#         print('')
#         
#         class Instrument(Item):
#             model_cls = self.ModelGeneralOne
#                 
#         class Dividend(Item):
#             model_cls = self.ModelGeneralTwo
#         
#         dividend = Dividend(f_string='Dividend-1')
#         instrument = dividend['one_x_1']
#         instrument['f_string'] = 'Instrument-1'
#         dividend_2 = instrument['two_1_x'].gen(f_string='Dividend-2')
#         
# #         item_two['f_string'] = 'item_two'
#         
# #         item_two['one_1_x'].gen(f_string='1')
# # #         item_two['one_1_x'].gen(f_string='2')
# #         
# # #         item_one.process()
# #     
# #         print(item_one['two_x_1']['one_1_x'][0]['f_string'])
# #         print(item_one['two_x_1']['one_1_x'][1]['f_string'])
#         
# #         instrument.process()
#         dividend_2.pprint()