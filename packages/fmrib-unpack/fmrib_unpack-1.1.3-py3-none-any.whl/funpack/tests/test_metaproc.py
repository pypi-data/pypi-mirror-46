#!/usr/bin/env python
#
# test_metaproc.py -
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#


import random

from .. import metaproc_functions as metaproc
from .. import hierarchy
from .. import icd10



def test_icd10DescriptionFromNumeric():

    hier = hierarchy.getHierarchyFilePath(name='icd10')
    hier = hierarchy.loadHierarchyFile(hier)

    code = random.choice(hier.codings)
    ncode = icd10.codeToNumeric(code)
    desc = hier.description(code)

    gendesc = metaproc.icd10DescriptionFromNumeric(ncode)

    assert code in gendesc
    assert desc in gendesc



def test_icd10DescriptionFromCode():
    hier = hierarchy.getHierarchyFilePath(name='icd10')
    hier = hierarchy.loadHierarchyFile(hier)

    code = random.choice(hier.codings)
    desc = hier.description(code)

    gendesc = metaproc.icd10DescriptionFromCode(code)

    assert code in gendesc
    assert desc in gendesc
