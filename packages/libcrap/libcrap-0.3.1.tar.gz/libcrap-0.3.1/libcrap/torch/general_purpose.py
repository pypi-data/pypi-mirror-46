import random

from typing import (
    Union, Callable, Any, Sequence, Iterable, Optional, List, Tuple, TypeVar, Dict, Callable
)

import numpy as np

import torch

from libcrap import get_now_as_str


def inverse_sigmoid(x: torch.Tensor) -> torch.Tensor:
    """Inverse of the sigmoid function, i.e., for any x,
    inverse_sigmoid(torch.sigmoid(x)) approximately equals x."""
    return torch.log(x / (torch.tensor(1.0, device=x.device) - x))


def set_random_seeds(device, seed_value=222):
    """Uses `seed_value` to fix random seeds of:
    * python standard library `random` module
    * numpy
    * pytorch (includes making cudnn deterministic)
    https://forums.fast.ai/t/solved-reproducibility-where-is-the-randomness-coming-in/31628/5

    `device` must be of type torch.device,
    `seed_value` must be int
    """
    np.random.seed(seed_value)
    torch.manual_seed(seed_value)
    random.seed(seed_value)
    if device.type == "cuda":
        torch.cuda.manual_seed(seed_value)
        torch.cuda.manual_seed_all(seed_value)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False
