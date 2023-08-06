# -*- coding: utf-8 -*-
"""
使用sklearn中的机器学习算法进行意图识别

@TODO 现在只实现了一句话只存在一个意图、领域的情况，如果一句话存在多个领域和意图，在后续实现

python3 -m lu.engine.ml_intent_classifier

"""

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC, LinearSVC
from sklearn.metrics import (
    accuracy_score, precision_score,
    recall_score, f1_score)
from sklearn.model_selection import cross_validate
from sklearn.metrics import make_scorer
from .engine_core import EngineCore
from infbot.common import FAQ_INTENT
from infbot.logger import logger


class MLIntentClassifier(EngineCore):
    """注意文本都会变小写"""

    def __init__(self):
        """初始化"""
        super(MLIntentClassifier, self).__init__(
            domain_implement=True, intent_implement=True, slot_implement=False)
        self.vectorizer = None
        self.model_intent = None
        self.model_domain = None

    def build_vectorizer(self, feature):
        """构建预料表"""

        if feature == 'tfidf':
            v = TfidfVectorizer(
                analyzer='char', ngram_range=(1, 2), max_features=20000)
            self.vectorizer = v
        elif feature == 'hashing':
            v = HashingVectorizer(
                analyzer='char', ngram_range=(1, 2), n_features=500)
            self.vectorizer = v

        if self.vectorizer is None:
            raise Exception('Unknown feature "{}"'.format(feature))

    def build_model(self,
                    sentence_result, domain_result, intent_result,
                    feature, algorithm, faq_questions=None):
        """构建模型"""

        self.build_vectorizer(feature)

        x_text = [''.join(x).lower() for x in sentence_result]

        y_class_domain = domain_result
        y_class_intent = intent_result

        if faq_questions:
            x_text += [x.lower() for x in faq_questions]
            y_class_domain += [FAQ_INTENT] * len(faq_questions)
            y_class_intent += [FAQ_INTENT] * len(faq_questions)

        with open('/tmp/ml_intent_classifier.tmp', 'w') as fp:
            for x, y in zip(x_text, y_class_intent):
                fp.write('{}\t{}\n'.format(x, y))

        x_train = self.vectorizer.fit_transform(x_text)

        intent_class_index = {}
        intent_index_class = {}
        for i, c in enumerate(sorted(list(set(y_class_intent)))):
            intent_class_index[c] = i
            intent_index_class[i] = c
        self.intent_class_index = intent_class_index
        self.intent_index_class = intent_index_class

        logger.info(
            'ml_intent_classifier intent class %s',
            len(intent_class_index))

        y_train_intent = [intent_class_index[x] for x in intent_result]

        domain_class_index = {}
        domain_index_class = {}
        for i, c in enumerate(sorted(list(set(y_class_domain)))):
            domain_class_index[c] = i
            domain_index_class[i] = c
        self.domain_class_index = domain_class_index
        self.domain_index_class = domain_index_class

        logger.info(
            'ml_intent_classifier domain class %s',
            len(domain_class_index))

        y_train_domain = [domain_class_index[x] for x in domain_result]

        model_intent = None
        model_domain = None
        if algorithm == 'RandomForest':
            model_intent, model_domain = [
                RandomForestClassifier(
                    random_state=0, n_estimators=10, n_jobs=-1)
                for _ in range(2)
            ]
        elif algorithm == 'SVC':
            model_intent, model_domain = [
                SVC(random_state=0, probability=True, class_weight='balanced')
                for _ in range(2)
            ]
        elif algorithm == 'LinearSVC':
            model_intent, model_domain = [
                LinearSVC(random_state=0, class_weight='balanced')
                for _ in range(2)
            ]
        else:
            raise Exception('Unknown algorithm "{}"'.format(algorithm))

        return (model_intent, model_domain, x_train, y_train_intent,
                y_train_domain)

    def fit(self,
            sentence_result,
            domain_result,
            intent_result,
            faq_questions=None,
            feature='tfidf',
            algorithm='RandomForest'):
        """fit model"""

        logger.info('fit MLIntentClassifier')
        (model_intent, model_domain, x_train,
         y_train_intent, y_train_domain) = self.build_model(
             sentence_result, domain_result, intent_result,
             feature, algorithm, faq_questions)
        self.model_intent = model_intent
        self.model_intent.fit(x_train, y_train_intent)
        if len(set(y_train_domain)) >= 2:
            self.model_domain = model_domain
            self.model_domain.fit(x_train, y_train_domain)

    def predict_domain(self, nlu_obj):
        """预测领域"""
        tokens = nlu_obj['tokens']
        tokens = [x.lower() for x in tokens]
        ret = self.predict_domains([tokens])

        ml_ret = {
            'domain': ret[0][0],
            'domain_prob': ret[1][0],
        }
        if 'ml_intent_classifier' not in nlu_obj:
            nlu_obj['ml_intent_classifier'] = {}
        for k, v in ml_ret.items():
            nlu_obj['ml_intent_classifier'][k] = v
        if nlu_obj['domain'] is None:
            nlu_obj['domain'] = ml_ret['domain']
        return nlu_obj

    def predict_intent(self, nlu_obj):
        """预测意图"""
        tokens = nlu_obj['tokens']
        tokens = [x.lower() for x in tokens]
        ret = self.predict_intents([tokens])

        ml_ret = {
            'intent': ret[0][0],
            'intent_prob': ret[1][0],
        }
        if 'ml_intent_classifier' not in nlu_obj:
            nlu_obj['ml_intent_classifier'] = {}
        for k, v in ml_ret.items():
            nlu_obj['ml_intent_classifier'][k] = v
        if nlu_obj['intent'] is None:
            nlu_obj['intent'] = ml_ret['intent']
        return nlu_obj

    def predict_intents(self, sentence_result):
        """预测结果"""
        assert self.vectorizer is not None, 'vectorizer not fitted'
        assert self.model_intent is not None, 'model not fitted'

        x_test = self.vectorizer.transform(
            [''.join(x).lower() for x in sentence_result])

        y_pred_intent = self.model_intent.predict(x_test)
        if hasattr(self.model_intent, 'predict_proba'):
            y_prob_intent = self.model_intent.predict_proba(x_test).max(1)
        else:
            y_prob_intent = [[-1]] * len(y_pred_intent)

        return ([self.intent_index_class[x] for x in y_pred_intent],
                [x for x in y_prob_intent])

    def predict_domains(self, sentence_result):
        """预测结果"""
        assert self.vectorizer is not None, 'vectorizer not fitted'
        # assert self.model_domain is not None, 'model not fitted'
        if self.model_domain is None:
            return (
                [self.domain_index_class[0]] * len(sentence_result),
                [[1] * len(sentence_result)]
            )

        x_test = self.vectorizer.transform(
            [''.join(x).lower() for x in sentence_result])

        y_pred_domain = self.model_domain.predict(x_test)
        if hasattr(self.model_domain, 'predict_proba'):
            y_prob_domain = self.model_domain.predict_proba(x_test).max(1)
        else:
            y_prob_domain = [[-1]] * len(y_pred_domain)

        return ([self.domain_index_class[x] for x in y_pred_domain],
                [x for x in y_prob_domain])

    def eval(self, sentence_result, domain_result):
        """评估模型"""
        assert self.vectorizer is not None, 'vectorizer not fitted'
        assert self.model is not None, 'model not fitted'

        y_test = [x for x in domain_result]
        y_pred, _ = self.predict(sentence_result)

        metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred, average='weighted'),
            'recall': recall_score(y_test, y_pred, average='weighted'),
            'f1': f1_score(y_test, y_pred, average='weighted'),
        }

        bad = []
        for sent, r, p, in zip(sentence_result, y_test, y_pred):
            if r != p:
                bad.append((''.join(sent), r, p))

        metrics['bad'] = bad

        return metrics

    @staticmethod
    def cv_eval(sentence_result,
                domain_result,
                cv=5,
                feature='tfidf',
                algorithm='RandomForest'):
        """cv方法评估模型"""
        np.random.seed(0)
        ml = MLIntentClassifier()
        (model_intent, model_domain, x_train,
         y_train_intent, y_train_domain) = ml.build_model(
             sentence_result, domain_result, feature, algorithm)
        score = make_scorer(f1_score, average='weighted')
        logger.info('-' * 10 + ' domain test')
        cv_result = cross_validate(
            model_domain,
            x_train,
            y_train_domain,
            scoring=score,
            cv=cv,
            verbose=1)
        for k, v in cv_result.items():
            logger.info(k)
            logger.info(np.mean(v))
            logger.info(v)
        logger.info('-' * 10 + ' intent test')
        cv_result = cross_validate(
            model_intent,
            x_train,
            y_train_intent,
            scoring=score,
            cv=cv,
            verbose=1)
        for k, v in cv_result.items():
            logger.info(k)
            logger.info(np.mean(v))
            logger.info(v)
