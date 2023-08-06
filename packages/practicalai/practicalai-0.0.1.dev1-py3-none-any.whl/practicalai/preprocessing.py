def untokenize(indices, tokenizer):
    """Untokenize a list of indices into string.

    Arguments:
        indices {numpy.ndarray} -- array of token indicies
        tokenizer {Tokenizer} -- tf.keras Tokenizer object

    Returns:
        string -- untokenized string
    """
    return " ".join([tokenizer.index_word[index] for index in indices])