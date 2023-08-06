
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.layers import LSTM
from keras.wrappers.scikit_learn import KerasClassifier
from keras.utils import to_categorical


def make_model(n_size, n_output):

    model = Sequential()
    model.add(LSTM(n_size, dropout=0.1, recurrent_dropout=0.1))
    model.add(Dense(n_output))
    model.add(Activation('softmax'))

    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])

    return model


def get_model(n_output, n_size=32, epochs=20, batch_size=32):
    return KerasClassifier(
        make_model,
        batch_size=batch_size,
        n_output=n_output,
        epochs=epochs,
        n_size=n_size
    )


if __name__ == '__main__':
    x_train = np.random.random((1000, 5, 30))
    y_train = np.random.randint(0, 5, size=(1000, 1))
    y_train = to_categorical(y_train)
    model = get_model(5)
    model.fit(x_train, y_train)
    p_test = model.predict(x_train)
    print(p_test.shape)
