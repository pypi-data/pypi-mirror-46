import datetime
from decimal import Decimal

from io import BytesIO
from save_to_db.core.item import Item
from save_to_db.utils.test_base import TestBase



class TestItemDump(TestBase):

    ModelGeneralOne = None
    ModelGeneralTwo = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        
        class ItemFieldTypes(Item):
            model_cls = cls.ModelFieldTypes
        cls.ItemFieldTypes = ItemFieldTypes
        
        class ItemGeneralOne(Item):
            model_cls = cls.ModelGeneralOne
        cls.ItemGeneralOne = ItemGeneralOne
        
        class ItemGeneralTwo(Item):
            model_cls = cls.ModelGeneralTwo
        cls.ItemGeneralTwo = ItemGeneralTwo
    
    
    def check_dumps(self, item, expected):
        # converting to bytes
        item_as_bytes = self.persister.dumps(item)
        self.assertIsInstance(item_as_bytes, bytes)
        
        item = self.persister.loads(item_as_bytes)    
        self.assertEqual(item.to_dict(), expected)
        
        # saving to a file-like object        
        storage = BytesIO()
        self.persister.dump(item, storage)
    
        storage.seek(0)
        item = self.persister.load(storage)
        self.assertEqual(item.to_dict(), expected)
    
    
    def test_dump_types(self):
        item = self.ItemGeneralOne(f_binary='binary data',
                                   f_boolean='true',
                                   f_string='string data',
                                   f_text='text_data',
                                   f_integer='10',
                                   f_float='10.10',
                                   f_date='2000-10-30',
                                   f_time='20:30:40',
                                   f_datetime='2000-10-30 20:30:40')
        expected = {
            'item': {
                'f_binary': b'binary data',
                'f_boolean': True,
                'f_date': datetime.date(2000, 10, 30),
                'f_datetime': datetime.datetime(2000, 10, 30, 20, 30, 40),
                'f_float': 10.1,
                'f_integer': 10,
                'f_string': 'string data',
                'f_text': 'text_data',
                'f_time': datetime.time(20, 30, 40),
            }
        }
        self.check_dumps(item, expected)


    def test_dump_single_item_with_relations(self):
        item = self.ItemGeneralOne(f_integer='1')
        item['two_1_1__f_integer'] = '11'
        item['two_x_x'].gen(f_float='99.1')
        item['two_x_x'].gen(f_float='99.2', one_x_1__f_integer='192') 
        item['two_x_x__f_float'] = '1000.1'
        
        expected = {
            'id': 1,
            'item': {
                'two_x_x': {
                    'defaults': {
                        'one_x_x': {
                            'defaults': {},
                            'bulk': [{
                                'id': 1
                            }]
                        },
                        'f_float': 1000.1
                    },
                    'bulk': [{
                        'item': {
                            'one_x_x': {
                                'defaults': {},
                                'bulk': [{
                                    'id': 1
                                }]
                            },
                            'f_float': 99.1
                        }
                    }, {
                        'id': 3,
                        'item': {
                            'one_x_1': {
                                'id': 2,
                                'item': {
                                    'two_1_x': {
                                        'defaults': {
                                            'one_x_1': {
                                                'id': 2
                                            }
                                        },
                                        'bulk': [{
                                            'id': 3
                                        }]
                                    },
                                    'f_integer': 192
                                }
                            },
                            'f_float': 99.2,
                            'one_x_x': {
                                'defaults': {},
                                'bulk': [{
                                    'id': 1
                                }]
                            }
                        }
                    }]
                },
                'f_integer': 1,
                'two_1_1': {
                    'item': {
                        'one_1_1': {
                            'id': 1
                        },
                        'f_integer': 11
                    }
                }
            }
        }
        
        self.check_dumps(item, expected)
        
        
    def test_dump_bulk_item_with_relations(self):
        bulk = self.ItemGeneralOne.Bulk()
        bulk.gen(f_float='1.1')
        bulk.gen(f_float='1.2', two_x_1__f_integer='2') 
        bulk['two_x_x__f_float'] = '1000.1'
        bulk['two_x_1'] = self.ItemGeneralTwo(f_boolean='true')

        expected = {
            'bulk': [{
                'id': 2
            }, {
                'item': {
                    'two_x_1': {
                        'item': {
                            'f_integer': 2,
                            'one_1_x': {
                                'bulk': [{
                                    'id': 4
                                }],
                                'defaults': {
                                    'two_x_1': {
                                        'id': 3
                                    }
                                }
                            }
                        },
                        'id': 3
                    },
                    'f_float': 1.2,
                    'two_x_x': {
                        'bulk': [],
                        'defaults': {
                            'f_float': 1000.1
                        }
                    }
                },
                'id': 4
            }],
            'defaults': {
                'two_x_x__f_float': 1000.1,
                'two_x_1': {
                    'item': {
                        'f_boolean': True,
                        'one_1_x': {
                            'bulk': [{
                                'item': {
                                    'two_x_1': {
                                        'id': 1
                                    },
                                    'f_float': 1.1,
                                    'two_x_x': {
                                        'bulk': [],
                                        'defaults': {
                                            'f_float': 1000.1
                                        }
                                    }
                                },
                                'id': 2
                            }],
                            'defaults': {
                                'two_x_1': {
                                    'id': 1
                                }
                            }
                        }
                    },
                    'id': 1
                }
            }
        }

        self.check_dumps(bulk, expected)
    
    
    def test_multiple_items_dump(self):
        storage = BytesIO()
        
        self.persister.dump(self.ItemGeneralOne(f_integer='1'), storage)
        self.persister.dump(self.ItemGeneralOne(f_integer='2'), storage)
        self.persister.dump(self.ItemGeneralOne(f_integer='3'), storage)
        
        storage.seek(0)
        
        dict_wrapper = self.persister.load(storage).to_dict()
        self.assertEqual(dict_wrapper, {'item': {'f_integer': 1}})
        
        dict_wrapper = self.persister.load(storage).to_dict()
        self.assertEqual(dict_wrapper, {'item': {'f_integer': 2}})
        
        dict_wrapper = self.persister.load(storage).to_dict()
        self.assertEqual(dict_wrapper, {'item': {'f_integer': 3}})
        
        # no more items
        dict_wrapper = self.persister.load(storage)
        self.assertIsNone(dict_wrapper)


    def test_arbitrary_id_position(self):
        # normal item
        item_one = self.ItemGeneralOne(f_integer='1')
        child_item = item_one['child_1_x'].gen(f_integer='2')
        item_one['child_x_x'].add(child_item)
        item_one.process()
        expect = {
            'id': 1,
            'item': {
                'child_1_x': {
                    'bulk': [
                        {
                            'id': 2,
                            'item': {
                                'f_integer': 2,
                                'parent_x_1': {
                                    'id': 1
                                },
                                'parent_x_x': {
                                    'bulk': [
                                        {
                                            'id': 1
                                        }
                                    ],
                                    'defaults': {}
                                }
                            }
                        }
                    ],
                    'defaults': {}
                },
                'child_x_x': {
                    'bulk': [
                        {
                            'id': 2
                        }
                    ],
                    'defaults': {}
                },
                'f_integer': 1
            }
        }
        loaded_item = self.ItemGeneralOne().load_dict(expect)
        self.assertEqual(loaded_item.to_dict(), expect)
        
        # moving parent data
        item_as_dict = {
            'id': 1,
            'item': {
                'child_1_x': {
                    'bulk': [
                        {
                            'id': 2
                        }
                    ],
                    'defaults': {}
                },
                'child_x_x': {
                    'bulk': [
                        {
                            'id': 2,
                            'item': {
                                'f_integer': 2,
                                'parent_x_1': {
                                    'id': 1
                                },
                                'parent_x_x': {
                                    'bulk': [
                                        {
                                            'id': 1
                                        }
                                    ],
                                    'defaults': {}
                                }
                            }
                        }
                    ],
                    'defaults': {}
                },
                'f_integer': 1
            }
        }
        loaded_item = self.ItemGeneralOne().load_dict(item_as_dict)
        self.assertEqual(loaded_item.to_dict(), expect)
        
        # id in default
        item_one = self.ItemGeneralOne.Bulk()
        item_one.gen(f_integer='1')
        other_item = item_one.gen(f_integer='2')
        item_one['parent_x_1'] = other_item
        item_one.process()
        expect = {
            'bulk': [
                {
                    'id': 2,
                    'item': {
                        'f_integer': 1,
                        'parent_x_1': {
                            'item': {
                                'child_1_x': {
                                    'bulk': [
                                        {
                                            'id': 2
                                        }
                                    ],
                                    'defaults': {}
                                },
                                'f_integer': 2
                            }
                        }
                    }
                },
                {
                    'id': 1
                }
            ],
            'defaults': {
                'parent_x_1': {
                    'id': 1,
                    'item': {
                        'f_integer': 2,
                        'parent_x_1': {
                            'item': {
                                'child_1_x': {
                                    'bulk': [
                                        {
                                            'id': 1
                                        }
                                    ],
                                    'defaults': {}
                                },
                                'f_integer': 2
                            }
                        }
                    }
                }
            }
        }
        loaded_item = self.ItemGeneralOne.Bulk().load_dict(expect)
        self.assertEqual(loaded_item.to_dict(), expect)
        
        # moving other item data
        item_as_dict = {
            'bulk': [
                {
                    'id': 2,
                    'item': {
                        'f_integer': 1,
                        'parent_x_1': {
                            'item': {
                                'child_1_x': {
                                    'bulk': [
                                        {
                                            'id': 2
                                        }
                                    ],
                                    'defaults': {}
                                },
                                'f_integer': 2
                            }
                        }
                    }
                },
                {
                    'id': 1,
                    'item': {
                        'f_integer': 2,
                        'parent_x_1': {
                            'item': {
                                'child_1_x': {
                                    'bulk': [
                                        {
                                            'id': 1
                                        }
                                    ],
                                    'defaults': {}
                                },
                                'f_integer': 2
                            }
                        }
                    }
                }
            ],
            'defaults': {
                'parent_x_1': {
                    'id': 1,
                  }
            }
        }
        loaded_item = self.ItemGeneralOne.Bulk().load_dict(item_as_dict)
        self.assertEqual(loaded_item.to_dict(), expect)
    
    
    def test_dump_instance_config(self):
        self.item_cls_manager.clear()
        
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            update_only_mode = True
        
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
            get_only_mode = True
            
        item_one_bulk = ItemGeneralOne.Bulk()
        item_one_bulk.gen(f_integer=1)
        
        item_one = item_one_bulk.gen(f_integer=2)
        item_one.get_only_mode = True
        item_one.update_only_mode = False
        
        
        item_one['two_1_x'].gen(f_integer=201)
        
        item_two = item_one['two_1_x'].gen(f_integer=202)
        item_two.get_only_mode = False
        item_two.update_only_mode = True
        
        expected = {
            'bulk': [
                {
                    'item': {
                        'f_integer': 1
                    }
                },
                {
                    'id': 1,
                    'item': {
                        'f_integer': 2,
                        'two_1_x': {
                            'bulk': [
                                {
                                    'item': {
                                        'f_integer': 201,
                                        'one_x_1': {
                                            'id': 1
                                        }
                                    }
                                },
                                {
                                    'item': {
                                        'f_integer': 202,
                                        'one_x_1': {
                                            'id': 1
                                        }
                                    },
                                    # overwritten values
                                    'get_only_mode': False,
                                    'update_only_mode': True
                                }
                            ],
                            'defaults': {
                                'one_x_1': {
                                    'id': 1
                                }
                            }
                        }
                    },
                    # overwritten values
                    'get_only_mode': True,
                    'update_only_mode': False
                }
            ],
            'defaults': {}
        }

        self.check_dumps(item_one_bulk, expected)


    def test_revert_and_to_dict(self):
        self.item_cls_manager.clear()
        
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            conversions = {
                'date_formats': '%d.%m.%Y',
                'time_formats': '%H-%M-%S',
                'datetime_formats': '%d.%m.%Y %H-%M-%S',
                'decimal_separator': '!',
            }
         
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
        
        # from single item -----------------------------------------------------
        one = ItemGeneralOne(f_integer='10',
                             f_decimal='10!10',
                             f_date='20.10.2010',
                             f_time='10-20-30',
                             f_datetime='20.10.2010 10-20-30')
        one['two_1_1'] = ItemGeneralTwo(f_integer='20',
                                        f_decimal='20.20',
                                        f_date='2010-10-20',
                                        f_time='10:20:30',
                                        f_datetime='2010-10-20 10:20:30')
        for i in range(3, 5):
            one['two_1_x'].gen(f_integer=i*10,
                               f_decimal='{}.{}'.format(i*10, i*10),
                               f_date='2010-10-20',
                               f_time='10:20:30',
                               f_datetime='2010-10-20 10:20:30')
        
        one.process()
        
        expect_processed = {
            'id': 1,
            'item': {
                'f_date': datetime.date(2010, 10, 20),
                'f_datetime': datetime.datetime(2010, 10, 20, 10, 20, 30),
                'f_decimal': Decimal('10.10'),
                'f_integer': 10,
                'f_time': datetime.time(10, 20, 30),
                'two_1_1': {
                    'item': {
                    'f_date': datetime.date(2010, 10, 20),
                       'f_datetime': datetime.datetime(2010, 10, 20,
                                                       10, 20, 30),
                       'f_decimal': Decimal('20.20'),
                       'f_integer': 20,
                       'f_time': datetime.time(10, 20, 30),
                       'one_1_1': {
                           'id': 1
                        }
                    }
                },
                'two_1_x': {
                    'bulk': [
                        {
                            'item': {
                                'f_date': datetime.date(2010, 10, 20),
                                'f_datetime': datetime.datetime(2010, 10, 20,
                                                                10, 20, 30),
                                'f_decimal': Decimal('30.30'),
                                'f_integer': 30,
                                'f_time': datetime.time(10, 20, 30),
                                'one_x_1': {
                                    'id': 1
                                }
                            }
                        },
                        {
                            'item': {
                                'f_date': datetime.date(2010, 10, 20),
                                'f_datetime': datetime.datetime(2010, 10, 20,
                                                                10, 20, 30),
                                'f_decimal': Decimal('40.40'),
                                'f_integer': 40,
                                'f_time': datetime.time(10, 20, 30),
                                'one_x_1': {
                                    'id': 1
                                }
                            }
                        }
                    ],
                    'defaults': {
                        'one_x_1': {
                            'id': 1
                        }
                    }
                }
            }
        }

        self.assertEqual(one.to_dict(), expect_processed)
        
        expect_reverted = {
            'id': 1,
            'item': {
                'f_date': '20.10.2010',
                'f_datetime': '20.10.2010 10-20-30',
                'f_decimal': '10!10',
                'f_integer': 10,
                'f_time': '10-20-30',
                'two_1_1': {
                    'item': {
                        'f_date': '2010-10-20',
                        'f_datetime': '2010-10-20 10:20:30',
                        'f_decimal': '20.20',
                        'f_integer': 20,
                        'f_time': '10:20:30',
                        'one_1_1': {
                            'id': 1
                        }
                    }
                },
                'two_1_x': {
                    'bulk': [
                        {
                            'item': {
                                'f_date': '2010-10-20',
                                'f_datetime': '2010-10-20 10:20:30',
                                'f_decimal': '30.30',
                                'f_integer': 30,
                                'f_time': '10:20:30',
                                'one_x_1': {
                                    'id': 1
                                }
                            }
                        },
                        {
                            'item': {
                                'f_date': '2010-10-20',
                                'f_datetime': '2010-10-20 10:20:30',
                                'f_decimal': '40.40',
                                'f_integer': 40,
                                'f_time': '10:20:30',
                                'one_x_1': {
                                    'id': 1
                                }
                            }
                        }
                    ],
                    'defaults': {
                        'one_x_1': {
                            'id': 1
                        }
                    }
                }
            }
        }

        self.assertEqual(one.to_dict(revert=True), expect_reverted)
        # original not changed
        self.assertEqual(one.to_dict(), expect_processed)
        
        # now all reverted
        one.revert()
        self.assertEqual(one.to_dict(), expect_reverted)
        self.assertEqual(one.to_dict(revert=True), expect_reverted)
        
        # again normal
        one.process()
        self.assertEqual(one.to_dict(), expect_processed)
        self.assertEqual(one.to_dict(revert=True), expect_reverted)
        
        # from bulk item -------------------------------------------------------
        bulk_one = ItemGeneralOne.Bulk(f_decimal='1000!1000')
        # bulk
        for i, j in zip(range(1, 3), range(3, 5)):
            bulk_one.gen(f_integer=i*10,
                         f_decimal='{}!{}'.format(i*10, i*10),
                         f_date='20.10.2010',
                         f_time='10-20-30',
                         f_datetime='20.10.2010 10-20-30')
            bulk_one['two_x_x'].gen(f_integer=j*10,
                                    f_decimal='{}.{}'.format(j*10, j*10),
                                    f_date='2010-10-20',
                                    f_time='10:20:30',
                                    f_datetime='2010-10-20 10:20:30')

        expect_processed = {
             'defaults': {
                 'two_x_x': {
                     'defaults': {},
                     'bulk': [{
                         'item': {
                             'f_integer': 30,
                             'f_date': datetime.date(2010, 10, 20),
                             'f_time': datetime.time(10, 20, 30),
                             'one_x_x': {
                                 'defaults': {
                                     'two_x_x': {
                                         'defaults': {},
                                         'bulk': [{
                                             'id': 1
                                         }]
                                     }
                                 },
                                 'bulk': [{
                                     'item': {
                                         'f_integer': 10,
                                         'f_date': datetime.date(2010, 10, 20),
                                         'f_time': datetime.time(10, 20, 30),
                                         'f_decimal': Decimal('10.10'),
                                         'two_x_x': {
                                             'defaults': {},
                                             'bulk': [{
                                                 'id': 1
                                             }, {
                                                 'item': {
                                                     'f_integer': 40,
                                                     'f_date':datetime.date(2010, 10, 20),
                                                     'f_time': datetime.time(10, 20, 30),
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
                                                             'id': 3
                                                         }, {
                                                             'item': {
                                                                 'f_integer': 20,
                                                                 'f_date': datetime.date(2010, 10, 20),
                                                                 'f_time': datetime.time(10, 20, 30),
                                                                 'f_decimal': Decimal('20.20'),
                                                                 'two_x_x': {
                                                                     'defaults': {},
                                                                     'bulk': [{
                                                                         'id': 1
                                                                     }, {
                                                                         'id': 2
                                                                     }]
                                                                 },
                                                                 'f_datetime': datetime.datetime(2010, 10, 20, 10, 20, 30)
                                                             },
                                                             'id': 4
                                                         }]
                                                     },
                                                     'f_decimal': Decimal('40.40'),
                                                     'f_datetime': datetime.datetime(2010, 10, 20, 10, 20, 30)
                                                 },
                                                 'id': 2
                                             }]
                                         },
                                         'f_datetime': datetime.datetime(2010, 10, 20, 10, 20, 30)
                                     },
                                     'id': 3
                                 }, {
                                     'id': 4
                                 }]
                             },
                             'f_decimal': Decimal('30.30'),
                             'f_datetime': datetime.datetime(2010, 10, 20, 10, 20, 30)
                         },
                         'id': 1
                     }, {
                         'id': 2
                     }]
                 },
                 'f_decimal': Decimal('1000.1000')
             },
             'bulk': [{
                 'id': 3
             }, {
                 'id': 4
             }]
         }
        
        bulk_one.process()
        self.assertEqual(bulk_one.to_dict(), expect_processed)
        
        expect_reverted = {
            'defaults': {
                'two_x_x': {
                    'defaults': {},
                    'bulk': [{
                        'item': {
                            'one_x_x': {
                                'defaults': {
                                    'two_x_x': {
                                        'defaults': {},
                                        'bulk': [{
                                            'id': 1
                                        }]
                                    }
                                },
                                'bulk': [{
                                    'item': {
                                        'f_integer': 10,
                                        'f_date': '20.10.2010',
                                        'f_decimal': '10!10',
                                        'f_time': '10-20-30',
                                        'two_x_x': {
                                            'defaults': {},
                                            'bulk': [{
                                                'id': 1
                                            }, {
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
                                                            'id': 3
                                                        }, {
                                                            'item': {
                                                                'f_integer': 20,
                                                                'f_date': '20.10.2010',
                                                                'f_decimal': '20!20',
                                                                'f_time': '10-20-30',
                                                                'two_x_x': {
                                                                    'defaults': {},
                                                                    'bulk': [{
                                                                        'id': 1
                                                                    }, {
                                                                        'id': 2
                                                                    }]
                                                                },
                                                                'f_datetime': '20.10.2010 10-20-30'
                                                            },
                                                            'id': 4
                                                        }]
                                                    },
                                                    'f_integer': 40,
                                                    'f_date': '2010-10-20',
                                                    'f_decimal': '40.40',
                                                    'f_time': '10:20:30',
                                                    'f_datetime': '2010-10-20 10:20:30'
                                                },
                                                'id': 2
                                            }]
                                        },
                                        'f_datetime': '20.10.2010 10-20-30'
                                    },
                                    'id': 3
                                }, {
                                    'id': 4
                                }]
                            },
                            'f_integer': 30,
                            'f_date': '2010-10-20',
                            'f_decimal': '30.30',
                            'f_time': '10:20:30',
                            'f_datetime': '2010-10-20 10:20:30'
                        },
                        'id': 1
                    }, {
                        'id': 2
                    }]
                },
                'f_decimal': '1000!1000'
            },
            'bulk': [{
                'id': 3
            }, {
                'id': 4
            }]
        }
        
        self.assertEqual(bulk_one.to_dict(revert=True), expect_reverted)
        # original not changed
        self.assertEqual(bulk_one.to_dict(), expect_processed)
        
        # all reverted
        bulk_one.revert()
        self.assertEqual(bulk_one.to_dict(revert=True), expect_reverted)
        self.assertEqual(bulk_one.to_dict(), expect_reverted)
        
        # back again
        bulk_one.process()
        self.assertEqual(bulk_one.to_dict(), expect_processed)
        self.assertEqual(bulk_one.to_dict(revert=True), expect_reverted)
    
    
    def test_multiple_date_time_formats_to_dict_revert(self):
        self.item_cls_manager.clear()
        self.item_cls_manager.autogenerate = True
        
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            conversions = {
                'date_formats': ['%d.%m.%Y', '%d.%m.%y'],
                'time_formats': ['%H:%M:%S', '%H:%M'],
                'datetime_formats': ['%d.%m.%Y %H:%M:%S', '%d.%m.%y %H:%M'],
            }
        
        # long format versions
        first_item = ItemGeneralOne(f_date='20.10.2010',
                                    f_time='10:20:30',
                                    f_datetime='20.10.2010 10:20:30')
        first_item.process()
        expect = {
            'item': {
                'f_time': datetime.time(10, 20, 30),
                'f_date': datetime.date(2010, 10, 20),
                'f_datetime': datetime.datetime(2010, 10, 20, 10, 20, 30),
            }
        }
        self.assertEqual(first_item.to_dict(), expect)
        
        first_item.revert()
        expect = {
            'item': {
                'f_time': '10:20:30',
                'f_datetime': '20.10.2010 10:20:30',
                'f_date': '20.10.2010',
            }
        }
        self.assertEqual(first_item.to_dict(), expect)
        
        # short format versions
        first_item = ItemGeneralOne(f_date='20.10.10',
                                    f_time='10:20',
                                    f_datetime='20.10.10 10:20')
        first_item.process()
        expect = {
            'item': {
                'f_time': datetime.time(10, 20, 0),
                'f_date': datetime.date(2010, 10, 20),
                'f_datetime': datetime.datetime(2010, 10, 20, 10, 20, 0),
            }
        }
        self.assertEqual(first_item.to_dict(), expect)
        
        first_item.revert()  # long versions will be used
        expect = {
            'item': {
                'f_time': '10:20:00',
                'f_datetime': '20.10.2010 10:20:00',
                'f_date': '20.10.2010',
            }
        }
        self.assertEqual(first_item.to_dict(), expect)

            