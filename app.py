from flask import Flask, request, render_template
import ast
import traceback
import yaml
import os
import datetime

app = Flask(__name__)

# Folder containing challenge YAML files
CHALLENGES_FOLDER = 'challenges'

# Map difficulty levels to their respective YAML files
DIFFICULTY_FILES = {
    'easy': 'easy.yaml',
    'medium': 'medium.yaml',
    'hard': 'hard.yaml'
}

# Load challenges from YAML files
challenges = {}

for difficulty, filename in DIFFICULTY_FILES.items():
    filepath = os.path.join(CHALLENGES_FOLDER, filename)
    with open(filepath, 'r') as file:
        challenges[difficulty] = yaml.safe_load(file)

@app.route("/", methods=["GET", "POST"])
def index():
    difficulty = request.args.get('difficulty', 'easy')
    challenge_index = int(request.args.get('challenge', 0))
    
    code = ""  # Initialize the code variable
    
    if request.method == "POST":
        difficulty = request.form["difficulty"]
        challenge_index = int(request.form["challenge_index"])
        code = request.form["code"]
    
    selected_challenge = challenges[difficulty][challenge_index]
    task = selected_challenge['task']
    test_cases = selected_challenge['test_cases']
  
    output = ""
  
    if request.method == "POST":
        try:
            parsed_code = ast.parse(code)
        except SyntaxError as e:
            output = f"Syntax Error: {e}"
        else:
            all_tests_passed = True
            results = []
            for i, test_case in enumerate(test_cases):
                inputs = test_case['inputs']
                expected_output = test_case['expected_output']
                result = execute_user_code(code, inputs)
                if result == expected_output:
                    results.append(f"Test case {i+1} passed.")
                else:
                    results.append(f"Test case {i+1} failed. Expected {expected_output} but got {result}.")
                    all_tests_passed = False
            if all_tests_passed:
                results.append("Congratulations! All test cases passed.")
            else:
                results.append("Some test cases failed. Try again.")
            output = "\n".join(results)
    
    return render_template('index.html', task=task, code=code, output=output, challenges=challenges, difficulty=difficulty, challenge_index=challenge_index, enumerate=enumerate)

def execute_user_code(user_code, input_data):
    local_vars = {}
    try:
        exec(user_code, {}, local_vars)
        if 'solve' in local_vars:
            result = local_vars['solve'](*input_data)
            return result
        else:
            return "Error: Your code must define a function named 'solve'."
    except Exception as e:
        return f"Error executing your code: {e}\n{traceback.format_exc()}"

if __name__ == "__main__":
    app.run(debug=True)
