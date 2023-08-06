# -*- coding: utf-8 -*-
"""
对话状态跟踪
"""

from typing import List
import numpy as np
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.svm import LinearSVC
from .keras_model import get_model
from ..common.dialog_state import DialogState
from ..common.user_action import UserAction
from ..common.build_dialog_train_data import make_new_state


class DialogStateTracker(object):

    def __init__(self):
        """初始化DST
        """
        self.clf = None

    def forward(self,
                init_state: DialogState,
                history: List[DialogState],
                user_action: UserAction):
        """
        input:
            state: current state
            user_action: action from this turn
        return: new_state DialogState
        """
        state = history[-1].clone()
        new_state = make_new_state(
            init_state.clone(),
            user_action.domain,
            user_action.intent,
            user_action.slots,
            user_action.utterance
        )
        # 只在domain不为空的时候修改domain
        if not state.user_domain or new_state.user_domain:
            state.user_domain = new_state.user_domain

        if self.clf is not None:
            x = np.array([
                s.vec
                for s in history
            ] + [new_state.vec])  # .flatten()

            pred = self.clf.predict_proba(np.array([x])).flatten()

            for i, slot in enumerate(new_state.slots):
                if pred[i] > 0.5:
                    state.slots[i] = slot

        state.user_intent = new_state.user_intent
        state.utterance = new_state.utterance
        return state

    def __len__(self):
        return len(self.slots)

    def fit(self, x, y):
        if y.shape[1] > 0:
            # clf = RandomForestClassifier(n_estimators=100)
            # clf = LinearSVC()
            clf = get_model(int(y.shape[-1]))
            clf.fit(x, y)
            print(f'DST FIT {clf.score(x, y)}')
            self.clf = clf
