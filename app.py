from flask import Flask, render_template, request, session, flash, redirect
import openai
import os
import dotenv
import random
import requests
import logging
from flask_session import Session

# configure application
app = Flask(__name__)
app.secret_key = "gened1091_final_project"

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
dotenv.load_dotenv("secrets.env")

openai.api_key = os.getenv("OPENAI_API_KEY").strip()

# client = openai.OpenAI(
#     api_key=os.getenv("OPEN_AI_API_KEY"),  
# )

# def prompt_engineer(input_text):
#     """
#     Uses OpenAI's GPT-4o Mini API to generate a response in a specific style.

#     Args:
#         input_text (str): The user's input to prompt engineer.
#         style (str): The specific style or type of response to generate.

#     Returns:
#         str: The model's response.
#     """
  

#     system_message = f"Respond to the user's queries as if you are a pro-wrestler."

#     try:
#         system_prompt = {
#             "role": "system",
#             "content": (
#                 system_message
#             )
#         }

#         user_prompt = {
#             "role": "user",
#             "content": input_text
#         }

#         chat_completion = client.chat.completions.create(
#             messages=[system_prompt, user_prompt],  # Include both system and user messages
#             model="gpt-4o-mini",
#         )

#         return chat_completion.choices[0].message.content
#     except Exception as e:
#         return f"An error occurred: {e}"


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

        return render_template('simulation.html')
    
    else:
        return render_template('index.html')

@app.route('/simulation', methods=['POST'])
def simulation():
    return render_template('simulation.html')

@app.route('/results', methods=['GET', 'POST'])
def results():        
    # Retrieve values from session["data"]
    data = session["data"]

    context = f"""
    Duration: {data['duration']}
    Distance: {data['distance']}
    User Philosophy: {data['phil1']}
    User Status: {data['status1']}
    User Followers: {data['follow1']}
    User Spread: {data['spread1']}
    Opponent Philosophy: {data['phil2']}
    Opponent Status: {data['status2']}
    Opponent Followers: {data['follow2']}
    Opponent Spread: {data['spread2']}
    """

    # Construct the prompt
    prompt = f"""
    Based on the simulation's parameters provided below, determine the winner of the battle and provide a 5-10 sentence explanation as to why this philosophy triumphed over the other in this situation:
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
            {"role": "system", "content": "You are an expert in ancient Chinese philosophy."},
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

        # Extract the winner from the explanation
        winner = explanation.split('.')[0]  # Assumes the first sentence indicates the winner
    except requests.exceptions.RequestException as e:
        logging.error(f"API Request failed: {e}")
        explanation = "An error occurred while generating the explanation. Please try again later."
        winner = "Unknown"

    # Render the results.html page
    return render_template('results.html', winner=winner, explanation=explanation)

@app.route('/explanation')
def explanation():
    return render_template('explanation.html')