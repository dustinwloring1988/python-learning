import requests
import yaml
import json

url = 'http://localhost:11434/api/generate'

level = input("Enter the level of challenges you want (easy, medium, hard): ").lower()

prompt_template = "You run a Python challenge website and want to add more {}-level challenges to your platform. You need diverse and challenging problems to engage your users. Show the output as a yaml file, all responses will have a solve function that the user has to build as that is what we check. Generate 10 {}-level Python challenges, each with a task description and multiple test cases. <example> - task: 'Write a function named \'solve\' that takes a list of integers and returns the maximum difference between any two elements in the list.' test_cases: - inputs: [[1, 2, 3, 4, 5]] expected_output: 4 - inputs: [[10, 20, 30, 40, 50]] expected_output: 40 - task: 'Write a function named \'solve\' that takes a string and returns True if it is a pangram (contains every letter of the alphabet at least once), False otherwise.' test_cases: - inputs: ['The quick brown fox jumps over the lazy dog'] expected_output: True - inputs: ['Hello, world!'] expected_output: False - task: 'Write a function named \'solve\' that takes a list of integers and returns True if there is a subsequence of the list that sums to zero, False otherwise.' test_cases: - inputs: [[4, 2, -3, 1, 6]] expected_output: True - inputs: [[1, 2, 3, 4, 5]] expected_output: False </example>"

if level not in ['easy', 'medium', 'hard']:
    print("Invalid level. Please choose from easy, medium, or hard.")
    exit()

data = {
    "model": "llama3",
    "prompt": prompt_template.format(level, level),
    "format": "json",
    "stream": False
}

response = requests.post(url, json=data)
response_data = response.json()

print("Response data:", response_data)

if response.status_code == 200 and response_data.get('done'):
    response_text = response_data['response']
    print("Response text before cleanup:", response_text)
    # Remove excessive whitespace and newlines
    response_text = ' '.join(response_text.split())
    print("Response text after cleanup:", response_text)
    
    try:
        response_dict = json.loads(response_text)
        print("Response dictionary:", response_dict)
        
        challenges_yaml = []
        for task_data in response_dict.get('tasks', []):
            task_description = task_data.get('task')
            test_cases = task_data.get('test_cases', [])
            task = {
                "task": task_description,
                "test_cases": test_cases
            }
            challenges_yaml.append(task)

        with open('test.yaml', 'w') as file:
            yaml.dump(challenges_yaml, file, default_flow_style=False)
        print("File test.yaml saved successfully.")
    
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
    except KeyError as e:
        print("KeyError:", e)
else:
    print("Error:", response.status_code)
