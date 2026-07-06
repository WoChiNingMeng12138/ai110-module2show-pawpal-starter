"""Backend logic layer for PawPal+.

Class skeletons generated from diagrams/class_diagram.mmd.
"""

from dataclasses import dataclass, field


@dataclass
class CareTask:
    task_id: int
    name: str
    category: str
    duration_minutes: int
    priority: int
    required: bool

    def update_task(self):
        pass


@dataclass
class Pet:
    name: str
    species: str
    age: int
    notes: str

    def update_info(self):
        pass


class Owner:
    def __init__(self, name: str, available_minutes: int, preferred_start_time: str, preferred_end_time: str):
        self.name = name
        self.available_minutes = available_minutes
        self.preferred_start_time = preferred_start_time
        self.preferred_end_time = preferred_end_time

    def update_info(self):
        pass


class ScheduleItem:
    def __init__(self, task: CareTask, start_time: str, end_time: str):
        self.task = task
        self.start_time = start_time
        self.end_time = end_time

    def display(self):
        pass


class DailyPlan:
    def __init__(self, date: str):
        self.date = date
        self.scheduled_items = []
        self.skipped_tasks = []
        self.total_minutes = 0

    def add_item(self):
        pass

    def get_summary(self):
        pass


class PlanExplanation:
    def __init__(self):
        self.reasons = []

    def add_reason(self, reason: str):
        pass

    def get_explanation(self) -> str:
        pass


class Scheduler:
    def generate_plan(self, owner: Owner, pet: Pet, tasks: list) -> DailyPlan:
        pass

    def sort_tasks(self, tasks: list) -> list:
        pass

    def can_fit(self, task: CareTask, remaining_time: int) -> bool:
        pass
