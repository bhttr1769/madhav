
import json

import pytest

from brain.agents.models.workflow import Workflow, WorkflowStatus
from brain.agents.models.workflow_persistence_state import (
    WorkflowPersistenceState,
)
from brain.agents.models.workflow_step import (
    WorkflowStep,
    WorkflowStepStatus,
)
from brain.agents.persistence.json_workflow_persistence import (
    JsonWorkflowPersistence,
)


def make_state():
    workflow = Workflow(
        id="workflow-1",
        goal_id="goal-1",
        step_ids=("step-1", "step-2"),
        status=WorkflowStatus.RUNNING,
    )
    steps = (
        WorkflowStep(
            id="step-1",
            task_id="task-1",
            status=WorkflowStepStatus.COMPLETED,
        ),
        WorkflowStep(
            id="step-2",
            task_id="task-2",
            status=WorkflowStepStatus.READY,
        ),
    )
    return WorkflowPersistenceState(workflow=workflow, steps=steps)


def test_save_and_load_round_trip(tmp_path):
    persistence = JsonWorkflowPersistence(tmp_path)
    state = make_state()

    persistence.save(state)
    restored = persistence.load("workflow-1")

    assert restored == state


def test_load_from_new_instance(tmp_path):
    JsonWorkflowPersistence(tmp_path).save(make_state())

    restored = JsonWorkflowPersistence(tmp_path).load("workflow-1")

    assert restored == make_state()


def test_unknown_workflow_raises_key_error(tmp_path):
    persistence = JsonWorkflowPersistence(tmp_path)

    with pytest.raises(KeyError):
        persistence.load("unknown-workflow")


def test_invalid_workflow_id_is_rejected(tmp_path):
    persistence = JsonWorkflowPersistence(tmp_path)

    with pytest.raises((TypeError, ValueError)):
        persistence.load(" ")


def test_malformed_json_is_rejected(tmp_path):
    persistence = JsonWorkflowPersistence(tmp_path)
    path = persistence._path_for("workflow-1")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("{invalid json", encoding="utf-8")

    with pytest.raises(ValueError):
        persistence.load("workflow-1")


def test_unsupported_schema_version_is_rejected(tmp_path):
    persistence = JsonWorkflowPersistence(tmp_path)
    path = persistence._path_for("workflow-1")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "schema_version": 999,
                "workflow": {
                    "id": "workflow-1",
                    "goal_id": "goal-1",
                    "step_ids": [],
                    "status": "running",
                },
                "steps": [],
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError):
        persistence.load("workflow-1")


def test_mismatched_workflow_id_is_rejected(tmp_path):
    persistence = JsonWorkflowPersistence(tmp_path)
    persistence.save(make_state())

    path = persistence._path_for("workflow-1")
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["workflow"]["id"] = "workflow-2"
    path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(ValueError):
        persistence.load("workflow-1")


def test_invalid_workflow_or_step_state_is_rejected(tmp_path):
    persistence = JsonWorkflowPersistence(tmp_path)
    persistence.save(make_state())

    path = persistence._path_for("workflow-1")
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["steps"][0]["status"] = "not-a-valid-status"
    path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(ValueError):
        persistence.load("workflow-1")


def test_save_rejects_wrong_state_type(tmp_path):
    persistence = JsonWorkflowPersistence(tmp_path)

    with pytest.raises(TypeError):
        persistence.save(object())
