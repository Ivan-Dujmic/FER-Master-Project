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

# Upute za pokretanje Prompter.py ( € $ )

1. Pratiti upute za pokretanje TestPromptBuilder.py
2. Potrebne nadogradnje:
  ```
  pip install openai
  ```
3. Generirati key na https://platform.openai.com/settings/organization/api-keys
4. Postaviti key

  Windows:
  ```
  setx OPENAI_API_KEY "api_key"
  ```
  Linux/macOS:
  ```
  export OPENAI_API_KEY="api_key"
  ```
5. Pregledati i po potrebi podesiti konfiguracije na početku `Prompter.py` datoteke
6. Iz root foldera pokrenite Prompter.py s naredbom

  Windows:
  ```
  python Prompter.py
  ```
  Linux/macOS:
  ```
  python3 Prompter.py
  ```
7. Rezultati se ispisuju u `results.txt`
