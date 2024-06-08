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
    """
    Handles the '/' route for both GET and POST requests.
    
    Retrieves the 'difficulty' and 'challenge' parameters from the request arguments.
    If the request method is POST, it retrieves the 'difficulty', 'challenge_index', and 'code' parameters from the request form.
    If the request method is GET, it initializes the 'code' parameter to an empty string.
    
    If a 'difficulty' parameter is provided, it loads a random challenge from the 'challenges' dictionary based on the difficulty.
    It retrieves the 'task' from the selected challenge and sets the 'challenge_index' to the index of the selected challenge in the corresponding difficulty list.
    
    Initializes the 'test_cases' list to an empty list.
    
    If the request method is POST, it executes the user code using the 'execute_user_code' function and stores the output in the 'output' variable.
    
    Renders the 'html_template' template with the 'task', 'code', 'output', 'challenges', 'difficulty', and 'challenge_index' variables.
    
    Returns:
        The rendered template.
    """
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
