"""Manual test harness for pawpal_system.py logic."""

from pawpal_system import Owner, Pet, Task, Scheduler

owner = Owner(
    name="Jordan",
    available_minutes=90,
    preferred_start_time="08:00",
    preferred_end_time="10:00",
)

dog = Pet(name="Mochi", species="dog", age=3, notes="Needs daily walk")
cat = Pet(name="Luna", species="cat", age=5, notes="Indoor only")

owner.add_pet(dog)
owner.add_pet(cat)

dog.add_task(Task(task_id=1, description="Morning walk", duration_minutes=30, priority=1))
dog.add_task(Task(task_id=2, description="Give medication", duration_minutes=10, priority=1, required=True))
cat.add_task(Task(task_id=3, description="Feed breakfast", duration_minutes=15, priority=2))

scheduler = Scheduler()
plan, explanation = scheduler.generate_plan(owner, date="2026-07-06")

print("=== Today's Schedule ===")
print(plan.get_summary())

print("\n=== Explanation ===")
print(explanation.get_explanation())
