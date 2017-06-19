# -*- coding: utf-8 -*-

import os
import json
from httplib import BAD_REQUEST, NOT_FOUND

from nose.tools import assert_equal, assert_in
import dpath

from . import subject


def post_json(data = None, file = None):
    if file:
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', file_name)
        with open(file_path, 'r') as file:
            data = file.read()
    return subject.post('/calculate', data = data, content_type = 'application/json')


invalid_json_response = post_json('{"a" : "x", "b"}')


def test_invalid_json_return_code():
    assert_equal(invalid_json_response.status_code, BAD_REQUEST)


def test_invalid_json_response_content():
    response = json.loads(invalid_json_response.data)
    error_message = response['error']
    assert_in('Invalid JSON', error_message)
    # The clients get details about where and why the JSON is invalid
    assert_in('line', error_message)
    assert_in('column', error_message)


def check_response(data, expected_error_code, path_to_check, content_to_check):
    response = post_json(data)
    try:
        assert_equal(response.status_code, expected_error_code)
        json_response = json.loads(response.data)
        content = dpath.util.get(json_response, path_to_check)
        assert_in(content_to_check, content)
    except:
        import nose.tools; nose.tools.set_trace(); import ipdb; ipdb.set_trace()


def test_incorrect_inputs():
    tests = [
        ('["An", "array"]', BAD_REQUEST, 'error', 'Invalid type'),
        ('{"unknown_entity": {}}', BAD_REQUEST, 'unknown_entity', 'entity is not defined',),
        ('{"households": {"dupont": {"parents": {}}}}', BAD_REQUEST, 'households/dupont/parents', 'type',),
        ('{"persons": {"bob": {"unknown_variable": {}}}}', NOT_FOUND, 'persons/bob/unknown_variable', 'You tried to calculate or to set',),
        ('{"persons": {"bob": {"housing_allowance": {}}}}', BAD_REQUEST, 'persons/bob/housing_allowance', 'housing_allowance is only defined for households',),
        # ('{"persons": {"bob": {"salary": 4000 }}}', BAD_REQUEST, 'persons/bob/salary', 'period',),

        ]

    for test in tests:
        yield (check_response,) + test
