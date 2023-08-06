import math
from typing import Optional

import numpy as np
from scipy.spatial.distance import pdist, squareform


def solution(array: np.ndarray, n:Optional[int]=None, metric="euclidean", max_dist:Optional[float]=None, quantile:Optional[float]=None):
    """Solve the closest pairs problem.
    Args:
        array (np.ndarray): N x M
        n (int)

    """
    pairs = []
    distances = []

    distance_matrix = pdist(array, metric=metric)

    if quantile:
        max_dist = np.quantile(distance_matrix, quantile)
    elif quantile is None and max_dist is None:
        max_dist = 0.0037 # 3 SDs

    # Convert to square form
    distance_matrix = squareform(distance_matrix)

    # Identify closest pairs
    for idx, img in enumerate(distance_matrix):
        for idx2, dist in enumerate(img):
            if idx != idx2 and dist <= (max_dist or np.inf):
                if dist in distances:
                    continue
                print(idx, idx2, dist)
                pair = sorted([idx, idx2])
                pairs.append(pair)
                distances.append(dist)

    pairs = np.array(pairs, dtype=int)

    # Sort by distance
    indices = np.argsort(distances)
    distances = np.array(distances)[indices]

    if n is not None:
        return pairs[indices][:n], distances[:n]

    return pairs[indices], distances
