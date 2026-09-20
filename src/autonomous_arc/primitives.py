"""Small, executable ARC transformation primitives."""

from __future__ import annotations

from collections.abc import Callable
from .types import Grid, freeze_grid

Transform = Callable[[Grid], Grid]


def identity(grid: Grid) -> Grid:
    return grid


def rot90(grid: Grid) -> Grid:
    return freeze_grid([list(row) for row in zip(*grid[::-1])])


def rot180(grid: Grid) -> Grid:
    return freeze_grid([list(reversed(row)) for row in reversed(grid)])


def rot270(grid: Grid) -> Grid:
    return freeze_grid([list(row) for row in zip(*grid)][::-1])


def flip_h(grid: Grid) -> Grid:
    return freeze_grid([list(reversed(row)) for row in grid])


def flip_v(grid: Grid) -> Grid:
    return freeze_grid(list(reversed(grid)))


def transpose(grid: Grid) -> Grid:
    return freeze_grid([list(row) for row in zip(*grid)])


def crop_nonzero(grid: Grid) -> Grid:
    points = [(r, c) for r, row in enumerate(grid) for c, value in enumerate(row) if value != 0]
    if not points:
        return grid
    r0 = min(r for r, _ in points)
    r1 = max(r for r, _ in points)
    c0 = min(c for _, c in points)
    c1 = max(c for _, c in points)
    return freeze_grid([row[c0 : c1 + 1] for row in grid[r0 : r1 + 1]])


def mirror_quadrants(grid: Grid) -> Grid:
    top = [list(row) + list(reversed(row)) for row in grid]
    bottom_source = list(reversed(grid))
    bottom = [list(row) + list(reversed(row)) for row in bottom_source]
    return freeze_grid(top + bottom)


def scale2(grid: Grid) -> Grid:
    rows = []
    for row in grid:
        expanded = [value for value in row for _ in range(2)]
        rows.extend([expanded, list(expanded)])
    return freeze_grid(rows)


def recolor(grid: Grid, mapping: tuple[tuple[int, int], ...]) -> Grid:
    lut = dict(mapping)
    return freeze_grid([[lut.get(value, value) for value in row] for row in grid])


PRIMITIVES: dict[str, Transform] = {
    "identity": identity,
    "rot90": rot90,
    "rot180": rot180,
    "rot270": rot270,
    "flip_h": flip_h,
    "flip_v": flip_v,
    "transpose": transpose,
    "crop_nonzero": crop_nonzero,
    "mirror_quadrants": mirror_quadrants,
    "scale2": scale2,
}
