import os
import django
from django.core.management import call_command

from save_to_db.adapters.django_adapter import DjangoAdapter
from save_to_db.core.persister import Persister

from . import project
from .project import settings
from .django_test_base import DjangoTestBase

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


# setting up Django and loading models
settings.INSTALLED_APPS = tuple(
    '{}.{}'.format(project.__name__, app) for app in settings.INSTALLED_APPS)
os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    '{}.settings'.format(project.__name__))
django.setup()
call_command('migrate', verbosity=0)
from .project.orm_only import models



AdapterPrefix = 'Django'
persister = Persister(DjangoAdapter({}))

models = {
    'ModelFieldTypes': models.ModelFieldTypes,
    
    'ModelGeneralOne': models.ModelGeneralOne,
    'ModelGeneralTwo': models.ModelGeneralTwo,

    'ModelConstraintsOne': models.ModelConstraintsOne,
    'ModelConstraintsTwo': models.ModelConstraintsTwo,
    'ModelConstraintsThree': models.ModelConstraintsThree,
    'ModelConstraintsFour': models.ModelConstraintsFour,
    'ModelConstraintsFive': models.ModelConstraintsFive,
    'ModelConstraintsSix': models.ModelConstraintsSix,
    'ModelConstraintsSelf': models.ModelConstraintsSelf,
    
    'ModelInvalidFieldNames': models.ModelInvalidFieldNames,

    'ModelManyRefsOne': models.ModelManyRefsOne,
    'ModelManyRefsTwo': models.ModelManyRefsTwo,
    
    'ModelAutoReverseOne': models.ModelAutoReverseOne,
    'ModelAutoReverseTwoA': models.ModelAutoReverseTwoA,
    'ModelAutoReverseTwoB': models.ModelAutoReverseTwoB,
    'ModelAutoReverseThreeA': models.ModelAutoReverseThreeA,
    'ModelAutoReverseThreeB': models.ModelAutoReverseThreeB,
    'ModelAutoReverseFourA': models.ModelAutoReverseFourA,
    'ModelAutoReverseFourB': models.ModelAutoReverseFourB,
    
    'ModelMergeOne': models.ModelMergeOne,
    'ModelMergeTwo': models.ModelMergeTwo,
    'ModelMergeThree': models.ModelMergeThree,
    'ModelMergeOneX': models.ModelMergeOneX,
    'ModelMergeTwoX': models.ModelMergeTwoX,
    'ModelMergeThreeX': models.ModelMergeThreeX,
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
    
    register_test(AdapterPrefix, DjangoTestBase,
                  test_cls, models, persister)