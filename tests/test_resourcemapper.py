#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
import os
import json
import datetime
from vnimport import resourcemapper

@pytest.fixture
def erogetrailers_response(fixture_path):
    filename = os.path.join(fixture_path, 'erogetrailers_response.json')
    with open(filename, 'r') as f:
        response = f.read()
    return json.loads(response.decode('utf-8'))

class TestErogetrailersResourceMapper:
    def setup(self):
        self.mapper = resourcemapper.ErogetrailersResourceMapper()
        
    def test_map_with_correct_types(self, erogetrailers_response):
        response = erogetrailers_response
        game_objs = self.mapper.map(response)
        assert len(response['items']) == len(game_objs)
        for game in game_objs:
            assert isinstance(game['original_name'], basestring)
            assert isinstance(game['roman_name'], basestring)
            assert isinstance(game['release_date'], datetime.datetime)
            assert isinstance(game['platform'], basestring)
            assert isinstance(game['getchu_id'], basestring)
            assert isinstance(game['developers'], list)
            if game['developers']:
                for developer in game['developers']:
                    assert isinstance(developer, basestring)
            assert isinstance(game['links'], list)
            if game['links']:
                for link in game['links']:
                    assert isinstance(link['name'], str)
                    assert isinstance(link['url'], str)