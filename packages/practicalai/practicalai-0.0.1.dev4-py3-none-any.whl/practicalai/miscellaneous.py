import numpy as np


def generate_spiral_data(num_samples_per_class, input_dim, num_classes):
    """Generate non-linear spiral data.

    Arguments:
        num_samples_per_class {int} -- number of samples per class
        input_dim {int} -- input dimensionality
        num_classes {int} -- number of classes

    Returns:
        X {numpy.ndarray} -- synthetic inputs
        y {numpy.ndarray} -- synthetic outputs
    """
    # Make synthetic spiral data
    X_original = np.zeros((num_samples_per_class*num_classes, input_dim))
    y = np.zeros(num_samples_per_class*num_classes, dtype='uint8')
    for j in range(num_classes):
        ix = range(num_samples_per_class*j, num_samples_per_class*(j+1))
        r = np.linspace(0.0, 1, num_samples_per_class)  # radius
        t = np.linspace(j*4, (j+1)*4, num_samples_per_class) + \
            np.random.randn(num_samples_per_class)*0.2  # theta
        X_original[ix] = np.c_[r*np.sin(t), r*np.cos(t)]
        y[ix] = j

    # Stack
    X = np.hstack([X_original])

    return X, y
