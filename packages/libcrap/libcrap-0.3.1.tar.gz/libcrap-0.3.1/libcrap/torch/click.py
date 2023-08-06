import random

from typing import Optional

import torch

import click

from . import set_random_seeds

def click_dataset_root_option(short_flag: Optional[str] ="-d"):
    return click.option(
        "--dataset-root", *([short_flag] if short_flag else []), required=True,
        type=click.Path(exists=True, dir_okay=True, file_okay=False),
        help="Dir where the dataset is saved or will be saved."
    )


def click_models_dir_option(short_flag: Optional[str] ="-m"):
    return click.option(
        "--models-dir", *([short_flag] if short_flag else []), required=True,
        type=click.Path(exists=True, dir_okay=True, file_okay=False, writable=True),
        help="Dir where checkpoint(s) of models and or optimizers will be saved."
    )


def click_tensorboard_log_dir_option(short_flag: Optional[str] ="-l"):
    return click.option(
        "--tb-log-dir", *([short_flag] if short_flag else []), required=True,
        type=click.Path(exists=True, dir_okay=True, file_okay=False, writable=True),
        help="Directory where tensorboard logs will be saved."
    )


def click_seed_and_device_options(
    seed_short_flag: Optional[str] ="-s", device_short_flag: Optional[str] ="-e",
    default_device: str ="cuda"
):
    """A decorator which adds 2 options to a click command: --device and --seed.
    When the command is run, if seed option is not passed, a random seed is generated.
    The seed and the device on which it is used are printed.
    Can be used like

    @click.command()
    @click_seed_and_device_options(device_short_flag="-D")
    def main(seed, device):
        assert isinstance(device, torch.device)
        assert isinstance(seed, int)
    """
    def decorate(func):
        @click.option(
            "--device", *([device_short_flag] if device_short_flag else []),
            type=str, default=default_device, help="Torch device"
        )
        @click.option(
            "--seed", *([seed_short_flag] if seed_short_flag else []),
            type=int, required=False,
            help="Initialize PRNGs with this seed number"
        )
        def decorated(**kwargs):
            kwargs = {**kwargs, "device": torch.device(kwargs["device"])}
            if kwargs["seed"] is None:
                kwargs = {**kwargs, "seed": random.randint(0, 2**32)}
            set_random_seeds(kwargs["device"], kwargs["seed"])
            print(f"Using seed {kwargs['seed']} (including on {kwargs['device']})")
            return func(**kwargs)
        return decorated
    return decorate
