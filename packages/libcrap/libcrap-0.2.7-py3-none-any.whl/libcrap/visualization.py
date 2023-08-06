from more_itertools import unzip

import numpy as np

from typing import List, Iterable, Tuple, Callable, Any, TypeVar, Sequence, cast


T1 = TypeVar('T1')
T2 = TypeVar('T2')


def generate_points(
    func: Callable[[float], T1],
    start: float, end: float, num: int
) -> Tuple[List[float], List[T1]]:
    """Takes a mathematical function on real numbers and generates
    points for plotting it.
    Returns a list of 2 lists. The first list is x coordinates, the second is
    y coordinates.
    """
    return cast(
        Tuple[List[float], List[T1]],
        tuple(map(list, unzip((x, func(x)) for x in np.linspace(start, end, num))))
    )


# colorpicked from this image
# http://i.stack.imgur.com/pFuNR.png
# it was posted at http://goo.gl/8l2rND
_COLORS = ['#0000ff', '#ff0000', '#00ff00', '#00002b',
           '#ff1ab8', '#ffd300', '#005700', '#8383ff',
           '#9e4f46', '#00ffc1', '#008395', '#00007b',
           '#95d34f', '#f69edb', '#d311ff', '#7b1a69',
           '#f61160', '#ffc183', '#232308', '#8ca77b',
           '#f68308', '#837200', '#72f6ff', '#9ec1ff',
           '#72607b']


def get_distinguishable_colors(amount: int) -> List[str]:
    if not 0 <= amount <= len(_COLORS):
        raise ValueError('amount must be >= 0 and cannot be more than '
                         'the amount of colors this supports (that is {0})'
                         .format(len(_COLORS)))
    return _COLORS[:amount]
