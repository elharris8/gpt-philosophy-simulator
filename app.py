from flask import Flask, render_template, request
from openai import OpenAI
import os
from dotenv import load_dotenv


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

@app.route('/explanation')
def explanation():
    return render_template('explanation.html')