import streamlit as st

from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app. Add pets, add tasks for them, and generate a
daily schedule using the backend logic in `pawpal_system.py`.
"""
)

st.divider()

# --- Owner: created once per session, then reused on every rerun ---
st.subheader("Owner")
owner_name = st.text_input("Owner name", value="Jordan")
available_minutes = st.number_input("Available minutes today", min_value=1, max_value=600, value=90)
col_start, col_end = st.columns(2)
with col_start:
    preferred_start_time = st.text_input("Preferred start time (HH:MM)", value="08:00")
with col_end:
    preferred_end_time = st.text_input("Preferred end time (HH:MM)", value="18:00")

if "owner" not in st.session_state:
    st.session_state.owner = Owner(
        name=owner_name,
        available_minutes=available_minutes,
        preferred_start_time=preferred_start_time,
        preferred_end_time=preferred_end_time,
    )
else:
    st.session_state.owner.update_info(
        name=owner_name,
        available_minutes=available_minutes,
        preferred_start_time=preferred_start_time,
        preferred_end_time=preferred_end_time,
    )

owner = st.session_state.owner

if "next_task_id" not in st.session_state:
    st.session_state.next_task_id = 1

st.divider()

# --- Adding a Pet ---
st.subheader("Adding a Pet")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])
age = st.number_input("Age", min_value=0, max_value=30, value=3)
notes = st.text_input("Notes", value="")

if st.button("Add pet"):
    if any(pet.name == pet_name for pet in owner.pets):
        st.warning(f"{pet_name} is already one of {owner.name}'s pets.")
    else:
        owner.add_pet(Pet(name=pet_name, species=species, age=int(age), notes=notes))
        st.success(f"Added {pet_name} the {species}.")

if owner.pets:
    st.write("Current pets:")
    st.table(
        [{"name": pet.name, "species": pet.species, "age": pet.age, "notes": pet.notes} for pet in owner.pets]
    )
else:
    st.info("No pets yet. Add one above.")

st.divider()

# --- Scheduling a Task ---
st.subheader("Scheduling a Task")

if owner.pets:
    task_pet_name = st.selectbox("Pet", [pet.name for pet in owner.pets])
    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col3:
        priority = st.selectbox("Priority", [1, 2, 3], index=0, help="1 = highest priority")

    if st.button("Add task"):
        target_pet = next(pet for pet in owner.pets if pet.name == task_pet_name)
        target_pet.add_task(
            Task(
                task_id=st.session_state.next_task_id,
                description=task_title,
                duration_minutes=int(duration),
                priority=priority,
            )
        )
        st.session_state.next_task_id += 1
        st.success(f"Added '{task_title}' for {task_pet_name}.")
else:
    st.info("Add a pet before scheduling tasks for it.")

all_tasks = owner.get_all_tasks()
if all_tasks:
    st.write("Current tasks:")
    st.table(
        [
            {
                "pet": pet.name,
                "task": task.description,
                "duration_minutes": task.duration_minutes,
                "priority": task.priority,
                "completed": task.completed,
            }
            for pet, task in all_tasks
        ]
    )
else:
    st.info("No tasks yet. Add one above.")

st.divider()

# --- Build Schedule ---
st.subheader("Build Schedule")

if st.button("Generate schedule"):
    scheduler = Scheduler()
    plan, explanation = scheduler.generate_plan(owner, date="2026-07-06")
    st.session_state.plan = plan
    st.session_state.explanation = explanation

if "plan" in st.session_state:
    st.text("Today's Schedule")
    st.code(st.session_state.plan.get_summary())
    with st.expander("Why this plan?"):
        st.text(st.session_state.explanation.get_explanation())
