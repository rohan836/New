"""Program execution and task-level rule induction."""

from __future__ import annotations

from typing import Iterable

from .primitives import PRIMITIVES, recolor
from .types import Grid, Operation, Program, Task


def execute(program: Program, grid: Grid) -> Grid:
    current = grid
    for operation in program.operations:
        if operation.name == "recolor":
            current = recolor(current, operation.params[0])
        else:
            try:
                transform = PRIMITIVES[operation.name]
            except KeyError as exc:
                raise ValueError(f"Unknown operation: {operation.name}") from exc
            current = transform(current)
    return current


def infer_recolor(task: Task) -> Operation | None:
    mapping: dict[int, int] = {}
    for example in task.train:
        if example.output is None:
            return None
        if len(example.input) != len(example.output) or len(example.input[0]) != len(example.output[0]):
            return None
        for in_row, out_row in zip(example.input, example.output):
            for src, dst in zip(in_row, out_row):
                previous = mapping.get(src)
                if previous is not None and previous != dst:
                    return None
                mapping[src] = dst
    pairs = tuple(sorted(mapping.items()))
    if all(src == dst for src, dst in pairs):
        return None
    return Operation("recolor", (pairs,))


def candidate_programs(task: Task, max_depth: int) -> Iterable[Program]:
    names = tuple(PRIMITIVES)
    yielded: set[tuple[tuple[str, tuple], ...]] = set()

    def emit(ops: tuple[Operation, ...]):
        key = tuple((op.name, op.params) for op in ops)
        if key not in yielded:
            yielded.add(key)
            yield Program(ops)

    yield from emit((Operation("identity"),))

    recolor_op = infer_recolor(task)
    if recolor_op is not None:
        yield from emit((recolor_op,))

    for name in names:
        yield from emit((Operation(name),))

    if max_depth >= 2:
        first_ops = [Operation(name) for name in names]
        if recolor_op is not None:
            first_ops.append(recolor_op)
        for first in first_ops:
            for second_name in names:
                yield from emit((first, Operation(second_name)))

    if max_depth >= 3:
        for first_name in (
            "rot90",
            "rot180",
            "rot270",
            "flip_h",
            "flip_v",
            "transpose",
            "mirror_quadrants",
        ):
            for second_name in names:
                for third_name in names:
                    yield from emit(
                        (
                            Operation(first_name),
                            Operation(second_name),
                            Operation(third_name),
                        )
                    )
