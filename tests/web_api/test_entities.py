# -*- coding: utf-8 -*-

from http.client import OK
from nose.tools import assert_equal
import json
import openfisca_country_template
from openfisca_core.commons import to_unicode
from . import subject

entities_response = subject.get('/entities')

# /entities


def test_return_code():
    assert_equal(entities_response.status_code, OK)


def test_response_data():
    entities = json.loads(entities_response.data.decode('utf-8'))
    test_documentation = to_unicode(openfisca_country_template.entities.Household.doc.strip())

    assert_equal(
        entities['household'],
        {
            'description': 'All the people in a family or group who live together in the same place.',
            'documentation': test_documentation,
            'plural': 'households',
            'roles': {
                'child': {
                    'description': 'Other individuals living in the household.',
                    'plural': 'children',
                    },
                'parent': {
                    'description': 'The one or two adults in charge of the household.',
                    'plural': 'parents',
                    'max': 2,
                    }
                }
            }
        )
