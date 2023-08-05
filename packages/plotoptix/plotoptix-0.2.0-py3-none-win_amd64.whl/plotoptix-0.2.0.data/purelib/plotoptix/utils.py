"""Utility and convenience functions.
"""

import numpy as np

from typing import Any
from matplotlib import cm


def map_to_colors(x: Any, cm_name: str) -> np.ndarray:
    """
    Scale variable ``x`` to the range <0; 1> and map it to RGB colors from
    matplotlib's colormap with ``cm_name``.

    Parameters
    ----------
    x : array_like
        Input variable, array_like of any shape.
    cm_name : string
        Matplotlib colormap name.

    Returns
    -------
    out : np.ndarray
        Numpy array with RGB color values mapped from the input array values.
        The output shape is ``x.shape + (3,)``.
    """
    if x is None: raise ValueError()

    if not isinstance(x, np.ndarray): x = np.asarray(x)

    min_x = x.min()
    x = (1 / (x.max() - min_x)) * (x - min_x)

    c = cm.get_cmap(cm_name)(x)
    return np.delete(c, np.s_[-1], len(c.shape) - 1) # skip alpha
