import subprocess
import time
import csv
import re
from datetime import datetime
from openai import OpenAI

# Program that generates all the .txt files needed for prompting
PRERUN_PROGRAM = "TestPromptBuilder.py"

SYSTEM_PROMPT_FILE = "prompt_texts/system.txt"
USER_PROMPT_FILE = "prompt_texts/user.txt"
EXPECTED_FILE = "prompt_texts/expected.txt"
RESULTS_FILE = "prompt_texts/results.csv"

MODEL_NAME = "gpt-4o"

# Adjust based on rate limits
DELAY_SECONDS = 1.0

# Usually "python" for Windows and "python3" for Unix-based systems
PYTHON_EXECUTABLE = "python"

def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()

def extract_grade(model_output):
    """Extract grade number from model output"""
    match = re.search(r'GRADE:\s*(\d+)', model_output)
    if match:
        return int(match.group(1))
    # Fallback: try to find any number
    match = re.search(r'\b(\d+)\b', model_output)
    return int(match.group(1)) if match else None

def extract_explanation(model_output):
    """Extract explanation from model output"""
    match = re.search(r'EXPLANATION:(.*)', model_output, re.DOTALL)
    if match:
        return match.group(1).strip().replace('\n', ' | ')
    return "No explanation provided"

client = OpenAI()
prompt_system = read_file(SYSTEM_PROMPT_FILE)

# Initialize CSV file with headers if it doesn't exist
try:
    with open(RESULTS_FILE, 'x', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Timestamp', 'AI_Grade', 'Edgar_Grade', 'Manual_Grade', 'Explanation'])
except FileExistsError:
    pass  # File already exists

print("Starting grading loop. Press Ctrl+C to stop.")

try:
    with open(RESULTS_FILE, "a", encoding="utf-8", newline='') as results_file:
        csv_writer = csv.writer(results_file)

    while True:
        # Generate new prompt and expected output (blocking)
        subprocess.run(
            [PYTHON_EXECUTABLE, PRERUN_PROGRAM],
            check=True
        )

        prompt_user = read_file(USER_PROMPT_FILE)
        expected_output = read_file(EXPECTED_FILE)

        # Prompt the model
        response = client.chat.completions.create(
            model=MODEL_NAME,
            temperature=0,
            messages=[
                {"role": "system", "content": prompt_system},
                {"role": "user", "content": prompt_user}
            ]
        )

        model_output = response.choices[0].message.content.strip()
        timestamp = datetime.utcnow().isoformat()

        # Parse expected grades (Edgar: X\nManual: Y)
        edgar_grade = None
        manual_grade = None
        for line in expected_output.split('\n'):
            if line.startswith('Edgar:'):
                edgar_grade = line.split(':')[1].strip()
            elif line.startswith('Manual:'):
                manual_grade = line.split(':')[1].strip()

        # Extract AI grade and explanation
        ai_grade = extract_grade(model_output)
        explanation = extract_explanation(model_output)

        # Write to CSV
        csv_writer.writerow([timestamp, ai_grade, edgar_grade, manual_grade, explanation])
        results_file.flush()

        print(f"Graded: AI={ai_grade}, Edgar={edgar_grade}, Manual={manual_grade}")

        time.sleep(DELAY_SECONDS)

except KeyboardInterrupt:
    print("\nStopped by user.")

finally:
    pass  # Context manager handles file closing