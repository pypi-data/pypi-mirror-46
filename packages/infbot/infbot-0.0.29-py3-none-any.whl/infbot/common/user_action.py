# -*- coding: utf-8 -*-
"""
系统行为模块
NLU模块的输出
"""


class UserAction(object):

    def __init__(self, utterance):
        self.raw = {
            'text': utterance,
            'tokens': list(utterance),
            'intent': None,
            'domain': None,
            'slots': [],
        }

    def __getattr__(self, key):
        if key == 'utterance':
            return self.raw['text']
        if key == 'intent':
            return self.raw['intent']
        if key == 'domain':
            return self.raw['domain']
        if key == 'slots':
            return self.raw['slots']
        raise AttributeError(key)

    def __str__(self):
        return f'''domain: {self.raw.get('domain', None)}
intent: {self.raw.get('intent', None)}
slots: {self.raw.get('slots', None)}'''
