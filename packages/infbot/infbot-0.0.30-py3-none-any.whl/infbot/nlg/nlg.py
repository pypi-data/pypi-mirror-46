# -*- coding: utf-8 -*-
"""
NLG模块
"""

import os
import random
import yaml
from yaml import Loader
from ..common.system_action import SystemAction
from ..common.dialog_state import DialogState


class NaturalLanguageGenerator(object):

    def __init__(self, outside_function={}):
        self.intent_list = []
        self.slot_list = []
        self.mapping = {}
        self.outside_function = outside_function

    def fit(self, data_path):
        assert os.path.exists(data_path)
        data = {}
        for dirname, _, names in os.walk(data_path):
            names = [x for x in names if x.lower().endswith('.yml')]
            for name in names:
                path = os.path.join(dirname, name)
                obj = yaml.load(open(path), Loader=Loader)
                for k, v in obj.items():
                    assert k not in data
                    if v == 'function':
                        data[k] = ('func', k)
                    else:
                        data[k] = v
        self.mapping = data
        self.intent_list = sorted(data.keys())
        assert 'None' in self.mapping, \
            '应该有一个名为None的intent在NLG中，为了响应未知情况'

    def forward(self, state: DialogState, sys_action: SystemAction):
        assert (
            sys_action.intent is None
            or sys_action.intent in self.mapping
        ), 'sys_action {} not exists in mapping'.format(sys_action.intent)
        if sys_action.intent is None:
            response = self.mapping['None']
        else:
            response = self.mapping[sys_action.intent]
        if isinstance(response, list):
            utterance = random.choice(response)
        elif isinstance(response, tuple) \
                and len(response) == 2 and response[0] == 'func':
            utterance = self.outside_function[response[1]](state)
        else:
            raise RuntimeError('Invalid response')
        return utterance
