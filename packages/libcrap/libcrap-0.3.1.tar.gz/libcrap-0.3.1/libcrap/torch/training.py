import re
import os
import warnings

from typing import (
    Union, Callable, Any, Sequence, Iterable, Optional, List, Tuple, TypeVar, Dict, Callable
)

import torch
import torch.nn as nn
import torch.nn.functional as tnnf

from torchvision.utils import make_grid

from ignite.engine import (
    Engine, Events,
    create_supervised_trainer as _create_supervised_trainer,
    create_supervised_evaluator as _create_supervised_evaluator
)
from ignite.metrics import Metric
from ignite.handlers import TerminateOnNan, ModelCheckpoint, EarlyStopping
from ignite.contrib.handlers.tensorboard_logger import (
    TensorboardLogger, OutputHandler, WeightsScalarHandler, GradsScalarHandler,
    WeightsHistHandler, GradsHistHandler
)

from libcrap import get_now_as_str, FunctionWithEvents


ModelOutputType = TypeVar("ModelOutputType")
ModelInputType = TypeVar("ModelInputType")
BatchType = TypeVar("BatchType")
TargetType = TypeVar("TargetType")
PrepareBatchType = Callable[
    [BatchType],
    Tuple[ModelInputType, TargetType]
]


def _make_kwargs_for_ignite_create_func(device, prepare_batch):
    kwargs = {}
    if device is not None:
        kwargs["device"] = device
    if prepare_batch is not None:
        def prepare_batch_(batch, device, non_blocking):
            return prepare_batch(batch)
        kwargs["prepare_batch"] = prepare_batch_
    return kwargs


def setup_trainer(
    model: nn.Module, optimizer: torch.optim.Optimizer,
    loss_fn: Callable[[ModelOutputType, TargetType], torch.Tensor],
    device: Optional[torch.device] =None,
    prepare_batch: Optional[PrepareBatchType] =None
) -> Engine:
    trainer = _create_supervised_trainer(
        model, optimizer, loss_fn, **_make_kwargs_for_ignite_create_func(device, prepare_batch)
    )
    trainer.add_event_handler(Events.ITERATION_COMPLETED, TerminateOnNan())
    return trainer


def setup_evaluator(
    model: nn.Module, trainer: Engine,
    data_loader: Any, metrics: Dict[str, Metric],
    device: Optional[torch.device] =None,
    prepare_batch: Optional[PrepareBatchType] =None
) -> Engine:
    evaluator = _create_supervised_evaluator(
        model, metrics, **_make_kwargs_for_ignite_create_func(device, prepare_batch)
    )
    @trainer.on(Events.EPOCH_STARTED)
    def run_evaluator(trainer_: Engine) -> None:
        evaluator.run(data_loader)
    return evaluator


def add_checkpointing(
    directory: str, metric_name: str, evaluator: Engine,
    objects_to_save: Dict[str, Any],
    model: Optional[nn.Module] =None,
    filename_prefix: Optional[str] =None,
    num_checkpoints: int =1
) -> ModelCheckpoint:
    if (
        (model is None and filename_prefix is None)
        or (model is not None and filename_prefix is not None)
    ):
        raise ValueError("Exactly one of (model, filename_prefix) arguments must be passed")
    if filename_prefix is None:
        filename_prefix = get_model_name(model)
    checkpointer = ModelCheckpoint(
        dirname=directory,
        filename_prefix=filename_prefix + "_" + get_now_as_str(year=True, seconds=True),
        score_name=metric_name, n_saved=num_checkpoints,
        score_function=lambda evaluator_: -evaluator.state.metrics[metric_name]
    )
    evaluator.add_event_handler(
        Events.COMPLETED, checkpointer, objects_to_save
    )
    return checkpointer


class UnknownModelNameWarning(Warning):
    pass


def get_model_name(model: nn.Module):
    """For a model with string representation like
    BlahBlah(something=123, another_thing=[5, 6, "a"])
    returns 'blahblah'. If unable to determine a name in such a way,
    raises a warning and returns 'unknown'."""
    matches = re.findall("^([a-zA-Z]+)\(", str(model))
    if matches:
        return matches[0].lower()
    else:
        warnings.warn(UnknownModelNameWarning(
            "get_model_name couldn't determine name of the model"
        ))
        return "unknown"


