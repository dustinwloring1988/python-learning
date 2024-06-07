from flask import Flask, request
from utils.challenges import load_challenges, select_random_challenge
from utils.execute import execute_user_code
from utils.render import render_template

app = Flask(__name__)
challenges = load_challenges()
with open("templates/template.html", "r") as file:
    html_template = file.read()

@app.route("/", methods=["GET", "POST"])
def index():
    difficulty = request.args.get('difficulty')
    challenge_index = int(request.args.get('challenge', 0))
    
    if request.method == "POST":
        difficulty = request.form["difficulty"]
        challenge_index = int(request.form["challenge_index"])
        code = request.form["code"]
    else:
        code = ""

    task = ""  # Initialize task to empty string
    
    # Load a random challenge if difficulty is selected
    if difficulty:
        selected_challenge = select_random_challenge(challenges, difficulty)
        task = selected_challenge['task']
        challenge_index = challenges[difficulty].index(selected_challenge)
    
    test_cases = []  # Initialize test_cases to empty list

    output = ""
    if request.method == "POST":
        output = execute_user_code(code, test_cases)  # Pass test cases here
    
    return render_template(html_template, task=task, code=code, output=output, challenges=challenges, difficulty=difficulty, challenge_index=challenge_index)

if __name__ == "__main__":
    app.run(debug=True)
