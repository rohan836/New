from autonomous_arc.solver import AutonomousSolver, SolverConfig
from autonomous_arc.types import Example, Task, freeze_grid


def g(rows):
    return freeze_grid(rows)


def test_solver_finds_mirror_rule():
    task = Task(
        task_id="mirror",
        train=(
            Example(
                g([[1, 0], [0, 2]]),
                g([[1, 0, 0, 1], [0, 2, 2, 0], [0, 2, 2, 0], [1, 0, 0, 1]]),
            ),
        ),
        test=(Example(g([[3, 0], [0, 4]])),),
    )
    result = AutonomousSolver(
        SolverConfig(max_depth=1, candidate_budget=32, attempts=2)
    ).solve(task)
    assert result.predictions[0][0] == g(
        [[3, 0, 0, 3], [0, 4, 4, 0], [0, 4, 4, 0], [3, 0, 0, 3]]
    )
    assert result.solved_by_verified_program
