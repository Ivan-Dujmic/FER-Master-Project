import subprocess
import time
from datetime import datetime
from openai import OpenAI

# Program that generates all the .txt files needed for prompting
PRERUN_PROGRAM = "TestPromptBuilder.py"

SYSTEM_PROMPT_FILE = "prompt_texts/system.txt"
USER_PROMPT_FILE = "prompt_texts/user.txt"
EXPECTED_FILE = "prompt_texts/expected.txt"
RESULTS_FILE = "prompt_texts/results.txt"

MODEL_NAME = "gpt-4o"

# Adjust based on rate limits
DELAY_SECONDS = 1.0

# Usually "python" for Windows and "python3" for Unix-based systems
PYTHON_EXECUTABLE = "python3"

def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()

client = OpenAI()
prompt_system = read_file(SYSTEM_PROMPT_FILE)
results_file = None

print("Starting grading loop. Press Ctrl+C to stop.")

try:
    results_file = open(RESULTS_FILE, "a", encoding="utf-8")

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

        # Log the results
        results_file.write(f"{timestamp}\n")
        results_file.write(f"Model: {model_output}\n")
        results_file.write(f"{expected_output}\n")
        results_file.write("-" * 40 + "\n")
        results_file.flush()

        time.sleep(DELAY_SECONDS)

except KeyboardInterrupt:
    print("\nStopped by user.")

finally:
    if results_file:
        results_file.close()