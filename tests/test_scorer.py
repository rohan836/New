import json

from autonomous_arc.scorer import score_prediction_dir


def test_missing_predictions_count_as_unsolved(tmp_path):
    task_dir = tmp_path / "tasks"
    prediction_dir = tmp_path / "predictions"
    task_dir.mkdir()
    prediction_dir.mkdir()

    (task_dir / "a.json").write_text(json.dumps({
        "train": [{"input": [[1]], "output": [[1]]}],
        "test": [{"input": [[2]], "output": [[2]]}]
    }))

    result = score_prediction_dir(task_dir, prediction_dir)

    assert result["tasks_evaluated"] == 1
    assert result["tasks_solved"] == 0
    assert result["task_accuracy"] == 0.0
