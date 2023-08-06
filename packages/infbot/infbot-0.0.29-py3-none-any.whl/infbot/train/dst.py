# -*- coding: utf-8 -*-
"""训练DST部分"""

from ..dst.dst import DialogStateTracker
from infbot.logger import logger


def train_dst(x_dst, y_dst):
    dst = DialogStateTracker()
    dst.fit(x_dst, y_dst)

    logger.info('\n' + '-' * 30)
    logger.info('DST: trained')
    return dst
