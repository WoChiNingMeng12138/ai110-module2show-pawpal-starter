"""Backend logic layer for PawPal+."""

from dataclasses import dataclass, field


@dataclass
class Task:
    task_id: int
    description: str
    duration_minutes: int
    priority: int  # 1 = highest priority
    frequency: str = "daily"
    required: bool = True
    completed: bool = False

    def mark_complete(self):
        """Mark this task as done."""
        self.completed = True


@dataclass
class Pet:
    name: str
    species: str
    age: int
    notes: str = ""
    tasks: list = field(default_factory=list)

    def add_task(self, task: Task):
        """Append a task to this pet's task list."""
        self.tasks.append(task)

    def get_tasks(self) -> list:
        """Return this pet's task list."""
        return self.tasks

    def update_info(self, **kwargs):
        """Update this pet's attributes from keyword arguments."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)


class Owner:
    def __init__(self, name: str, available_minutes: int, preferred_start_time: str, preferred_end_time: str):
        self.name = name
        self.available_minutes = available_minutes
        self.preferred_start_time = preferred_start_time
        self.preferred_end_time = preferred_end_time
        self.pets = []

    def add_pet(self, pet: Pet):
        """Add a pet to this owner's list of pets."""
        self.pets.append(pet)

    def get_all_tasks(self) -> list:
        """Return every task across all pets as (pet, task) pairs."""
        return [(pet, task) for pet in self.pets for task in pet.tasks]

    def update_info(self, **kwargs):
        """Update this owner's attributes from keyword arguments."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)


class ScheduleItem:
    def __init__(self, pet: Pet, task: Task, start_time: str, end_time: str):
        self.pet = pet
        self.task = task
        self.start_time = start_time
        self.end_time = end_time

    def display(self) -> str:
        """Return a one-line human-readable rendering of this scheduled item."""
        return f"{self.start_time}-{self.end_time}  {self.pet.name}: {self.task.description}"


class DailyPlan:
    def __init__(self, date: str):
        self.date = date
        self.scheduled_items = []
        self.skipped_tasks = []
        self.total_minutes = 0

    def add_item(self, item: ScheduleItem):
        """Add a scheduled item to the plan and track its minutes."""
        self.scheduled_items.append(item)
        self.total_minutes += item.task.duration_minutes

    def add_skipped(self, pet: Pet, task: Task):
        """Record a task that could not be fit into the plan."""
        self.skipped_tasks.append((pet, task))

    def get_summary(self) -> str:
        """Return a multi-line human-readable summary of the plan."""
        lines = [f"Plan for {self.date} ({self.total_minutes} min scheduled)"]
        lines += [item.display() for item in self.scheduled_items]
        if self.skipped_tasks:
            lines.append("Skipped:")
            lines += [f"  {pet.name}: {task.description}" for pet, task in self.skipped_tasks]
        return "\n".join(lines)


class PlanExplanation:
    def __init__(self):
        self.reasons = []

    def add_reason(self, reason: str):
        """Record one reason behind a scheduling decision."""
        self.reasons.append(reason)

    def get_explanation(self) -> str:
        """Return all recorded reasons as a multi-line string."""
        return "\n".join(self.reasons)


class Scheduler:
    def generate_plan(self, owner: Owner, date: str) -> tuple:
        """Build a DailyPlan and PlanExplanation from all of the owner's pet tasks."""
        plan = DailyPlan(date)
        explanation = PlanExplanation()

        pet_tasks = self.sort_tasks(owner.get_all_tasks())
        remaining_time = owner.available_minutes
        current_time = owner.preferred_start_time

        for pet, task in pet_tasks:
            if self.can_fit(task, remaining_time):
                end_time = self._add_minutes(current_time, task.duration_minutes)
                item = ScheduleItem(pet, task, current_time, end_time)
                plan.add_item(item)
                explanation.add_reason(
                    f"Scheduled '{task.description}' for {pet.name} at {current_time} "
                    f"(priority {task.priority})."
                )
                current_time = end_time
                remaining_time -= task.duration_minutes
            else:
                plan.add_skipped(pet, task)
                explanation.add_reason(
                    f"Skipped '{task.description}' for {pet.name}: not enough time remaining."
                )

        return plan, explanation

    def sort_tasks(self, pet_tasks: list) -> list:
        """Sort (pet, task) pairs by required-first, then priority."""
        return sorted(pet_tasks, key=lambda pt: (not pt[1].required, pt[1].priority))

    def can_fit(self, task: Task, remaining_time: int) -> bool:
        """Check whether a task's duration fits within the remaining time."""
        return task.duration_minutes <= remaining_time

    @staticmethod
    def _add_minutes(time_str: str, minutes: int) -> str:
        """Add minutes to an "HH:MM" time string and return the result."""
        hours, mins = map(int, time_str.split(":"))
        total = hours * 60 + mins + minutes
        return f"{(total // 60) % 24:02d}:{total % 60:02d}"
