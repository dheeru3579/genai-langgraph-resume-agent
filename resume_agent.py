import os
from dotenv import load_dotenv
from tools import read_pdf, save_report, read_text_file
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")


def extract_resume_skills(resume_text):
    prompt = f"""
    Extract only the technical skills from this resume.
    Return them as a comma-separated list.

    Resume:
    {resume_text}
    """

    response = model.generate_content(prompt)
    return response.text

def extract_jd_skills(job_description):
    prompt = f"""
    Extract only the required technical skills from this job description.
    Return them as a comma-separated list.

    Job Description:
    {job_description}
    """

    response = model.generate_content(prompt)
    return response.text

def compare_skills(resume_skills, jd_skills):
    prompt = f"""
    Compare the resume skills and job description skills.

    Resume Skills:
    {resume_skills}

    Job Description Skills:
    {jd_skills}

    Return:
    1. Matching Skills
    2. Missing Skills
    3. Skills to Improve
    """

    response = model.generate_content(prompt)
    return response.text

def generate_learning_roadmap(skill_gap_analysis):
    prompt = f"""
    Based on this skill gap analysis, create a 4-week learning roadmap.

    Include:
    - Weekly topics
    - Hands-on tasks
    - Mini project ideas
    - Interview preparation points

    Skill Gap Analysis:
    {skill_gap_analysis}
    """

    response = model.generate_content(prompt)
    return response.text

resume_text = read_pdf("data/sample.pdf")
resume_skills = extract_resume_skills(resume_text)

job_description = read_text_file("data/job_description.txt")

jd_skills = extract_jd_skills(job_description)

print("\nResume Skills:")
print(resume_skills)

print("\nJob Description Skills:")
print(jd_skills)

analysis = compare_skills(resume_skills, jd_skills)

print("\nSkill Gap Analysis:")
print(analysis)

roadmap = generate_learning_roadmap(analysis)

print("\n4-Week Learning Roadmap:")
print(roadmap)

final_report = f"""
RESUME SKILLS:
{resume_skills}

JOB DESCRIPTION SKILLS:
{jd_skills}

SKILL GAP ANALYSIS:
{analysis}

4-WEEK LEARNING ROADMAP:
{roadmap}
"""

save_message = save_report(final_report)

print("\nFinal Report:")
print(final_report)

print("\n" + save_message)