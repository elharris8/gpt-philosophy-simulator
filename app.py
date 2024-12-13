from flask import Flask, render_template, request
from openai import OpenAI
import os
from dotenv import load_dotenv
import random
import requests
import logging

app = Flask(__name__)


load_dotenv("secrets.env")

client = OpenAI(
    api_key=os.getenv("OPEN_AI_API_KEY"),  
)

def prompt_engineer(input_text):
    """
    Uses OpenAI's GPT-4o Mini API to generate a response in a specific style.

    Args:
        input_text (str): The user's input to prompt engineer.
        style (str): The specific style or type of response to generate.

    Returns:
        str: The model's response.
    """
  

    system_message = f"Respond to the user's queries as if you are a pro-wrestler."

    try:
        system_prompt = {
            "role": "system",
            "content": (
                system_message
            )
        }

        user_prompt = {
            "role": "user",
            "content": input_text
        }

        chat_completion = client.chat.completions.create(
            messages=[system_prompt, user_prompt],  # Include both system and user messages
            model="gpt-4o-mini",
        )

        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {e}"


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        duration = request.form.get('duration')
        distance = request.form.get('distance')
        philosophy1 = request.form.get('philosophy1')
        status1 = request.form.get('status1')
        num_followers1 = request.form.get('followers1') if status1 == "leader" else request.form.get('cofollowers1')
        spread1 = request.form.get('followerspread1') if status1 == "leader" else request.form.get('cofollowerspread1')
        philosophy2 = request.form.get('philosophy2')
        status2 = request.form.get('status2')
        num_followers2 = request.form.get('followers2') if status2 == "leader" else request.form.get('cofollowers2')
        spread2 = request.form.get('followerspread2') if status2 == "leader" else request.form.get('cofollowerspread2')

        simulation_result = prompt_engineer(f"what does {duration} mean?")

        return render_template('simulation.html', simulation_result=simulation_result)
    return render_template('index.html')

@app.route('/simulation', methods=['POST'])
def simulation():
    # Get form data (if needed)
    duration = request.form.get('duration')
    # Process data or prepare battle logic
    return render_template('simulation.html')

@app.route('/results', methods=['GET'])
def results():
    # Get form data passed from index.html
    user_philosophy = request.args.get('user_philosophy')  # Example: 'xunzi', 'shang', 'laozi'
    opponent_philosophy = request.args.get('opponent_philosophy')  # Example: 'xunzi', 'shang', 'laozi'
    duration = request.args.get('duration')  # 'short', 'medium', or 'long'
    distance = request.args.get('distance')  # Example: 'short', 'medium', 'long'

    # Construct the context dynamically
    context = f"""
    User Philosophy: {user_philosophy}
    Opponent Philosophy: {opponent_philosophy}
    Duration: {duration}
    Distance: {distance}
    """

    # ChatGPT prompt based on your reference
    prompt = f"""
    Based on the simulation's parameters provided below, determine the winner of the battle and provide a 5-10 sentence explanation as to why this philosophy triumphed over the other in this situation:
    {context}
    """

    # Use the shared chat URL (replace with the actual API key and endpoint if available)
    headers = {
        "Authorization": f"Bearer sk-proj-cu82kEi7dPbpROFHR6wBwi|24BJa2uwYIMSST1xF77k2R50HIFDj-4YmPbt4wKaZTJKe3SD7JT3BIbkFJ_NYYg4fnNbStpZ_8pf_fDQzTKD-yLw-86JOi5t2zct1 HiYH1 iheflFuJpgpy517535pzQpskA",
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
        response = requests.post("https://api.openai.com/v1/chat/completions", json=data, headers=headers)
        response.raise_for_status()  # Raise an error for bad HTTP responses (4xx or 5xx)

        result = response.json()
        explanation = result['choices'][0]['message']['content'].strip()
        winner = explanation.split('.')[0]
    except requests.exceptions.RequestException as e:
        logging.error(f"API Request failed: {e}")
        explanation = "An error occurred while generating the explanation. Please try again later."
        winner = "Unknown"

    # Render the results.html page
    return render_template('results.html', winner=winner, explanation=explanation)


@app.route('/explanation')
def explanation():
    return render_template('explanation.html')