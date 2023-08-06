
import sys
import pickle
from .nlu import NaturalLanguageUnderstanding  # noqa


def main(path):
    with open(path, 'rb') as fp:
        nlu = pickle.load(fp)
    while True:
        utterance = input('Utterance:')
        if utterance.lower() in ('quit', 'exit'):
            return
        user_action = nlu.forward(utterance)
        print(user_action)


if __name__ == '__main__':
    main(sys.argv[1])
