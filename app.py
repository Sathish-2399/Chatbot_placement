from flask import Flask, render_template, request, jsonify
from datetime import datetime
import requests, os

app = Flask(__name__)

API_KEY = os.getenv("OPENROUTER_API_KEY")  # optional

conversation_history = [
    {
        "role": "system",
        "content": "You are a Placement Chatbot that helps students with placement preparation, interview questions, resume tips, companies, aptitude, and career guidance."
    }
]

def time_now():
    return datetime.now().strftime("%H:%M")

def fallback_response(msg):
    msg = msg.lower()

    if "prepare for placements" in msg or "placement" in msg:
        return (
            "To prepare for placements, focus on aptitude, basic programming, "
            "core subjects like DBMS and OS, and improve your communication skills."
        )

    if "resume" in msg:
        return (
            "Keep your resume simple and professional. Limit it to one page, "
            "highlight your projects, technical skills, internships, and measurable achievements."
        )

    if "project" in msg:
        return (
            "Add projects that demonstrate real-world problem solving, such as "
            "web applications, data analysis projects, machine learning models, or system-based projects."
        )

    if "hr interview" in msg:
        return (
            "For HR interviews, prepare self-introduction, strengths and weaknesses, "
            "career goals, company knowledge, and practice confident communication."
        )

    if "technical skills" in msg:
        return (
            "Important technical skills include programming basics, SQL, data structures, "
            "operating systems, DBMS, and problem-solving ability."
        )

    if "company" in msg or "hiring" in msg:
        return (
            "Popular companies hiring freshers include TCS, Infosys, Wipro, Accenture, "
            "Cognizant, Zoho, and Capgemini."
        )

    if "communication" in msg:
        return (
            "Improve communication skills by practicing speaking daily, attending mock interviews, "
            "watching English interviews, and participating in group discussions."
        )

    if "aptitude" in msg:
        return (
            "To crack aptitude tests, practice quantitative aptitude, logical reasoning, "
            "and verbal ability regularly using mock tests."
        )

    if "programming" in msg:
        return (
            "Start with C, Java, or Python. Learn basic problem-solving, data structures, "
            "and write clean, logical code."
        )

    if "interview tips" in msg:
        return (
            "Be confident, revise fundamentals, know your resume thoroughly, "
            "maintain eye contact, and communicate clearly during interviews."
        )

    if "hello" in msg or "hi" in msg:
        return "Hello! I am your Placement Chatbot. How can I assist you today?"

    return "Please ask a clear placement-related question so I can help you better."


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/send_message", methods=["POST"])
def send_message():
    user_msg = request.json.get("message")

    conversation_history = [
    {
        "role": "system",
        "content": (
            "You are a Placement Chatbot. Always respond in clear, professional English. "
            "You help students with placement preparation, resumes, interview questions, "
            "technical skills, aptitude, and career guidance."
        )
    }
]


    try:
        if API_KEY:
            res = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "deepseek/deepseek-chat",
                    "messages": conversation_history,
                    "temperature": 0.7
                }
            )
            reply = res.json()["choices"][0]["message"]["content"]
        else:
            reply = fallback_response(user_msg)

    except:
        reply = fallback_response(user_msg)

    conversation_history.append({
        "role": "assistant",
        "content": reply
    })

    return jsonify({
        "response": reply,
        "time": time_now()
    })

if __name__ == "__main__":
    app.run(debug=True)
