import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()
Faker.seed(42)
random.seed(42)

# 👥 צוות מדומה
employees = ['Alice', 'Bob', 'Charlie', 'Dana', 'Eli']

# הגדרות כלליות
n_tasks = 60
start_date = datetime.now() - timedelta(days=7)
tasks = []

# ספציפית: Eli מגיב לאט, Dana מקבלת המון, Charlie כמעט לא פעיל
employee_weights = {
    'Alice': 1.0,
    'Bob': 1.0,
    'Charlie': 0.2,  # כמעט לא מקבל משימות
    'Dana': 2.0,     # מקבלת הרבה משימות
    'Eli': 1.0
}

last_end_times = {e: start_date for e in employees}

for i in range(n_tasks):
    assignee = random.choices(employees, weights=employee_weights.values(), k=1)[0]

    # זמן תחילת המשימה: מרווח כלשהו מהמשימה הקודמת של אותו עובד
    delay_hours = random.randint(1, 5)
    if assignee == 'Eli':  # מגיב לאט במיוחד
        delay_hours += random.randint(3, 5)

    start_time = last_end_times[assignee] + timedelta(hours=delay_hours)

    # משך משימה
    duration_hours = random.randint(1, 6)
    end_time = start_time + timedelta(hours=duration_hours)

    tasks.append({
        "task_id": f"T{i+1:03d}",
        "assigned_to": assignee,
        "start_time": start_time.strftime('%Y-%m-%d %H:%M:%S'),
        "end_time": end_time.strftime('%Y-%m-%d %H:%M:%S')
    })

    last_end_times[assignee] = end_time

# שמירה לקובץ
df = pd.DataFrame(tasks)
df.to_csv("data/team_behavior.csv", index=False)
print("✅ Mock data saved to: data/team_behavior.csv")
