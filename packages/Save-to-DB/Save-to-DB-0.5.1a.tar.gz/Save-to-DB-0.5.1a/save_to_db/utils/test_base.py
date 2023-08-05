import copy
from unittest import TestCase
from save_to_db.core import signals
from save_to_db.core.item_cls_manager import item_cls_manager
from save_to_db.core.scope import Scope




class TestBase(TestCase):
    
    item_cls_manager = item_cls_manager
    
    @classmethod
    def setUpClass(cls):
        cls.item_cls_manager.clear()
        Scope.clear()
        super().setUpClass()
        
        
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.item_cls_manager.clear()
        Scope.clear()
    
    
    def setUp(self):
        self.item_cls_manager.autogenerate = False
        self.__item_cls_manager_registry_before = \
            set(self.__class__.item_cls_manager.registry)
        self.__scope_registry_before = copy.deepcopy(Scope.registry)
        super().setUp()
        
    
    def tearDown(self):
        super().tearDown()
        self.__class__.item_cls_manager.registry = \
            self.__item_cls_manager_registry_before
        Scope.registry = self.__scope_registry_before
        for signal in signals.all_signals:
            signal.clear()
        
    
    def get_all_models(self, model_cls, sort_key=None):
        db_adapter = self.persister.db_adapter
        return db_adapter.get_all_models(model_cls, sort_key=sort_key)
        
        
    def get_related_x_to_many(self, model, field_name, sort_key=None):
        db_adapter = self.persister.db_adapter
        result = list(db_adapter.get_related_x_to_many(model, field_name))
        if sort_key:
            result.sort(key=sort_key)
        return result
