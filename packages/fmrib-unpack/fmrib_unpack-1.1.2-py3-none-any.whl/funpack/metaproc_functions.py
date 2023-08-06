#!/usr/bin/env python
#
# metaproc_functions.py - Functions for manipulating column metadata.
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#
"""This module contains ``metaproc`` functions - functions for manipulating
column metadata.

Some :class:`.Column` instances have a ``metadata`` attribute, containing some
additional information about the column. The functions in this module can be
used to modify these metadata values. Currently, column metadata is only used
to generate a description of each column (via the ``--description_file``
command-line option).
"""


from . import icd10
from . import custom
from . import hierarchy


@custom.metaproc('icd10.numdesc')
def icd10DescriptionFromNumeric(val):
    """Generates a description for a numeric ICD10 code. """
    val  = icd10.numericToCode(val)
    hier = hierarchy.getHierarchyFilePath(name='icd10')
    hier = hierarchy.loadHierarchyFile(hier)
    desc = hier.description(val)
    return '{} - {}'.format(val, desc)


@custom.metaproc('icd10.codedesc')
def icd10DescriptionFromCode(val):
    """Generates a description for an ICD10 code. """
    hier = hierarchy.getHierarchyFilePath(name='icd10')
    hier = hierarchy.loadHierarchyFile(hier)
    desc = hier.description(val)
    return '{} - {}'.format(val, desc)
