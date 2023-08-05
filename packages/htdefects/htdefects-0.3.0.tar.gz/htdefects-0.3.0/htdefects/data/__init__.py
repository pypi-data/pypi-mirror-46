# -*- coding: utf-8 -*-

""" Global lookup dictionaries of elemental property data."""

import os
import json

ELEM_VOLUMES = {}
current_file_dir = os.path.abspath(os.path.dirname(__file__))
elemental_volumes_file = os.path.join(current_file_dir,
                                      'elemental_volumes.json')
if os.path.isfile(elemental_volumes_file):
    with open(elemental_volumes_file) as fr:
        ELEM_VOLUMES = json.load(fr)
