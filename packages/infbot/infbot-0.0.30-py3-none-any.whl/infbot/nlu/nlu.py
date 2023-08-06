# -*- coding: utf-8 -*-
"""
LU模块
"""

import numpy as np
from tqdm import tqdm
from ..common.user_action import UserAction
from .load_nlu_data import load_nlu_data
from .data_to_iob import data_to_iob
from .engine.ml_intent_classifier import MLIntentClassifier
from .engine.crf_slot_filler import CRFSlotFiller
from infbot.logger import logger


class NaturalLanguageUnderstanding(object):

    def __init__(self):
        self.ml_intent = None
        self.crf_slot = None
        self.slot_list = []
        self.intent_list = []
        self.domain_list = []

    def fit(self, data_path, faq_questions=None):
        """
        先从目录转换出所有的yml文件
        然后得到四个列表，分别是句子本身，槽，领域，意图，他们的长度是相等的
        例如一条句子：
        sentences: [ ['我', '爱', '你'] ]
        slots: [ 'O', 'O', 'O' ]
        domains: [ 'life' ]
        intents: [ 'ask_love' ]
        """
        raw_intents, raw_entities = load_nlu_data(data_path)
        sentences, slots, domains, intents = data_to_iob(
            raw_intents, raw_entities)

        slot_list = []
        for slot in slots:
            for s in slot:
                if s.startswith('B_'):
                    if s[2:] not in slot_list:
                        slot_list.append(s[2:])
        self.slot_list = sorted(set(slot_list))
        self.intent_list = sorted(set(intents))
        self.domain_list = sorted(set(domains))

        self.ml_intent = MLIntentClassifier()
        self.ml_intent.fit(sentences, domains, intents, faq_questions)
        self.crf_slot = CRFSlotFiller()
        self.crf_slot.fit(sentences, slots)

        loop = tqdm(zip(
            sentences, domains, intents),
            total=len(sentences))
        domain_ret, _ = self.ml_intent.predict_domains(sentences)
        intent_ret, _ = self.ml_intent.predict_intents(sentences)
        ret = []
        for (a, b, c), dr, ir in zip(loop, domain_ret, intent_ret):
            ret.append((
                b == dr,
                c == ir
            ))
        domain_accuracy, intent_accuracy = (
            np.sum([x[0] for x in ret]) / len(sentences),
            np.sum([x[1] for x in ret]) / len(sentences)
        )
        slot_accuracy, _ = self.crf_slot.eval(
            sentences,
            slots
        )
        logger.info(
            'domain_accuracy: %s\n' +
            'intent_accuracy: %s\n' +
            'slot_accuracy: %s\n',
            domain_accuracy,
            intent_accuracy,
            slot_accuracy
        )

    def forward(self, utterance):
        user_action = UserAction(utterance)
        if self.ml_intent:
            user_action.raw = self.ml_intent.predict_intent(user_action.raw)
            user_action.raw = self.ml_intent.predict_domain(user_action.raw)
        if self.crf_slot:
            user_action.raw = self.crf_slot.predict_slot(user_action.raw)
        return user_action
