from save_to_db.core.item import Item
from save_to_db.exceptions import MultipleModelsMatch, MultipleItemsMatch
from save_to_db.utils.test_base import TestBase



class TestExceptions(TestBase):
    
    ModelGeneralOne = None
    ModelGeneralTwo = None
    
    ModelManyRefsOne = None
    ModelManyRefsTwo = None
    
    ModelAutoReverseOne = None
    ModelAutoReverseTwoA = None
    ModelAutoReverseTwoB = None
    ModelAutoReverseThreeA = None
    ModelAutoReverseThreeB = None
    ModelAutoReverseFourA = None
    ModelAutoReverseFourB = None
    
    
    def test_multiple_items_match_exception(self):
        
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = [{'f_integer'}]
            getters = [{'f_integer'}, {'f_float'}]
        
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
        
        persister = self.persister
        
        # check for existing models
        persister.persist(ItemGeneralOne(f_integer=10, f_float=1))
        persister.persist(ItemGeneralOne(f_integer=20, f_float=2))
        
        bulk = ItemGeneralOne.Bulk()
        # two items will get the same model
        bulk.gen(f_integer=10, f_string='str-value-one')
        bulk.gen(f_float=1, f_string='str-value-two')
        
        with self.assertRaises(MultipleItemsMatch):
            persister.persist(bulk)
            
        # check for newly created models
        bulk = ItemGeneralOne.Bulk()
        bulk.gen(f_integer=10, f_float=1)
        bulk.gen(f_integer=20, f_float=1)
        
        with self.assertRaises(MultipleItemsMatch):
            persister.persist(bulk)
        
        # trying to create the same model twice
        bulk = ItemGeneralOne.Bulk()
        bulk.gen(f_integer=100)
        bulk.gen(f_integer=100)
        with self.assertRaises(MultipleItemsMatch):
            persister.persist(bulk)
    
    
    def test_multiple_models_match_exception(self):
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
        item = ItemGeneralOne(f_integer='100', f_float='200.200')
        persister.persist(item)
        item = ItemGeneralOne(f_integer='200', f_float='200.200')
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
        with self.assertRaises(MultipleModelsMatch):
            persister.persist(item)
        
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
        with self.assertRaises(MultipleModelsMatch):
            persister.persist(item)        
            
            
    def test_multiple_models_match_x_to_1_exception(self):
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
        
        #--- set two models to x-to-one field must fail ------------------------
        item_two = ItemGeneralTwo(f_integer='200')
        item_two['one_1_1'](f_float='200.200', f_text='text-1')
        with self.assertRaises(MultipleModelsMatch):
            persister.persist(item_two)