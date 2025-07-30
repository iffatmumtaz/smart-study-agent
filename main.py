import datetime
import json
from typing import List, Dict

# Scheduler agent: Distributes study time among topics
def schedular_agent(topics: List[str], deadline: str) -> List[Dict]:
    try:
        deadline_date = datetime.datetime.strptime(deadline, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Invalid date format. Use YYYY-MM-DD.")
    
    today = datetime.date.today()
    days_remaining = (deadline_date - today).days

    if days_remaining <= 0:
        raise ValueError("Deadline must be a future date.")

    study_days = max(1, days_remaining // len(topics))
    study_plan = []
    current_day = today

    for topic in topics:
        end_day = current_day + datetime.timedelta(days=study_days - 1)
        study_plan.append({
            "topic": topic,
            "start_date": str(current_day),
            "end_date": str(end_day)
        })
        current_day = end_day + datetime.timedelta(days=1)

    return study_plan

# Research agent: Provides dummy research links for a topic
def research_agent(topic: str) -> List[str]:
    return [
        f"What is {topic}? - https://en.wikipedia.org/wiki/{topic.replace(' ', '_')}",
        f"YouTube Intro to {topic} - https://www.youtube.com/results?search_query=introduction+to+{topic.replace(' ', '+')}",
        f"Benefits and Risks of {topic} - https://medium.com/tag/{topic.replace(' ', '-')}",
        f"Research Paper on {topic} - https://scholar.google.com/scholar?q={topic.replace(' ', '+')}"
    ]

# Summarizer agent: Converts list of links into a summary string (dummy for now)
def summerizer_agent(snippets: List[str]) -> str:
    return " | ".join(snippets)

# Main function to run the assistant
def run_study_assistant():
    topics_input = input("Enter your topics separated by commas: ")
    deadline = input("Enter your study deadline (YYYY-MM-DD): ")
    topics = [t.strip() for t in topics_input.split(",") if t.strip()]

    if not topics:
        print("No valid topics entered.")
        return

    try:
        study_plan = schedular_agent(topics, deadline)
    except Exception as e:
        print("Error:", e)
        return

    full_output = []

    for item in study_plan:
        topic = item["topic"]
        print(f"\n🔍 Researching: {topic}")
        research = research_agent(topic)
        summary = summerizer_agent(research)

        item_output = {
            "topic": topic,
            "start_date": item["start_date"],
            "end_date": item["end_date"],
            "summary": summary
        }

        full_output.append(item_output)
        print(f"\n📄 Summary for {topic}:\n{summary}")

    with open("study_assistant_output.json", "w") as f:
        json.dump(full_output, f, indent=4)

    print("\n✅ Study plan and summaries saved in 'study_assistant_output.json'.")

# Run the assistant if this is the main script
if __name__ == "__main__":
    run_study_assistant()
