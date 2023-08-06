import numpy as np

def make_embeddings_matrix(embeddings, word_index, embedding_dim):
    """Create embeddings matrix to use in Embedding layer.

    Arguments:
        embeddings {dict} -- dictionary of tokens and their embeddings
        word_index {dict} -- dictionary of words and their indexes
        embedding_dim {[int} -- embedding dimensionality

    Returns:
        embedding_matrix {numpy.ndarray} -- matrix of embeddings
    """
    embedding_matrix = np.zeros((len(word_index) + 1, embedding_dim))
    for word, i in word_index.items():
        embedding_vector = embeddings.get(word)
        if embedding_vector is not None:
            embedding_matrix[i] = embedding_vector
    return embedding_matrix
