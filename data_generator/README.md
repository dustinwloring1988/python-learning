# Python Challenge Generator

This project generates Python programming challenges and categorizes them based on difficulty levels. The challenges are fetched from a local llama instance, filtered to remove duplicates based on similarity, and then saved into separate YAML files based on their difficulty level.

## Project Structure

- `generate_challenges.py`: Script to generate Python challenges by sending a POST request to a local llama instance and saving the challenges to a `challenges.yaml` file.
- `filter_similar_challenges.py`: Script to read the `challenges.yaml` file, generate embeddings for each challenge, filter out similar challenges, and save the cleaned challenges to a `challenges_cleaned.yaml` file.
- `categorize_challenges.py`: Script to categorize challenges based on their difficulty level and save them into separate YAML files in the `output` folder.
- `README.md`: This file.

## Requirements

- Python 3.6 or higher
- Required Python libraries:
  - `requests`
  - `pyyaml`
  - `numpy`

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/python-challenge-generator.git
   cd python-challenge-generator
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required libraries:
   ```bash
   pip install requests pyyaml numpy
   ```

## Usage

### Step 1: Generate Challenges

Run the `generate_challenges.py` script to generate Python challenges:
```bash
python generate_challenges.py
```
This script sends a POST request to a local llama instance to generate challenges and saves them in a `challenges.yaml` file.

### Step 2: Filter Similar Challenges

Run the `filter_similar_challenges.py` script to filter out similar challenges:
```bash
python filter_similar_challenges.py
```
This script reads the `challenges.yaml` file, generates embeddings for each challenge, filters out similar challenges, and saves the cleaned challenges to a `challenges_cleaned.yaml` file.

### Step 3: Categorize Challenges

Run the `categorize_challenges.py` script to categorize challenges based on difficulty:
```bash
python categorize_challenges.py
```
This script reads the `challenges_cleaned.yaml` file, categorizes challenges into easy, medium, and hard, and saves them into separate YAML files in the `output` folder.

## Output

The output folder will contain the following files:
- `easy.yaml`: Contains easy challenges.
- `medium.yaml`: Contains medium challenges.
- `hard.yaml`: Contains hard challenges.
- `other.yaml` (optional): Contains challenges that were not categorized into easy, medium, or hard.

## Notes

- Ensure your local llama instance is running and accessible at the specified URL before running the scripts.
- The similarity threshold for filtering challenges is set to 0.85. You can adjust this threshold in the `filter_similar_challenges.py` script if needed.

## License

This project is licensed under the MIT License.
```
