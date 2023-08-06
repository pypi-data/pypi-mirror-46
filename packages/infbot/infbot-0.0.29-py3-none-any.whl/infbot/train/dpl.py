# -*- coding: utf-8 -*-
"""训练DPL部分"""

from ..dpl.dpl import DialogPolicy
from infbot.logger import logger


def train_dpl(x_dpl, y_dpl):
    dpl = DialogPolicy()
    dpl.fit(x_dpl, y_dpl)

    logger.info('\n' + '-' * 30)
    logger.info('DPL: trained')
    return dpl
