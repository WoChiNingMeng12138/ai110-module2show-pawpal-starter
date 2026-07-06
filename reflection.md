# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- My initial UML design separated the PawPal+ system into three main parts: data models, scheduling logic, and the Streamlit user interface. The goal was to keep the core scheduling logic independent from the UI so that it would be easier to test and maintain.

The main classes in my design were:

Owner: Stores basic information about the pet owner.
Pet: Stores information about the pet, including the pet's name, species, age, and any special notes.
CareTask: Represents a pet care task. Each task includes a name, category, duration, priority, and whether the task is required.
Scheduler: Contains the main scheduling logic. It sorts tasks based on priority and checks whether each task can fit within the owner’s available time.
DailyPlan: Stores the final generated plan, including scheduled tasks, skipped tasks, and the total time used.
ScheduleItem: Represents one task placed into the daily schedule, including its start and end time.
PlanExplanation: Stores the reasoning behind the generated plan, such as why certain tasks were selected or skipped.

In this design, the user enters owner, pet, and task information through the Streamlit interface. The UI then sends that information to the Scheduler, which generates a DailyPlan. The final plan and explanation are displayed back to the user.

**b. Design changes**

- My design changed slightly during implementation. I planned to add a skipped_tasks list to the DailyPlan class. In the initial design, I only planned to store scheduled tasks. During implementation, I realized that skipped tasks were important because the app needs to explain why some tasks were not included.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
