# -*- coding: utf-8 -*-
"""训练NLG部分"""

import os
from ..nlg.nlg import NaturalLanguageGenerator


def train_nlg(data_path):
    nlg_path = os.path.join(data_path, 'nlg')
    nlg = NaturalLanguageGenerator()
    nlg.fit(nlg_path)
    return nlg
