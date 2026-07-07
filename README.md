# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
# === Today's Schedule ===
# Plan for 2026-07-06 (55 min scheduled)
# 08:00-08:30  Mochi: Morning walk
# 08:30-08:40  Mochi: Give medication
# 08:40-08:55  Luna: Feed breakfast

# === Explanation ===
# Scheduled 'Morning walk' for Mochi at 08:00 (priority 1).
# Scheduled 'Give medication' for Mochi at 08:30 (priority 1).
# Scheduled 'Feed breakfast' for Luna at 08:40 (priority 2).
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Sorting by priority | `Scheduler.sort_tasks()` | Sorts `(pet, task)` pairs required-first, then by `priority` (1 = highest). Used for tasks with no fixed time. |
| Sorting by time | `Scheduler.sort_by_time()` | Sorts `(pet, task)` pairs by `Task.preferred_time` ("HH:MM" string, zero-padded so lexicographic order = chronological order). Tasks with no `preferred_time` sort last. Used to place fixed-time tasks in the day before flexible ones. |
| Filtering by pet / status | `Owner.filter_tasks(pet_name=None, completed=None)` | Single method that filters by pet name and/or completion status (either, both, or neither). `Owner.get_tasks_by_pet()` / `Owner.get_tasks_by_status()` and `Pet.get_tasks_by_status()` are thin wrappers over it for convenience. |
| Filtering by fit | `Scheduler.can_fit()` | Skips a task (adds it to `DailyPlan.skipped_tasks`) once the owner's remaining available minutes can't cover its duration. |
| Conflict detection | `Scheduler.detect_conflicts()`, `Scheduler._format_conflict()`, `DailyPlan.has_conflict()` | `detect_conflicts()` sweeps schedule items sorted by start time and reports every time overlap as a warning string — same-pet ("double-booked") and cross-pet ("schedule conflict between pets") are worded differently. It never raises; malformed items are filtered out rather than crashing the whole check. `generate_plan()` calls it automatically and stores the result on `DailyPlan.warnings`. `has_conflict()` is the simpler pairwise check `generate_plan()` uses while placing fixed-time tasks, to skip/shift a task before it's even added. |
| Recurring tasks | `Task.is_due()`, `Task.create_next_occurrence()`, `Pet.mark_task_complete()` | `Task.frequency` is `"daily"`, `"weekly"`, or `"once"`. `is_due(date)` checks whether an occurrence still needs doing on a given date. `Pet.mark_task_complete(task, date)` marks the task done and, for `"daily"`/`"weekly"` tasks, calls `create_next_occurrence()` (via `datetime.timedelta`) to append a fresh `Task` due 1 or 7 days later — so completing a recurring task automatically schedules its next occurrence. |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
