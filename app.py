from flask import Flask, render_template, request

app = Flask(__name__)

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

        
        print(f'S: {duration}')
        print(f'User Player: {distance}')
        print(f'Opposing Player: {philosophy1}')
        print(f's: {status1}')
        print(num_followers1)
        print(spread1)

        print(f'Opposing Player: {philosophy2}')
        print(f's: {status2}')
        print(num_followers2)
        print(spread2)
        
        # return render_template('index.html', simulation=simulation, user_player=user_player, opposing_player=opposing_player)
        return render_template('simulation.html',duration=duration,distance=distance,philosophy1=philosophy1,
                               status1=status1,num_followers1=num_followers1,spread1=spread1,philosophy2=philosophy2,
                               status2=status2,num_followers2=num_followers2,spread2=spread2,)
    return render_template('index.html')

@app.route('/explanation')
def explanation():
    return render_template('explanation.html')