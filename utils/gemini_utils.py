import json
import requests
from google import genai

def parse_to_json(data: str):
    cleaned_data = data[data.index("{") : data.rindex("}") + 1]
    return json.loads(cleaned_data)

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

    try:
        return parse_to_json(response.text)
    
    except json.JSONDecodeError:
        print("❌ Unable to parse JSON. The response might not be properly formatted.")
        return {}
    

# user_input = {
#         "name": 'name',
#         "email": 'email',
#         "age_group": '20+',
#         "current_role": 'computer engineer',
#         "industry": 'software',
#         "experience": '1 year',
#         "career_goal": 'data scientist',
#         "career_switch": 'yes',
#         "skills": 'None',
#         "learning_style": 'basic',
#         "time_commitment": '8 hours a day',
#         "budget": '1000'
# }

# print(get_career_roadmap(user_input))