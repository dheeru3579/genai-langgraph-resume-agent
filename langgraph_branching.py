import os
from dotenv import load_dotenv
import google.generativeai as genai
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from pypdf import PdfReader

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

class ResumeState(TypedDict):
    resume_text: str
    skills: list
    missing_skills: list
    roadmap: str
    interview_questions: str
    final_report: str
    approved: bool
    revision_note: str
    revised_report: str
    email_status: str
    user_request: str
    plan: str

def read_resume(state):
    print("\n=== READ RESUME NODE ===")

    reader = PdfReader("data/resume.pdf")
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    state["resume_text"] = text
    return state


def extract_skills(state):
    print("\n=== EXTRACT SKILLS NODE ===")

    prompt = f"""
    Extract only technical skills from this resume.
    Return as a comma-separated list.

    Resume:
    {state["resume_text"]}
    """

    response = model.generate_content(prompt)

    skills = [skill.strip() for skill in response.text.split(",")]

    state["skills"] = skills
    return state


def compare_skills(state):
    print("\n=== COMPARE SKILLS NODE ===")

    required_skills = [
        "Java",
        "Spring Boot",
        "React.js",
        "AWS",
        "Docker",
        "Kubernetes",
        "Kafka",
        "RAG",
        "LangChain",
        "LangGraph",
        "Vector Databases",
        "MCP"
    ]

    resume_skills_text = ", ".join(state["skills"])
    required_skills_text = ", ".join(required_skills)

    prompt = f"""
    Compare resume skills with required skills.

    MCP means Model Context Protocol, not Microsoft Certified Professional.

    Resume Skills:
    {resume_skills_text}

    Required Skills:
    {required_skills_text}

    Return only missing skills as a comma-separated list.
    If nothing is missing, return: None
    """

    response = model.generate_content(prompt)

    if response.text.strip().lower() == "none":
        state["missing_skills"] = []
    else:
        state["missing_skills"] = [
            skill.strip() for skill in response.text.split(",")
        ]

    return state

def planner(state):
    print("\n=== PLANNER NODE ===")

    request = state["user_request"]

    prompt = f"""
    User request:

    {request}

    Decide what action should be taken.

    Possible actions:

    ANALYZE_RESUME
    GENERATE_INTERVIEW_QUESTIONS
    CREATE_ROADMAP

    Return only one action.
    """

    response = model.generate_content(prompt)

    state["plan"] = response.text.strip()

    print("PLAN:", state["plan"])

    return state

def route_plan(state):
    plan = state["plan"]

    if "ANALYZE_RESUME" in plan:
        return "read_resume"

    if "GENERATE_INTERVIEW_QUESTIONS" in plan:
        return "read_resume"

    if "CREATE_ROADMAP" in plan:
        return "read_resume"

    return "read_resume"

def decide_next_step(state):
    print("\n=== DECISION NODE ===")

    if len(state["missing_skills"]) > 0:
        return "generate_roadmap"
    else:
        return "generate_interview_questions"


def generate_roadmap(state):
    print("\n=== GENERATE ROADMAP NODE ===")

    prompt = f"""
    Create a 4-week learning roadmap for these missing skills:

    {state["missing_skills"]}
    """

    response = model.generate_content(prompt)

    state["roadmap"] = response.text
    return state


def generate_interview_questions(state):
    print("\n=== GENERATE INTERVIEW QUESTIONS NODE ===")

    state["interview_questions"] = """
    1. Explain Spring Boot.
    2. Explain React components.
    3. Explain AWS deployment.
    """

    return state

def save_report(state):
    skills = state.get("skills", [])
    missing_skills = state.get("missing_skills", [])

    skills_text = "\n".join(f"- {skill}" for skill in skills)
    missing_text = "\n".join(f"- {skill}" for skill in missing_skills)

    print("\n=== SAVE REPORT NODE ===")

    if len(missing_skills) > 0:
        report = f"""
RESUME SKILLS:
{skills_text}

MISSING SKILLS:
{missing_text}

ROADMAP:
{state["roadmap"]}
"""
    else:
        report = f"""
RESUME SKILLS:
{state["skills"]}

INTERVIEW QUESTIONS:
{state["interview_questions"]}
"""

    with open("langgraph_resume_report.txt", "w", encoding="utf-8") as file:
        file.write(report)

    state["final_report"] = report
    return state

def human_approval(state):
    print("\n=== HUMAN APPROVAL NODE ===")

    print("\nGenerated Report Preview:")
    print(state["final_report"])

    user_input = input("\nDo you approve this report? yes/no: ")

    state["approved"] = user_input.strip().lower() == "yes"

    return state

def approval_decision(state):
    if state["approved"]:
        return "approved"
    else:
        return "rejected"
    
def revision_note(state):
    print("\n=== REVISION NOTE NODE ===")

    note = input("What should be changed in the report?: ")

    state["revision_note"] = note

    with open("revision_note.txt", "w", encoding="utf-8") as file:
        file.write(note)

    return state

def revise_report(state):
    print("\n=== REVISE REPORT NODE ===")

    prompt = f"""
    Revise the report based on the user's revision note.

    Original Report:
    {state["final_report"]}

    Revision Note:
    {state["revision_note"]}
    """

    response = model.generate_content(prompt)

    state["revised_report"] = response.text

    with open("revised_resume_report.txt", "w", encoding="utf-8") as file:
        file.write(state["revised_report"])

    return state

def email_report(state):
    print("\n=== EMAIL REPORT NODE ===")

    report_to_send = state.get("revised_report") or state["final_report"]

    # Mock email tool for now
    print("\nSending email with report...")
    print(report_to_send)

    state["email_status"] = "Email sent successfully."

    return state


builder = StateGraph(ResumeState)

builder.add_node("read_resume", read_resume)
builder.add_node("extract_skills", extract_skills)
builder.add_node("compare_skills", compare_skills)
builder.add_node("generate_roadmap", generate_roadmap)
builder.add_node("generate_interview_questions", generate_interview_questions)
builder.add_node("save_report", save_report)
builder.add_node("human_approval", human_approval)
builder.add_node("revision_note", revision_note)
builder.add_node("revise_report", revise_report)
builder.add_node("email_report", email_report)
builder.add_node("planner", planner)

builder.add_edge(START, "planner")
builder.add_edge("read_resume", "extract_skills")
builder.add_edge("extract_skills", "compare_skills")

builder.add_conditional_edges(
    "compare_skills",
    decide_next_step,
    {
        "generate_roadmap": "generate_roadmap",
        "generate_interview_questions": "generate_interview_questions"
    }
)

builder.add_edge("generate_roadmap", "save_report")
builder.add_edge("generate_interview_questions", "save_report")
builder.add_edge("save_report", "human_approval")

builder.add_conditional_edges(
    "human_approval",
    approval_decision,
    {
        "approved": "email_report",
        "rejected": "revision_note"
    }
)

builder.add_conditional_edges(
    "planner",
    route_plan,
    {
        "read_resume": "read_resume",
        "generate_interview_questions":
            "generate_interview_questions",
        "generate_roadmap":
            "generate_roadmap"
    }
)

builder.add_edge("email_report", END)

builder.add_edge("revision_note", "revise_report")
builder.add_edge("revise_report", END)


graph = builder.compile()

result = graph.invoke(
    {
        "user_request":
        "Analyze my resume"
    }
)

print("\nFINAL STATE:")
print(result)