import pandas as pd
import os
import re

def find_question_column(columns):
    # Return the column name that matches "question" (case-insensitive, ignore spaces)
    for col in columns:
        if re.sub(r'\s+', '', col.lower()) == "question":
            return col
    return None

def load_questions_from_excel_all_sheets(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    xl = pd.ExcelFile(file_path)
    all_questions = []
    for sheet_name in xl.sheet_names:
        df = xl.parse(sheet_name)
        col = find_question_column(df.columns)
        if col:
            questions = df[col].dropna().tolist()
            for q in questions:
                all_questions.append((sheet_name, str(q)))
        else:
            print(f"Sheet '{sheet_name}' has no 'question' column (case/space-insensitive).")
    return all_questions  # list of (sheet, question)

# Example usage for test/debug:
if __name__ == "__main__":
    excel_path = "qa/qa_test_questions.xlsx"
    qs = load_questions_from_excel_all_sheets(excel_path)
    for sheet, q in qs:
        print(f"[{sheet}] {q}")
