from typing import TypedDict
from langgraph.graph import StateGraph, START, END


class ResumeState(TypedDict):
    resume_text: str
    skills: list
    report: str


def read_resume(state):
    print("\n=== READ RESUME NODE ===")

    state["resume_text"] = """
    Java Spring Boot React AWS Docker Kafka
    """

    return state


def extract_skills(state):
    print("\n=== EXTRACT SKILLS NODE ===")

    resume = state["resume_text"]

    skills = resume.split()

    state["skills"] = skills

    return state


def generate_report(state):
    print("\n=== GENERATE REPORT NODE ===")

    skills = state["skills"]

    state["report"] = (
        f"Candidate has skills: {', '.join(skills)}"
    )

    return state


builder = StateGraph(ResumeState)

builder.add_node("read_resume", read_resume)
builder.add_node("extract_skills", extract_skills)
builder.add_node("generate_report", generate_report)

builder.add_edge(START, "read_resume")
builder.add_edge("read_resume", "extract_skills")
builder.add_edge("extract_skills", "generate_report")
builder.add_edge("generate_report", END)

graph = builder.compile()

result = graph.invoke({})

print("\nFINAL STATE:")
print(result)