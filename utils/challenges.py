import yaml
import os
import random

CHALLENGES_FOLDER = 'challenges'
DIFFICULTY_FILES = {
    'easy': 'easy.yaml',
    'medium': 'medium.yaml',
    'hard': 'hard.yaml'
}

def load_challenges():
    """
    Load challenges from different files based on difficulty level and return a dictionary of challenges.
    """
    challenges = {}
    for difficulty, filename in DIFFICULTY_FILES.items():
        filepath = os.path.join(CHALLENGES_FOLDER, filename)
        with open(filepath, 'r') as file:
            challenges[difficulty] = yaml.safe_load(file)
    return challenges

def select_random_challenge(challenges, difficulty):
    return random.choice(challenges.get(difficulty, []))
