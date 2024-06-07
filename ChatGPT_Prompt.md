Make python challenges for my python script below. the user while tell you the difficulty they want and you will give them 10 python challenges do you understand (y or n)?
<code>
from flask import Flask, request, render_template_string
import ast
import traceback
import yaml
import os

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

# HTML template for the form
html_template = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Python Code Challenge</title>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.63.0/codemirror.min.css">
  <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.63.0/codemirror.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.63.0/mode/python/python.min.js"></script>
  <style>
    body { font-family: Arial, sans-serif; margin: 20px; }
    .container { max-width: 800px; margin: 0 auto; }
    .task { background-color: #f9f9f9; padding: 10px; border-radius: 5px; margin-bottom: 20px; }
    .output { background-color: #f1f1f1; padding: 10px; border-radius: 5px; margin-top: 20px; display: block; }
    textarea { width: 100%; height: 200px; font-family: monospace; }
    .btn { padding: 10px 20px; cursor: pointer; background-color: #007bff; color: #fff; border: none; border-radius: 5px; }
    .btn:hover { background-color: #0056b3; }
    .toast { position: fixed; top: 20px; right: 20px; background-color: #007bff; color: #fff; padding: 10px; border-radius: 5px; display: none; }
    .collapse-btn { cursor: pointer; }
    .collapse-content { display: none; }
    .collapse-content.active { display: block; }
  </style>
  <script>
    document.addEventListener('DOMContentLoaded', function() {
      var collapseBtn = document.querySelector('.collapse-btn');
      var collapseContent = document.querySelector('.collapse-content');
      var outputDiv = document.querySelector('.output');

      collapseBtn.addEventListener('click', function() {
        collapseContent.classList.toggle('active');
      });

      // Reset output when new challenge is loaded
      var selectChallenge = document.querySelector('select[name="challenge"]');
      selectChallenge.addEventListener('change', function() {
        outputDiv.innerHTML = ''; // Reset output
      });

      // Show toast message when all tests are passed
      var output = document.querySelector('.output pre');
      if (output && output.innerText.includes('Congratulations! All test cases passed.')) {
        var toast = document.querySelector('.toast');
        toast.style.display = 'block';
        setTimeout(function() {
          toast.style.display = 'none';
        }, 3000);
      }

      // Initialize CodeMirror
      var codeMirrorTextarea = document.querySelector('textarea[name="code"]');
      var codeMirrorEditor = CodeMirror.fromTextArea(codeMirrorTextarea, {
        mode: 'python',
        theme: 'default',
        lineNumbers: true,
        indentUnit: 2, // Set tab to indent 2 spaces
        autofocus: true
      });
    });
  </script>
</head>
<body>
  <div class="container">
    <h1>Select Difficulty Level and Challenge</h1>
    <form method="GET">
      <select name="difficulty">
        {% for level in challenges.keys() %}
          <option value="{{ level }}" {% if level == difficulty %}selected{% endif %}>{{ level.capitalize() }}</option>
        {% endfor %}
      </select>
      <select name="challenge">
        {% for idx, challenge in enumerate(challenges[difficulty]) %}
          <option value="{{ idx }}" {% if idx == challenge_index %}selected{% endif %}>Challenge {{ idx+1 }}</option>
        {% endfor %}
      </select>
      <button type="submit" class="btn"><i class="fas fa-play"></i> Load Challenge</button>
    </form>
    <div class="task">
      <h2>Task</h2>
      <button class="collapse-btn"><i class="fas fa-chevron-down"></i></button>
      <div class="collapse-content active">
        <p>{{ task }}</p>
      </div>
    </div>
    <form method="POST">
      <input type="hidden" name="difficulty" value="{{ difficulty }}">
      <input type="hidden" name="challenge_index" value="{{ challenge_index }}">
      <textarea name="code" placeholder="Write your Python code here...">{{ code }}</textarea>
      <button type="submit" class="btn"><i class="fas fa-check"></i> Submit</button>
    </form>
    <div class="output">
      <h3>Output</h3>
      <pre>{{ output }}</pre>
    </div>
    <div class="toast">
      <i class="fas fa-check-circle"></i> Congratulations! All test cases passed.
    </div>
  </div>
</body>
</html>

"""

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

@app.route("/", methods=["GET", "POST"])
def index():
    difficulty = request.args.get('difficulty', 'easy')
    challenge_index = int(request.args.get('challenge', 0))
    
    if request.method == "POST":
        difficulty = request.form["difficulty"]
        challenge_index = int(request.form["challenge_index"])
        code = request.form["code"]
    else:
        code = ""
    
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
    
    return render_template_string(html_template, task=task, code=code, output=output, challenges=challenges, difficulty=difficulty, challenge_index=challenge_index, enumerate=enumerate)

if __name__ == "__main__":

    app.run(debug=True)
</code>

<easy_example_response>
- task: "Write a function named 'solve' that takes a single integer input and returns its square."
  test_cases:
    - inputs: [2]
      expected_output: 4
    - inputs: [3]
      expected_output: 9
    - inputs: [4]
      expected_output: 16

- task: "Write a function named 'solve' that takes two integers and returns their sum."
  test_cases:
    - inputs: [1, 2]
      expected_output: 3
    - inputs: [5, 7]
      expected_output: 12
    - inputs: [0, 0]
      expected_output: 0

- task: "Write a function named 'solve' that takes a list of integers and returns the maximum value."
  test_cases:
    - inputs: [[1, 2, 3, 4, 5]]
      expected_output: 5
    - inputs: [[-1, -2, -3, -4]]
      expected_output: -1
    - inputs: [[100, 50, 200, 150]]
      expected_output: 200
</easy_example_response>
