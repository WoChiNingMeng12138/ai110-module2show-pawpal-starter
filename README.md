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
python -m pytest

# Run with coverage:
pytest --cov
```

The suite covers the three areas most likely to break silently in a scheduler with sorting and recurring tasks:

- **Sorting correctness** — `Scheduler.sort_tasks()` orders required-before-optional then by priority (including the empty-list edge case), and `Scheduler.sort_by_time()` orders by `preferred_time` with tasks missing a preferred time sorted last.
- **Recurrence logic** — completing a `"daily"`/`"weekly"` task creates a next occurrence due 1/7 days later and appends it to the pet's task list, while a `"once"` task creates nothing.
- **Conflict detection** — `DailyPlan.has_conflict()` and `Scheduler.detect_conflicts()` correctly flag true overlaps (same-pet and cross-pet) but not back-to-back or non-overlapping items, and a pet with no tasks produces an empty plan without crashing.

Sample test output:

```
============================================================================ test session starts ============================================================================
platform win32 -- Python 3.14.0, pytest-9.0.3, pluggy-1.6.0
rootdir: F:\UniversityDocument\US_TAMU\2026_Summer\Interview\ai110-module2show-pawpal-starter
plugins: anyio-4.13.0
collected 18 items

test\test_pawpal.py ..................                                                                                                                                 [100%]

============================================================================= 18 passed in 0.03s =============================================================================
```

**Confidence level: 4/5 stars.** All 18 tests pass, and the core sorting, recurrence, and conflict-detection paths are verified — including edge cases like empty task lists and boundary-touching time slots. The point held back from 5/5: while writing these tests we found that the fixed-time conflict-skip branch inside `Scheduler.generate_plan()` is currently unreachable in practice, since `current_time` only ever advances forward, two fixed-time tasks requested at the same slot get staggered automatically instead of ever hitting that skip path. That's not an incorrect result, just an untested/dead code path worth a closer look before calling the scheduler fully verified.

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
