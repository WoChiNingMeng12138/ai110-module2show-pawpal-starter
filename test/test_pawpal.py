import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pawpal_system import Pet, Task


def test_task_completion():
    task = Task(task_id=1, description="Give medication", duration_minutes=10, priority=1)
    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


def test_task_addition():
    pet = Pet(name="Mochi", species="dog", age=3)
    assert len(pet.get_tasks()) == 0

    pet.add_task(Task(task_id=1, description="Morning walk", duration_minutes=30, priority=1))

    assert len(pet.get_tasks()) == 1
