from keras.layers import Input, Dense, Activation, ZeroPadding2D, BatchNormalization, Flatten, Conv2D
from keras.layers import AveragePooling2D, MaxPooling2D, Dropout, GlobalMaxPooling2D, GlobalAveragePooling2D
from keras.models import Model

from kt_utils import *

import keras.backend as K

import keras


def HappyModel(input_shape):
    """
    Implementation of the HappyModel.

    Arguments:
    input_shape -- shape of the images of the dataset

    Returns:
    model -- a Model() instance in Keras
    """

    # Feel free to use the suggested outline in the text above to get started, and run through the whole
    # exercise (including the later portions of this notebook) once. The come back also try out other
    # network architectures as well.

    # Define the input placeholder as a tensor with shape input_shape. Think of this as your input image!
    X_input = Input(input_shape)

    # Zero-Padding: pads the border of X_input with zeroes
    X = ZeroPadding2D((1, 1))(X_input)  # 66,66,3

    # CONV -> BN -> RELU Block applied to X
    X = Conv2D(8, (3, 3), strides=(1, 1), name='conv0')(X)  # 64,64,8
    X = BatchNormalization(axis=3, name='bn0')(X)  # axis=3 because channels is 3th([batch, height, width, channel])
    X = Activation('relu')(X)

    # MAXPOOL
    X = MaxPooling2D((2, 2), name='max_pool')(X)  # 32,32,8

    # FLATTEN X (means convert it to a vector) + FULLY CONNECTED
    X = Flatten()(X)
    X = Dense(1, activation='sigmoid', name='fc')(X)

    # Create model. This creates your Keras model instance, you'll use this instance to train/test the model.
    model = Model(inputs=X_input, outputs=X, name='HappyModel')

    return model


if __name__ == '__main__':
    K.set_image_data_format('channels_last')
    X_train_orig, Y_train_orig, X_test_orig, Y_test_orig, classes = load_dataset()

    # Normalize image vectors
    X_train = X_train_orig / 255.
    X_test = X_test_orig / 255.

    # Reshape
    Y_train = Y_train_orig.T
    Y_test = Y_test_orig.T

    print("number of training examples = " + str(X_train.shape[0]))
    print("number of test examples = " + str(X_test.shape[0]))
    print("X_train shape: " + str(X_train.shape))
    print("Y_train shape: " + str(Y_train.shape))
    print("X_test shape: " + str(X_test.shape))
    print("Y_test shape: " + str(Y_test.shape))

    '''
    2 - Building a model in Keras
    '''
    # 2-1 Create the model by calling the function above
    happyModel = HappyModel((64, 64, 3))

    # 2-2 Compile the model by calling
    happyModel.compile(optimizer=keras.optimizers.Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.0),
                       loss='binary_crossentropy', metrics=['accuracy'])
    # 2-3 Train the model on train data by calling
    happyModel.fit(x=X_train, y=Y_train, batch_size=16, epochs=20)
    # 2-4 Test the model on test data by calling
    preds = happyModel.evaluate(x=X_test, y=Y_test)

    print("Loss = " + str(preds[0]))
    print("Test Accuracy = " + str(preds[1]))

    happyModel.summary()
