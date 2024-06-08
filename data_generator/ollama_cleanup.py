import yaml
import requests
import json
import numpy as np

# Step 1: Read the challenges.yaml file
with open('challenges.yaml', 'r') as file:
    data = yaml.safe_load(file)

# Extract task descriptions
tasks = [challenge['task'] for challenge in data if 'task' in challenge]

# Step 2: Generate Embeddings
def get_embedding(challenge):
    url = "http://localhost:11434/api/embeddings"
    payload = json.dumps({
        "model": "all-minilm",
        "prompt": challenge
    })
    headers = {
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()
        return response.json().get('embedding')
    except requests.exceptions.RequestException as e:
        print(f"Error fetching embedding for challenge: {e}")
        return None

embeddings = {}
for i, task in enumerate(tasks):
    print(f"Generating embedding for challenge {i+1}/{len(tasks)}")
    embedding = get_embedding(task)
    if embedding:
        embeddings[i] = embedding
    else:
        print(f"Failed to generate embedding for challenge {i+1}")

# Step 3: Calculate Similarities
def cosine_similarity(vec1, vec2):
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

similarities = []
for i in range(len(embeddings)):
    for j in range(i + 1, len(embeddings)):
        sim = cosine_similarity(embeddings[i], embeddings[j])
        if sim >= 0.85:
            similarities.append((i, j, sim))

# Step 4: Remove Similar Challenges
to_remove = set()
for i, j, sim in similarities:
    to_remove.add(j)

filtered_data = [challenge for i, challenge in enumerate(data) if i not in to_remove]

# Step 5: Save the Updated challenges.yaml File
with open('challenges_cleaned.yaml', 'w') as file:
    yaml.safe_dump(filtered_data, file, allow_unicode=True)

print("Filtered challenges saved to challenges_cleaned.yaml")
