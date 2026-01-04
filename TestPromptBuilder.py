import pandas as pd

# The OpenAI API allows separation of system and user prompts
# If true then USER will contain the entire prompt, otherwise the prompt will be split between SYSTEM and USER
combined_prompt = True

SYSTEM_PROMPT_FILE = "prompt_texts/system.txt"
USER_PROMPT_TEMPLATE_FILE = "prompt_texts/user_template.txt"
USER_PROMPT_FILE = "prompt_texts/user.txt"
EXPECTED_FILE = "prompt_texts/expected.txt"

# Load CSV files
attempts = pd.read_csv("studentTestQuestion.csv", sep=";")
questions = pd.read_csv("questionAnswerGrader.csv", sep=";")

user_prompt = ""

# Load system prompt if combined
if combined_prompt:
    with open(SYSTEM_PROMPT_FILE, "r", encoding="utf-8") as f:
        user_prompt = f.read() + "\n\n"

# Load prompt template
with open(USER_PROMPT_TEMPLATE_FILE, "r", encoding="utf-8") as f:
    user_prompt = user_prompt + f.read()

# Ensure we can match questions with attempts
question_ids_with_attempts = set(attempts["id_question"])
valid_questions = questions[questions["question_id"].isin(question_ids_with_attempts)]

# Pick a random question that has at least one attempt
question_row = valid_questions.sample(n=1).iloc[0]
question_id = question_row["question_id"]

# Pick a random attempt for that question
attempt_rows = attempts[attempts["id_question"] == question_id]
attempt_row = attempt_rows.sample(n=1).iloc[0]

# Replace placeholders in the template
user_prompt = user_prompt.replace("<PROBLEM>", str(question_row["question_text"]))
user_prompt = user_prompt.replace("<GRADER>", str(question_row["grader_object"]))
user_prompt = user_prompt.replace("<COMMENT>", str(question_row["question_comment"]))
user_prompt = user_prompt.replace("<ATTEMPT>", str(attempt_row["student_answer_code"]))

# Write populated prompt
with open("prompt_texts/user.txt", "w", encoding="utf-8") as f:
    f.write(user_prompt)
    
# Write expected output
with open("prompt_texts/expected.txt", "w", encoding="utf-8") as f:
    f.write(f"Edgar: {attempt_row['question_score_perc_ed']}\n")
    f.write(f"Manual: {attempt_row['question_score_perc_man']}\n")