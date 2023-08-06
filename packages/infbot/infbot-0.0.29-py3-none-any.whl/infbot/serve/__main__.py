
from .serve import Serve


def main(model_path, outside_function={}):
    s = Serve(model_path, outside_function)
    s.console()


if __name__ == '__main__':
    main()
