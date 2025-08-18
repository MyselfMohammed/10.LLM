def validate_user_query(query):
    if not query or not query.strip():
        return False, "Query cannot be empty."
    if len(query.strip()) < 2:
        return False, "Please Ask Any Specific Question To Proceed Further."
    return True, ""
