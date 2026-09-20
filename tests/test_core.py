from autonomous_arc.program import execute, infer_recolor
from autonomous_arc.types import Example, Operation, Program, Task, freeze_grid


def g(rows):
    return freeze_grid(rows)


def test_rotation():
    assert execute(
        Program((Operation("rot90"),)),
        g([[1, 2], [3, 4]]),
    ) == g([[3, 1], [4, 2]])


def test_recolor_inference():
    task = Task(
        task_id="x",
        train=(
            Example(g([[1, 0], [0, 1]]), g([[2, 0], [0, 2]])),
            Example(g([[1, 1], [0, 0]]), g([[2, 2], [0, 0]])),
        ),
        test=(Example(g([[1]])),),
    )
    op = infer_recolor(task)
    assert op is not None
    assert op.name == "recolor"
    assert execute(Program((op,)), task.train[0].input) == task.train[0].output
