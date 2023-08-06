import collections
import numpy as np
from sklearn.metrics import precision_recall_fscore_support


def get_performance(y_true, y_pred, classes):
    """Per-class performance metrics.

    Arguments:
        y_true {numpy.ndarray} -- ground truth values
        y_pred {numpy.ndarray} -- probability distributions (N, C)
        classes {list} -- list of classes

    Returns:
        performance {dict} -- dictionary of metrics
    """
    performance = {}
    y_pred = np.argmax(y_pred, axis=1)
    metrics = precision_recall_fscore_support(y_true, y_pred)
    # Per-class performance
    for i in range(len(classes)):
        performance[classes[i]] = {
            "precision": metrics[0][i],
            "recall": metrics[1][i],
            "f1": metrics[2][i],
            "num_samples": np.float64(metrics[3][i])
        }
    return performance


def get_probability_distributions(probabilities, classes):
    """Produce probability distributions with labels.

    Arguments:
        probabilities {numpy.ndarray} -- probabilities from inference
        classes {list} -- list of classes

    Returns:
        probability_distributions {list} -- probability distributions with class names
    """
    probability_distributions = []
    for i, y_prob in enumerate(probabilities):
        probability_distribution = {}
        for j, prob in enumerate(y_prob):
            probability_distribution[classes[j]] = np.float64(prob)
        probability_distribution = collections.OrderedDict(
            sorted(probability_distribution.items(), key=lambda kv: kv[1], reverse=True))
        probability_distributions.append(probability_distribution)
    return probability_distributions
