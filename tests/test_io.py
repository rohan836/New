import json

from autonomous_arc.io import load_task, write_predictions
from autonomous_arc.types import freeze_grid


def test_task_loader_does_not_require_test_outputs(tmp_path):
    task_path = tmp_path / "x.json"
    task_path.write_text(json.dumps({
        "train": [{"input": [[1]], "output": [[2]]}],
        "test": [{"input": [[3]]}]
    }))
    task = load_task(task_path)
    assert task.test[0].output is None


def test_prediction_writer(tmp_path):
    path = tmp_path / "pred.json"
    write_predictions(path, "x", [[freeze_grid([[1]])]])
    payload = json.loads(path.read_text())
    assert payload["predictions"] == [[[1]]]
