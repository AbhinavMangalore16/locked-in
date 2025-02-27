import streamlit as st
import json
import requests
from google import genai  # Google Gemini API


def get_career_roadmap(user_input):
    client = genai.Client(api_key="AIzaSyDy3uwnNR6bgQKm5mf43mf5RLN4ZG8ehKg")  
    prompt = f"""
    You are an AI career assistant that helps users upskill effectively. Based on the given user profile and goals, generate a structured JSON response that includes:

    1️⃣ **Skills to Learn** – The key skills they should acquire.
    2️⃣ **Recommended Courses** – Specific courses from relevant platforms.
    3️⃣ **Hours per Week** – Suggested weekly time commitment.
    4️⃣ **Step-by-Step Roadmap** – A sequence of learning steps.

    **User Profile:** {user_input}

    **Output Format (JSON):**
    {{
    "career_level": "Beginner | Intermediate | Advanced",
    "skills_to_learn": [
        {{"name": "Skill 1", "category": "Technical"}},
        {{"name": "Skill 2", "category": "Soft Skill"}},
        {{"name": "Skill 3", "category": "Domain-specific"}}
    ],
    "recommended_courses": [
        {{
            "title": "Course 1",
            "platform": "Udemy",
            "url": "https://udemy.com/...",
            "difficulty": "Beginner"
        }},
        {{
            "title": "Course 2",
            "platform": "Coursera",
            "url": "https://coursera.org/...",
            "difficulty": "Advanced"
        }}
    ],
    "learning_resources": [
        {{"type": "Book", "title": "Book Name", "author": "Author Name"}},
        {{"type": "YouTube Channel", "name": "Channel Name", "url": "https://youtube.com/..."}},
        {{"type": "Practice Platform", "name": "LeetCode", "url": "https://leetcode.com"}}
    ],
    "hours_per_week": 10,
    "roadmap": [
        {{
            "week": 1,
            "focus": "Fundamentals",
            "tasks": ["Complete Course 1", "Read Book 1"],
            "project": "Set up development environment"
        }},
        {{
            "week": 2,
            "focus": "Hands-on Learning",
            "tasks": ["Solve 10 LeetCode problems", "Watch YouTube tutorials"],
            "project": "Build a simple project using Skill 1"
        }},
        {{
            "week": 3,
            "focus": "Advanced Concepts",
            "tasks": ["Complete Course 2", "Attend a workshop"],
            "project": "Contribute to an open-source project"
        }}
    ],
    "career_tips": [
        "Network with professionals on LinkedIn",
        "Build a strong portfolio with projects",
        "Stay updated with industry trends"
    ]
    }}

    Ensure the response follows this structure strictly.
    """
    
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=prompt,
    )
    print(type(response))
    print(1)
    print(response)
    print(2)
    print(response.data)

    # Display the raw response text in a Streamlit text area
    st.text_area("Raw Response from API", response.text, height=200)

    try:
        return json.loads(response.text) if response.text else {}
    except json.JSONDecodeError:
        st.error("❌ Unable to parse JSON. The response might not be properly formatted.")
        return {}

st.title("📈 Career Assistant")
st.write("Answer the questions below to get a personalized upskilling roadmap.")

# Basic Info
name = st.text_input("Full Name")
email = st.text_input("Email Address")
age_group = st.selectbox("Age Group", ["18-24", "25-34", "35-44", "45+"])
current_role = st.text_input("Current Role/Title")
industry = st.selectbox("Industry", ["Software", "Finance", "Healthcare", "Other"])
experience = st.slider("Years of Experience", 0, 20, 1)

# Career Goals
career_goal = st.multiselect("What is your primary career goal?", [
    "Get a promotion", "Switch careers", "Become a freelancer", "Master advanced skills", "Prepare for job interviews"
])
career_switch = st.radio("Are you considering a career switch?", ["No", "Yes", "I'm unsure"])
if career_switch == "Yes":
    new_career = st.text_input("Which career do you want to switch to?")

# Skills & Learning Preferences
skills = st.multiselect("Which skills do you already have?", ["Python", "JavaScript", "SQL", "Machine Learning", "Cloud Computing", "Soft Skills"])
learning_style = st.multiselect("Preferred learning style?", ["Video tutorials", "Books", "Coding platforms", "Hands-on projects"])
time_commitment = st.slider("How many hours per week can you dedicate to learning?", 1, 20, 5)
budget = st.selectbox("Budget for learning?", ["Free only", "<$50 per course", "$50-$200", "No budget constraints"])

# Submit & Generate Roadmap
if st.button("Generate My Roadmap"):
    user_input = {
        "name": name,
        "email": email,
        "age_group": age_group,
        "current_role": current_role,
        "industry": industry,
        "experience": experience,
        "career_goal": career_goal,
        "career_switch": career_switch if career_switch != "Yes" else new_career,
        "skills": skills,
        "learning_style": learning_style,
        "time_commitment": time_commitment,
        "budget": budget
    }
    
    roadmap = get_career_roadmap(user_input)
    
    if roadmap:
        st.success("🎯 Your Personalized Upskilling Roadmap")
        st.json(roadmap)  
    else:
        st.error("❌ Unable to generate roadmap. Try again!")
