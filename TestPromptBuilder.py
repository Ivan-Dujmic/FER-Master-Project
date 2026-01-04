import pandas as pd

# Load CSV files
attempts = pd.read_csv("studentTestQuestion.csv", sep=";")
questions = pd.read_csv("questionAnswerGrader.csv", sep=";")

# Load prompt template
with open("promptTemplate.txt", "r", encoding="utf-8") as f:
    template = f.read()

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
output_prompt = template
output_prompt = output_prompt.replace("<PROBLEM>", str(question_row["question_text"]))
output_prompt = output_prompt.replace("<GRADER>", str(question_row["grader_object"]))
output_prompt = output_prompt.replace("<COMMENT>", str(question_row["question_comment"]))
output_prompt = output_prompt.replace("<ATTEMPT>", str(attempt_row["student_answer_code"]))

# Write populated prompt
with open("promptOutput.txt", "w", encoding="utf-8") as f:
    f.write(output_prompt)

# Write expected output
with open("promptExpected.txt", "w", encoding="utf-8") as f:
    f.write(f"Edgar: {attempt_row['question_score_perc_ed']}\n")
    f.write(f"Manual: {attempt_row['question_score_perc_man']}\n")