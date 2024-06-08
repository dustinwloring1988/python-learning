import requests
import json
import yaml
import os
import psycopg2

def save_to_yaml(challenge_data):
    with open("challenges.yaml", "a", encoding="utf-8") as file:
        yaml.dump(challenge_data, file, allow_unicode=True)

def save_to_database(challenge_data):
    # Connect to PostgreSQL
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST")
    )

    # Create a cursor
    cur = conn.cursor()

    # Insert challenges into the database
    for challenge in challenge_data:
        task = challenge.get("task", "")
        test_cases = json.dumps(challenge.get("test_cases", []))
        cur.execute("INSERT INTO challenge (task, test_cases) VALUES (%s, %s)",
                    (task, test_cases))

    # Commit the transaction
    conn.commit()

    # Close the cursor and connection
    cur.close()
    conn.close()

def main():
    # Define the request payload
    payload = {
        "model": "llama3",
        "prompt": "You run a Python challenge website and want to add more hard-level challenges to your platform. You need diverse and challenging problems to engage your users. Show the output as a yaml file, all responses will have a solve function that the user has to build as that is what we check. Generate 10 hard-level Python challenges, each with a task description and multiple test cases. <example> - task: 'Write a function named \'solve\' that takes a single integer input and returns its square.' test_cases: - inputs: [2] expected_output: 4 - inputs: [3] expected_output: 9 - inputs: [4] expected_output: 16 - task: 'Write a function named \'solve\' that takes two integers and returns their sum.' test_cases: - inputs: [1, 2] expected_output: 3 - inputs: [5, 7] expected_output: 12 - inputs: [0, 0] expected_output: 0 - task: 'Write a function named \'solve\' that takes a list of integers and returns the maximum value.' test_cases: - inputs: [[1, 2, 3, 4, 5]] expected_output: 5 - inputs: [[-1, -2, -3, -4]] expected_output: -1 - inputs: [[100, 50, 200, 150]] expected_output: 200 </example>",
        "format": "json",
        "stream": False
    }

    # Send the HTTP POST request to the local llama instance
    response = requests.post("http://localhost:11434/api/generate", json=payload)

    # Check if the request was successful
    if response.status_code == 200:
        # Extract the response JSON from the HTTP response
        response_json = response.json()

        # Extract the response string from the response JSON
        response_string = response_json["response"]

        # Clean the response string by removing unnecessary characters
        cleaned_response = response_string.strip()

        # Parse the YAML string into a Python dictionary
        challenge_data = yaml.safe_load(cleaned_response)

        # Remove the 'challenges' key
        challenge_data = challenge_data.get('challenges', [])

        # Check the saving method
        #TODO: get database saving working
        save_method = os.getenv("SAVE_METHOD", "yaml")

        # Save challenges based on the chosen method
        if save_method == "yaml":
            save_to_yaml(challenge_data)
            print("Challenges saved to challenges.yaml")
        elif save_method == "db":
            save_to_database(challenge_data)
            print("Challenges saved to the database")
        else:
            print("Invalid saving method:", save_method)
    else:
        print("Error:", response.status_code)

if __name__ == "__main__":
    main()
