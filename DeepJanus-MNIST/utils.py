import matplotlib

from folder import Folder

matplotlib.use('Agg')


from os import makedirs
from os.path import exists, basename, join
import matplotlib.pyplot as plt
import matplotlib.cm as cm

#from tensorflow import keras
import keras



from properties import MODEL, IMG_SIZE
import numpy as np

# load the MNIST dataset
mnist = keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()


def input_reshape(x):
    # shape numpy vectors
    if keras.backend.image_data_format() == 'channels_first':
        x_reshape = x.reshape(x.shape[0], 1, 28, 28)
    else:
        x_reshape = x.reshape(x.shape[0], 28, 28, 1)
    x_reshape = x_reshape.astype('float32')
    x_reshape /= 255.0

    return x_reshape


def get_distance(v1, v2):
    return np.linalg.norm(v1 - v2)


def print_archive(archive):
    dst = Folder.DST_ARC+"_DJ"
    if not exists(dst):
        makedirs(dst)

    for i, ind in enumerate(archive):
        filename1 = join(dst, basename(
            'archived_' + str(i) + '_mem1_l_' + str(ind.member1.predicted_label) + '_seed_' + str(ind.seed)))
        plt.imsave(filename1, ind.member1.purified.reshape(28, 28), cmap=cm.gray, format='png')
        #loaded_label = (Predictor.predict(ind.member1.purified))
        #assert (ind.member1.predicted_label == loaded_label[0])
        #assert (ind.member1.predicted_label == Predictor.model.predict_classes(ind.member1.purified))
        np.save(filename1, ind.member1.purified)
        #loaded_label = Predictor.predict(np.load(filename1 + '.npy'))[0]
        #assert (ind.member1.predicted_label == loaded_label)
        assert (np.array_equal(ind.member1.purified, np.load(filename1 + '.npy')))

        filename2 = join(dst, basename(
            'archived_' + str(i) + '_mem2_l_' + str(ind.member2.predicted_label) + '_seed_' + str(ind.seed)))
        plt.imsave(filename2, ind.member2.purified.reshape(28, 28), cmap=cm.gray, format='png')
        #loaded_label = (Predictor.predict(ind.member2.purified))
        #assert (ind.member2.predicted_label == loaded_label[0])
        #assert (ind.member2.predicted_label == Predictor.model.predict_classes(ind.member2.purified))
        np.save(filename2, ind.member2.purified)
        #loaded_label = Predictor.predict(np.load(filename2 + '.npy'))[0]
        #assert (ind.member2.predicted_label == loaded_label)
        assert (np.array_equal(ind.member2.purified, np.load(filename2 + '.npy')))


def print_archive_experiment(archive):
    for i, ind in enumerate(archive):
        digit = ind.member1
        seed = reshape(x_test[int(digit.seed)])
        if get_distance(digit.purified, seed) < 2.0:
            digit.export()

        digit = ind.member2
        seed = reshape(x_test[int(digit.seed)])
        if get_distance(digit.purified, seed) < 2.0:
            digit.export()


# Useful function that shapes the input in the format accepted by the ML model.
def reshape(v):
    v = (np.expand_dims(v, 0))
    # Shape numpy vectors
    if keras.backend.image_data_format() == 'channels_first':
        v = v.reshape(v.shape[0], 1, IMG_SIZE, IMG_SIZE)
    else:
        v = v.reshape(v.shape[0], IMG_SIZE, IMG_SIZE, 1)
    v = v.astype('float32')
    v = v / 255.0
    return v
