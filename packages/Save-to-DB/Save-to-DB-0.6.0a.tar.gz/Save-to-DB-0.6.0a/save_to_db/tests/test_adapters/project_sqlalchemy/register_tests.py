from save_to_db.adapters.sqlalchemy_adapter import SqlachemyAdapter
from save_to_db.core.persister import Persister

from . import config
from .sqlalchemy_test_base import SqlalchemyTestBase

from .models.fields import ModelFieldTypes
from .models.constraints import (ModelConstraintsOne,
                                 ModelConstraintsTwo,
                                 ModelConstraintsThree,
                                 ModelConstraintsFour,
                                 ModelConstraintsFive,
                                 ModelConstraintsSix,
                                 ModelConstraintsSelf)
from .models.general import (ModelGeneralOne,
                             ModelGeneralTwo)
from .models.invalid_fields import ModelInvalidFieldNames
from .models.many_refs import ModelManyRefsOne, ModelManyRefsTwo
from .models.auto_reverse import (ModelAutoReverseOne,
                                  ModelAutoReverseTwoA,
                                  ModelAutoReverseTwoB,
                                  ModelAutoReverseThreeA,
                                  ModelAutoReverseThreeB,
                                  ModelAutoReverseFourA,
                                  ModelAutoReverseFourB)
from .models.merge import (ModelMergeOne,
                           ModelMergeTwo,
                           ModelMergeThree,
                           ModelMergeOneX,
                           ModelMergeTwoX,
                           ModelMergeThreeX) 

from .. import register_test
from ..test_fields_and_relations import TestFieldsAndRelations
from ..test_constraints import TestConstraints
from ..test_item_cls_manager import TestItemClsManager
from ..test_merge_policy import TestMergeModels, TestPolicySetup
from ..test_item_persist import (TestAdapter,
                                 TestExceptions,
                                 TestItemHooks,
                                 TestResolveModel,
                                 TestModelDeleter,
                                 TestNorewrite,
                                 TestPersist,
                                 TestReplace,
                                 TestSimpleConfig)
from ..test_item_use import (TestBasicUse,
                             TestItemDump,
                             TestItemProcess,
                             TestItemSetup)
from ..test_scope import TestScope
from ..test_select import TestSelect
from ..test_signals import TestSignals

AdapterPrefix = 'Sqlalchemy'
persister = Persister(SqlachemyAdapter({'session': config.session,
                                        'ModelBase': config.Base}),
                      autocommit=True)
models = {
    'ModelFieldTypes': ModelFieldTypes,
    
    'ModelGeneralOne': ModelGeneralOne,
    'ModelGeneralTwo': ModelGeneralTwo,
    
    'ModelConstraintsOne': ModelConstraintsOne,
    'ModelConstraintsTwo': ModelConstraintsTwo,
    'ModelConstraintsThree': ModelConstraintsThree,
    'ModelConstraintsFour': ModelConstraintsFour,
    'ModelConstraintsFive': ModelConstraintsFive,
    'ModelConstraintsSix': ModelConstraintsSix,
    'ModelConstraintsSelf': ModelConstraintsSelf,
    
    'ModelInvalidFieldNames': ModelInvalidFieldNames,
    
    'ModelManyRefsOne': ModelManyRefsOne,
    'ModelManyRefsTwo': ModelManyRefsTwo,
        
    'ModelAutoReverseOne': ModelAutoReverseOne,
    'ModelAutoReverseTwoA': ModelAutoReverseTwoA,
    'ModelAutoReverseTwoB': ModelAutoReverseTwoB,
    'ModelAutoReverseThreeA': ModelAutoReverseThreeA,
    'ModelAutoReverseThreeB': ModelAutoReverseThreeB,
    'ModelAutoReverseFourA': ModelAutoReverseFourA,
    'ModelAutoReverseFourB': ModelAutoReverseFourB,
    
    'ModelMergeOne': ModelMergeOne,
    'ModelMergeTwo': ModelMergeTwo,
    'ModelMergeThree': ModelMergeThree,
    'ModelMergeOneX': ModelMergeOneX,
    'ModelMergeTwoX': ModelMergeTwoX,
    'ModelMergeThreeX': ModelMergeThreeX,
}

for test_cls in (TestFieldsAndRelations,
                 TestConstraints,
                 TestItemClsManager,
                 TestMergeModels,
                 TestPolicySetup,
                 TestAdapter,
                 TestExceptions,
                 TestItemHooks,
                 TestResolveModel,
                 TestModelDeleter,
                 TestNorewrite,
                 TestPersist,
                 TestReplace,
                 TestSimpleConfig,
                 TestBasicUse,
                 TestItemDump,
                 TestItemProcess,
                 TestItemSetup,
                 TestItemDump,
                 TestScope,
                 TestSelect,
                 TestSignals):

    register_test(AdapterPrefix, SqlalchemyTestBase,
                  test_cls, models, persister)

