#!/usr/bin/env python
#
# icd10.py - Query the ICD10 disease coding hierarchy.
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#
"""This module contains functions for working with the `ICD10
<https://en.wikipedia.org/wiki/ICD-10>`_ disease coding hierarcy.


The :func:`codeToNumeric` function will take an ICD10 coding, and return
a numeric variant of it.


The :func:`storeCodes` function allows sets of ICD10 codes to be stored
so that they can be saved out to a file via the :func:`saveCodes` function, at
a later stage.
"""


import              logging
import itertools as it

import numpy     as np
import pandas    as pd

import funpack.hierarchy as hierarchy


log = logging.getLogger(__name__)


def codeToNumeric(code):
    """Converts an ICD10 code into a numeric version. """
    # We use the node IDs as defined
    # in the ICD10 hierarchy file as
    # the numeric version of each
    # coding.
    hier = hierarchy.getHierarchyFilePath(name='icd10')
    hier = hierarchy.loadHierarchyFile(hier)

    try:
        # hierarchy uses 0-indexing,
        # whereas the hierarchy files
        # use 1-indexing
        return int(hier.index(code) + 1)
    except KeyError:
        return np.nan


def numericToCode(code):
    """Converts a numeric ICD10 code into its original version. """
    hier = hierarchy.getHierarchyFilePath(name='icd10')
    hier = hierarchy.loadHierarchyFile(hier)

    try:
        return hier.coding(int(code - 1))
    except KeyError:
        return 'NaN'


def storeCodes(codes):
    """Stores the given sequence of ICD10 codes, so they can be exported to
    file at a later stage.

    The codes are stored in a list called ``store``, an attribute of this
    function.

    :arg codes: Sequence of ICD10 codes to add to the mapping file
    """
    store = getattr(storeCodes, 'store', [])
    store.append(codes)
    storeCodes.store = store


def saveCodes(fname, hierarchy, fields=None):
    """Saves any codes which have been stored via :func:`storeCodes` out to
    the specified file.

    :arg fname:     File to save the codes to.

    :arg hierarchy: :class:`.Hierarchy` object containing the ICD10
                    hierarchy information.

    :arg fields:    Sequence of fields to include in the ``mapfile``. Defaults
                    to ``['code', 'value', 'description', 'parent_descs]``. May
                    contain any of the following:
                      - ``'code'``
                      - ``'value'``
                      - ``'description'``
                      - ``'parent_codes'``
                      - ``'parent_descs'``
    """

    if fields is None:
        fields = ['code', 'value', 'description', 'parent_descs']

    valid = ['code', 'value', 'description', 'parent_codes', 'parent_descs']
    if not all([f in valid for f in fields]):
        raise ValueError('Invalid field in: {}'.format(fields))

    store = getattr(storeCodes, 'store', [])
    store = pd.Series(list(it.chain(*store)))
    store = store[store.notna()]
    codes = np.sort(store.unique())

    def parent_codes(c):
        return ','.join(reversed(hierarchy.parents(c)))

    def parent_descs(c):
        parents = reversed(hierarchy.parents(c))
        descs   = [hierarchy.description(p) for p in parents]
        return ' '.join(['[{}]'.format(d) for d in descs])

    df = pd.DataFrame({'code' : codes})

    for f in fields:
        if   f == 'code':         continue
        elif f == 'value':        func = codeToNumeric
        elif f == 'description':  func = hierarchy.description
        elif f == 'parent_codes': func = parent_codes
        elif f == 'parent_descs': func = parent_descs

        df[f] = df['code'].apply(func)

    log.debug('Saving %u ICD10 codes to %s', len(df), fname)

    df = df[fields]
    df.to_csv(fname, sep='\t', index=False)
