import yaml
import os

# Function to create folder if it doesn't exist
def create_folder_if_not_exist(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

# Load YAML file
with open('challenges.yaml', 'r') as file:
    challenges = yaml.safe_load(file)

# Divide challenges based on difficulty
easy_challenges = []
medium_challenges = []
hard_challenges = []
other_challenges = []

for challenge in challenges:
    difficulty = challenge.get('difficulty', 'medium')  # default to medium if difficulty field not present
    if 'difficulty' in challenge:
        del challenge['difficulty']  # remove difficulty field

    if difficulty == 'easy':
        easy_challenges.append(challenge)
    elif difficulty == 'medium':
        medium_challenges.append(challenge)
    elif difficulty == 'hard':
        hard_challenges.append(challenge)
    else:
        other_challenges.append(challenge)

# Create output folder if it doesn't exist
create_folder_if_not_exist('output')

# Save challenges into separate YAML files
with open('output/easy.yaml', 'w') as file:
    yaml.dump(easy_challenges, file)

with open('output/medium.yaml', 'w') as file:
    yaml.dump(medium_challenges, file)

with open('output/hard.yaml', 'w') as file:
    yaml.dump(hard_challenges, file)

if other_challenges:
    print("Warning: Some challenges were not categorized into easy, medium, or hard difficulty.")
    with open('output/other.yaml', 'w') as file:
        yaml.dump(other_challenges, file)
