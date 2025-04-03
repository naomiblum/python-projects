# 🧠 FlowSense – Behavioral Pattern Detection for Teams

> “Tasks are getting done, but something still feels off in the team.”  
This is the insight that inspired **FlowSense** — a tool designed to reveal what task trackers don't.

FlowSense is a Python-based analytics system that detects hidden dysfunctions in team collaboration:  
task flow issues, bottlenecks, unresponsive contributors, and behavioral anomalies — all through real data.

---

## 📖 Story Behind the Project

I’ve always been fascinated by how **teams behave as systems**, not just as collections of people.

As an aspiring **Optimization Architect**, I wanted to go beyond tools like Jira and Trello.  
I wanted a tool that sees **how people actually interact**, where flow gets disrupted, and what patterns silently emerge.

So I built FlowSense.

It bridges:
- 🧠 Behavioral data  
- 🧮 Algorithmic thinking  
- 🔍 Systems analysis  
into one practical tool.

---

## 🚀 What FlowSense Does

✅ Loads team activity data (from CSV or logs)  
✅ Computes **behavioral KPIs** for every person and task  
✅ Finds **dysfunctional interaction patterns**  
✅ Uses clustering to reveal types of contributors  
✅ Generates clear visual reports and anomaly graphs

---

## 💻 Technologies

- **Python 3.10+**
- `pandas` – data handling
- `matplotlib`, `seaborn` – data visualization
- `scikit-learn` – clustering (optional)
- `collections`, `datetime`, and Python core libraries

---

## 📦 Project Structure

    FlowSense/
    ├── main.py                      # Entry point
    ├── data/
    │   └── team_behavior.csv        # Input data
    ├── analysis/
    │   └── behavior_patterns.py     # Metrics & logic
    ├── plots/
    │   └── *.png                    # Generated graphs
    ├── README.md
    ├── theory.md                    # Mathematical / conceptual notes
    └── requirements.txt

---

## 🧪 How to Run

1. Clone this repository  
2. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Run the analysis:

    ```bash
    python main.py
    ```

---

## 📊 KPIs Computed

| Metric                | Description                                  |
|-----------------------|----------------------------------------------|
| Avg. Response Time    | Delay between task assignment and response   |
| Task Lag              | Time between task start and completion       |
| Load Ratio            | Tasks assigned vs completed per person       |
| Interaction Frequency | How often teammates collaborate or stall     |

---

## 🧠 Learning Objectives

This project helps practice:

- Real-world data manipulation (`pandas`)
- KPI design for human behavior modeling
- Clustering and pattern detection
- Visual storytelling with data
- Writing clean, modular, scalable Python code
- Thinking like a systems analyst

---

## 🔭 Future Features

- Streamlit-based dashboard  
- Jira/Trello/Monday.com integrations  
- Real-time anomaly detection  
- Predictive modeling for team risks