def add_early_stopping(
    trainer: Engine,
    evaluator: Engine, metric: str, patience_num_evaluations: int,
    is_utility_function: bool =False
) -> EarlyStopping:
    def score_function(evaluator_: Engine) -> float:
        value = evaluator_.state.metrics[metric]
        if not is_utility_function:
            value *= -1
        return value
    handler = EarlyStopping(patience_num_evaluations, score_function, trainer)
    evaluator.add_event_handler(Events.COMPLETED, handler)
    return handler


def setup_tensorboard_logger(
    logs_base_dir: str,
    trainer: Engine,
    metric_names: Optional[Iterable[str]] =None,
    evaluators: Optional[Dict[str, Engine]] =None,
    model: Optional[nn.Module] =None,
    logs_subdir: Optional[str] =None,
) -> TensorboardLogger:
    """The returned object is a context manager, hence it should be closed when you finish
    using it.
    The returned logger will log loss obtained by `trainer` under 'train/loss',
    and for each (evaluator_name, evaluator) in `evaluators.items()`, for each
    metric name in `metric_names`, will log the value of the metric
    under '`evaluator_name`/`metric`'"""
    if logs_subdir is None:
        if model is None:
            raise ValueError("At least one of (logs_subdir, model) arguments must be passed")
        log_subdir = f"{get_model_name(model)}_{get_now_as_str(year=True, seconds=True)}"
    metric_names = list(metric_names)
    try:
        tb_logger = TensorboardLogger(os.path.join(logs_base_dir, log_subdir))
        tb_logger.attach(
            trainer, OutputHandler(tag="train", output_transform=lambda loss: {"loss": loss}),
            Events.ITERATION_COMPLETED
        )
        if evaluators:
            for (evaluator_name, evaluator) in evaluators.items():
                tb_logger.attach(
                    evaluator, OutputHandler(
                        tag=evaluator_name, metric_names=metric_names, another_engine=trainer
                    ),
                    Events.COMPLETED
                )
        return tb_logger
    except:
        tb_logger.close()
        raise


def add_weights_and_grads_logging(
    trainer: Engine, tb_logger: TensorboardLogger, model: nn.Module
) -> None:
    def abs_mean(tensor: torch.Tensor) -> torch.Tensor:
        with torch.no_grad():
            return tensor.abs().mean()

    for (handler, event) in (
        (WeightsScalarHandler(model, abs_mean), Events.ITERATION_COMPLETED),
        (GradsScalarHandler(model, abs_mean), Events.ITERATION_COMPLETED),
        (WeightsHistHandler(model), Events.EPOCH_COMPLETED),
        (GradsHistHandler(model), Events.EPOCH_COMPLETED)
    ):
        tb_logger.attach(trainer, handler, event)


def make_standard_prepare_batch_with_events(device: torch.device):
    @FunctionWithEvents
    def prepare_batch(batch: Tuple[torch.Tensor, torch.Tensor]) \
    -> Tuple[torch.Tensor, torch.Tensor]:
        return tuple(tensor.to(device) for tensor in batch)
    return prepare_batch


def add_logging_input_images(
    tb_logger: TensorboardLogger,
    engine: Engine,
    tag: str,
    prepare_batch: FunctionWithEvents,
    another_engine: Optional[Engine] =None,
    num_images: int =16
) -> None:
    """The function wrapped in prepare_batch must return a tuple of tensors, such that
    the tensor under index 0 is the desired tensor of images. (this is the standard
    prepare_batch function for supervised learning with images).
    Logging will happen once per engine's epoch. The will be logged under tag/input_images
    """
    engine_for_determining_epoch = another_engine if another_engine is not None else engine
    def make_funcs_with_closure():
        must_log = False
        def switch_flag(engine: Engine):
            nonlocal must_log
            assert must_log == False
            must_log = True
        def maybe_log_images(
            return_value: Any, batch: Tuple[torch.Tensor, torch.Tensor]
        ) -> None:
            batch_images = batch[0]
            nonlocal must_log
            if must_log:
                grid = make_grid(
                    batch_images[:num_images], nrow=min(8, num_images), normalize=True,
                    pad_value=1.0
                )
                tb_logger.writer.add_image(
                    f"{tag}/input_images", grid,
                    global_step=engine_for_determining_epoch.state.epoch
                )
                must_log = False
        return switch_flag, maybe_log_images
    switch_flag, maybe_log_images = make_funcs_with_closure()
    engine.add_event_handler(Events.EPOCH_STARTED, switch_flag)
    prepare_batch.after_call.append(maybe_log_images)
