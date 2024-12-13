from flask import Flask, render_template, request, session, flash, redirect
import openai
import os
import dotenv
import random
import requests
import logging
from flask_session import Session
import re

from helpers import extract_pdf_text

# configure application
app = Flask(__name__)
app.secret_key = "gened1091_final_project"

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
dotenv.load_dotenv("secrets.env")

openai.api_key = os.getenv("OPENAI_API_KEY").strip()

gpt_feeder_input = extract_pdf_text("GPT_input.pdf")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        duration = request.form.get('duration')
        distance = request.form.get('distance')
        philosophy1 = request.form.get('philosophy1')
        status1 = request.form.get('status1')
        num_followers1 = request.form.get('followers1')
        spread1 = request.form.get('spread1')
        philosophy2 = request.form.get('philosophy2')
        status2 = request.form.get('status2')
        num_followers2 = request.form.get('followers2')
        spread2 = request.form.get('spread2')

        session["data"] = {
            "duration": duration,
            "distance": distance,
            "phil1": philosophy1,
            "status1": status1,
            "follow1": num_followers1,
            "spread1": spread1,
            "phil2": philosophy2,
            "status2": status2,
            "follow2": num_followers2,
            "spread2": spread2
        } # TODO: don't forget to clear session at some point

        print(session["data"].values())

        if not all(session["data"].values()):
            flash("One or parameters missing. Please fill in all boxes.")
            return redirect("/")

        return redirect("/simulation")
    
    else:
        return render_template('index.html')

@app.route('/simulation', methods=['GET', 'POST'])
def simulation():
    # Map durations to delays
    duration_mapping = {
        "short": 500,  # 3 seconds
        "med": 7000,  # 7 seconds
        "long": 15000  # 15 seconds
    }

    # Get duration from session data or default to "short"
    duration_key = session.get("data", {}).get("duration", "short")
    duration = duration_mapping.get(duration_key, 3000)

    print(f"Duration key: {duration_key}, Duration (ms): {duration}")

    return render_template('simulation.html', duration=duration)

@app.route('/results', methods=['GET', 'POST'])
def results():        
    context = f"""
    Duration: {session["data"]['duration']}
    Distance: {session["data"]['distance']}
    User Philosophy: {session["data"]['phil1']}
    User Status: {session["data"]['status1']}
    User Followers: {session["data"]['follow1']}
    User Spread: {session["data"]['spread1']}
    Opponent Philosophy: {session["data"]['phil2']}
    Opponent Status: {session["data"]['status2']}
    Opponent Followers: {session["data"]['follow2']}
    Opponent Spread: {session["data"]['spread2']}
    """

    # Construct the prompt
    prompt = f"""
    Based specifically on the parameters provided in the information below, determine the winner of the battle and provide a 5-10 sentence explanation as to why this philosophy triumphed over the other in this situation. Relate your answer directly to the parameters and why this combination of parameters led you to your chosen outcome. Your initial answer should just be the name of the winning philosopher. Then in the paragraph you give your explanation.
    {context}
    """

    # OpenAI API key and endpoint
    headers = {
        "Authorization": f"Bearer {openai.api_key}",
        "Content-Type": "application/json",
    }

    data = {
        "model": "gpt-4",
        "messages": [
            {"role": "system", "content": gpt_feeder_input},
            {"role": "user", "content": prompt},
        ],
    }

    try:
        # Make the API request
        response = requests.post("https://api.openai.com/v1/chat/completions", json=data, headers=headers)
        response.raise_for_status()  # Raise an error for bad HTTP responses (4xx or 5xx)

        # Parse the response
        result = response.json()
        explanation = result['choices'][0]['message']['content'].strip()

        # Extract the winner using a regular expression
        if explanation[:2] == "Lo":
            winner = "Lord Shang"
        elif explanation[:2] == "La":
            winner = "Laozi"
        elif explanation[:2] == "Xu":
            winner = "Xunzi"

        # update explanation
        explanation = explanation.replace(winner, "", 1).strip()

    except:
        explanation = "An error occurred while generating the explanation. Please try again."
        winner = "Unknown"

    return render_template('results.html', winner=winner, explanation=explanation)

# TODO: this is now incorporated within the results.html page. but we could have some extra tabs including idk what
@app.route('/explanation')
def explanation():
    return render_template('explanation.html')