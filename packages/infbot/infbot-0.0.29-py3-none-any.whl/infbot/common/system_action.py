# -*- coding: utf-8 -*-
"""
记录系统行为（DP输出）
"""


class SystemAction(object):

    def __init__(self, sys_action):
        self.intent = sys_action

    def __str__(self):
        return f'{self.intent}'
