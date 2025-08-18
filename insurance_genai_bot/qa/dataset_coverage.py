def check_dataset_coverage(documents, sample_questions):
    # Ensure each sample question matches at least one document (by keyword, etc)
    covered = []
    for q in sample_questions:
        found = any(q.lower() in d.lower() for d in documents)
        covered.append((q, found))
    return covered
