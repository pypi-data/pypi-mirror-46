from sklearn.model_selection import train_test_split

def train_val_test_split(X, y, val_size, test_size, shuffle):
    """Split data into train/val/test datasets.

    Arguments:
        X {numpy.ndarray} -- input array
        y {numpy.ndarray} -- output array
        val_size {float} -- proportion of data for validation set
        test_size {float} -- proportion of data for test set
        shuffle {bool} -- shuffle data

    Returns:
        X_train {numpy.ndarray} -- training inputs
        X_val {numpy.ndarray} -- validation inputs
        X_test {numpy.ndarray} -- test inputs
        y_train {numpy.ndarray} -- training outputs
        y_val {numpy.ndarray} -- validation outputs
        y_test {numpy.ndarray} -- test outputs
    """
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size,
        shuffle=shuffle, stratify=y)
    X_train, X_val, y_train, y_val = train_test_split(
        X_train, y_train, test_size=val_size,
        shuffle=shuffle, stratify=y_train)
    return X_train, X_val, X_test, y_train, y_val, y_test
