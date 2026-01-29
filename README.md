# Upute za pokretanje jupyter bilježnica

1. Potrebne nadogradnje:
  ```
  pip install notebook pandas numpy matplotlib
  ```
2. Stavite CSV datoteke `studentTestQuestion.csv` i `questionAnswerGrader.csv` u root folder projekta (isti folder gdje su .ipynb i .py)
3. Iz root foldera pokrenite Jupyter Notebook naredbom
  ```
  jupyter notebook
  ```

# Upute za pokretanje TestPromptBuilder.py

1. Pratiti upute za pokretanje jupyter bilježnice
2. Po želji izmjeniti datoteke `system.txt` i `user_template.txt` koje čine prompt.
3. Postaviti combined_prompt u `TestPromptBuilder.py` na True ako se NE koristi `Prompter.py`, a ako se koristi onda na False
4. Iz root foldera pokrenite TestPromptBuilder.py s naredbom

  Windows:
  ```
  python TestPromptBuilder.py
  ```
  Linux/macOS:
  ```
  python3 TestPromptBuilder.py
  ```
5. Potpuni prompt je u `user.txt`, a Edgar i manual ocijene su u `expected.txt`
