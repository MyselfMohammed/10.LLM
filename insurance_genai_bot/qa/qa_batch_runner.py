from dotenv import load_dotenv
load_dotenv()

import os
import sys
import pandas as pd
from datetime import datetime
import pytz

from utils.excel_loader import load_questions_from_excel_all_sheets
from qa.response_quality import response_quality_checks, get_response_quality_columns
from qa.pipeline_health import health_report

def get_ist_now():
    ist = pytz.timezone('Asia/Kolkata')
    return datetime.now(ist)

def get_bot_response(query):
    from core.rag_engine import get_rag_chain
    qa_chain = get_rag_chain()
    response = qa_chain.invoke(query)
    return response["result"] if isinstance(response, dict) else str(response)

def ensure_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

def critical_pass(checks):
    # Adjust criteria as needed for "Pass"
    if (checks.get("Non-empty", "").startswith("Empty") or
        ("PII" in checks.get("PII Check", "") and "detected" in checks.get("PII Check", "") and checks.get("PII Check", "") != "No PII detected") or
        checks.get("Moderation", "") != "No Moderation Flagged (PASS)" or ("(LOW)" in str(checks.get("Semantic No Hallucination", ""))) or
        ("FAIL" in str(checks.get("Keyword Hallucination", ""))) or ("FAIL" in str(checks.get("Relevance", "")))):
        return False
    return True

def main(input_excel):
    qa_folder = "qa/qa_output"
    ensure_folder(qa_folder)
    now_ist = get_ist_now()
    timestamp_str = now_ist.strftime("%d_%m_%Y_%I_%M_%p_IST")
    output_file = f"QA_Results_{timestamp_str}.xlsx"
    output_path = os.path.join(qa_folder, output_file)

    questions = load_questions_from_excel_all_sheets(input_excel)
    log_rows = []

    for sheet, question in questions:
        dt = get_ist_now()
        date_str = dt.strftime("%d-%m-%Y")
        time_str = dt.strftime("%I:%M:%S %p IST")
        h = health_report(get_bot_response, question)
        answer, latency = h["result"], h["latency"]

        checks = response_quality_checks(answer, question, context_docs=None, context=None, latency=latency)
        status = "Pass" if critical_pass(checks) else "Fail"

        row = {"Date": date_str, "Time": time_str, "Sheet Name": sheet, "Question": question, "Response": answer, "Status": status,}
        row.update(checks)
        log_rows.append(row)
        print(f"[{sheet}] {question} | {status} | {latency:.2f}s")

    quality_cols = get_response_quality_columns()
    columns = ["Date", "Time", "Sheet Name", "Question", "Response"] + quality_cols + ["Status"]

    df = pd.DataFrame(log_rows)
    final_columns = [col for col in columns if col in df.columns]
    df = df[final_columns]
    df.to_excel(output_path, index=False)

    # --- Auto-fit all columns ---
    import openpyxl
    wb = openpyxl.load_workbook(output_path)
    ws = wb.active
    for col in ws.columns:
        max_length = 0
        column = col[0].column_letter
        for cell in col:
            try:
                cell_value = str(cell.value) if cell.value is not None else ""
                max_length = max(max_length, len(cell_value))
            except Exception:
                pass
        adjusted_width = max_length + 2
        ws.column_dimensions[column].width = adjusted_width
    wb.save(output_path)

    print(f"\n✅ QA results saved to: {output_path}")


if __name__ == "__main__":
    DEFAULT_EXCEL = "qa/qa_input/qa_test_questions.xlsx"
    if len(sys.argv) < 2:
        print(f"No Excel file argument passed, using default: {DEFAULT_EXCEL}")
        input_excel = DEFAULT_EXCEL
    else:
        input_excel = sys.argv[1]
    main(input_excel)
