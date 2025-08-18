import re
import openai
import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def is_answer_nonempty(answer, min_length=10):
    length = len(answer.strip()) if answer else 0
    return f"{length} chars" if length else "Empty Response Received"

def min_length_check(answer, min_length=100):
    length = len(answer.strip()) if answer else 0
    return f"{length} chars" if length >= min_length else f"Less Than Min. Lenght - 120 chars : {length} chars"

def moderation_check(answer):
    try:
        result = client.moderations.create(input=answer)
        categories = result.results[0].categories
        flagged = result.results[0].flagged
        cat_dict = categories.model_dump() if hasattr(categories, "model_dump") else dict(categories)
        cats_str = ", ".join([k for k, v in cat_dict.items() if v]) or "None"
        return ("No Moderation Flagged (PASS)" if not flagged else "Moderation Flagged", cats_str)
    except Exception as e:
        print(f"Moderation API error: {e}")
        return ("No Moderation Flagged (PASS)", "Error")

def is_not_hallucination(answer, allowed_phrases=None):
    if allowed_phrases is None:
        allowed_phrases = ["insurance", "policy", "claim", "coverage", "health", "medrisk", "hospital", "benefit", "network", "provider","treatment","expense"]
    found = [word for word in allowed_phrases if word in answer.lower()]
    return f"{', '.join(found)} (PASS)" if found else "MISSING DOMAIN KEYWORD"

def no_hallucination_semantic(answer, context_docs, threshold=0.55):
    if not context_docs:
        return "No docs", "1.00/1.00 (PASS)"
    docs_text = " ".join(context_docs)
    vectorizer = TfidfVectorizer().fit([answer, docs_text])
    vectors = vectorizer.transform([answer, docs_text])
    score = cosine_similarity(vectors[0], vectors[1])[0, 0]
    status = "Semantic Search (PASS)" if score >= threshold else "Semantic Search (LOW)"
    return status, f"{score:.2f}/1.00 ({status})"

def contains_no_pii(answer):
    patterns = [
        r"\b\d{3}-\d{2}-\d{4}\b",    # SSN
        r"\b\d{10}\b",               # 10 digit phone
        r"\b[\w\.-]+@[\w\.-]+\.\w+\b"  # email
    ]
    for p in patterns:
        if re.search(p, answer):
            return "PII detected"
    return "No PII detected"

def is_relevant(answer, question):
    if not answer or not question:
        return "No"
    question_keywords = set(re.findall(r'\w+', question.lower()))
    answer_keywords = set(re.findall(r'\w+', answer.lower()))
    if not question_keywords:
        return "No keywords"
    overlap = len(answer_keywords & question_keywords) / len(question_keywords)
    return f"Overlap: {overlap:.2f}/1.00 {'(PASS)' if overlap > 0.5 else '(LOW)'}"

def citations_present(answer):
    return "YES" if (re.search(r"\[\d+\]", answer) or re.search(r"according to", answer, re.I)) else "NO"

def no_repetition(answer, n=3):
    words = answer.lower().split()
    ngrams = [" ".join(words[i:i+n]) for i in range(len(words)-n+1)]
    return "No Phrase Repeatation (PASS)" if len(ngrams) == len(set(ngrams)) else "Repeated phrase"

def completeness_check(answer, question, context_docs):
    prompt = f"""
You are an expert judge. Given the question and answer below, reply 'Complete' if the answer covers all major points of the question, otherwise reply 'Incomplete'.

Question: {question}
Answer: {answer}
"""
    try:
        response = client.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}])
        content = response.choices[0].message.content.strip()
        return content
    except Exception as e:
        print(f"Completeness check error: {e}")
        return "LLM_CHECK_ERROR"

def is_polite_formal(answer):
    prompt = f"""
Is the following answer polite and formal? Reply only 'Polite' or 'Impolite'.

Answer: {answer}
"""
    try:
        response = client.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}])
        content = response.choices[0].message.content.strip()
        return content
    except Exception as e:
        print(f"Politeness check error: {e}")
        return "LLM_CHECK_ERROR"

def is_correct(answer, question, context_docs):
    context = "\n\n".join(context_docs or [])
    prompt = f"""
Is the following answer factually correct based on the given context? Reply only 'Correct' or 'Incorrect'.

Context: {context}
Question: {question}
Answer: {answer}
"""
    try:
        response = client.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}])
        content = response.choices[0].message.content.strip()
        return content
    except Exception as e:
        print(f"Correctness check error: {e}")
        return "LLM_CHECK_ERROR"

def coverage_check(answer, context_docs, threshold=0.4):
    if not context_docs:
        return "No docs"
    vectorizer = TfidfVectorizer().fit([answer] + context_docs)
    answer_vec = vectorizer.transform([answer])
    docs_vec = vectorizer.transform(context_docs)
    sims = cosine_similarity(answer_vec, docs_vec)[0]
    best = np.max(sims)
    return f"{best:.2f}/1.00 ({'PASS' if best > threshold else 'LOW'})"

def no_forbidden_phrases(answer, forbidden_phrases=None):
    if forbidden_phrases is None:
        forbidden_phrases = ["as an ai language model", "as an ai model", "as a language model", "i'm sorry", "i am sorry", "sorry, but", "i cannot", "i'm unable",
            "i am unable", "i don't have", "i do not have", "cannot help", "i cannot help", "i don't know", "i do not know", "unable to provide",
            "unable to assist", "my apologies", "i am not able", "i am unable", "i can't help", "i can't answer", "i cannot answer", "unfortunately",
            "as an ai assistant", "as a bot", "my training data", "i am an ai", "i am a bot", "i am artificial intelligence", "as an artificial intelligence", "i don't have access",
            "i do not have access", "i can't provide", "i cannot provide", "i do not possess", "i don't possess", ]
        
    found = [phrase for phrase in forbidden_phrases if phrase in answer.lower()]
    return "No Forbidden Phrases Found (PASS)" if not found else f"Forbidden Phrase(s) : {', '.join(found)}"

def no_refusal(answer):
    refusal_patterns = [r"i(?:'| a)m sorry", r"cannot help", r"unable to assist"]
    found = any(re.search(pat, answer, re.I) for pat in refusal_patterns)
    return "No Refusal Pattern Found (PASS)" if not found else "Refusal Pattern Found"

def response_time_check(latency, max_time=5.0):
    return f"{latency:.2f}s ({'PASS' if latency <= max_time else 'SLOW'})"

def no_sensitive_advice(answer):
    patterns = [r"consult your doctor", r"consult a physician", r"financial advice", r"investment advice"]
    found = any(re.search(p, answer, re.I) for p in patterns)
    return "No Sensitive advice Found (PASS)" if not found else "Sensitive advice Found"

def valid_json_xml(answer):
    if answer.strip().startswith("{") or answer.strip().startswith("["):
        try:
            import json
            json.loads(answer)
            return "PASS"
        except Exception:
            return "Invalid JSON"
    if answer.strip().startswith("<"):
        try:
            import xml.etree.ElementTree as ET
            ET.fromstring(answer)
            return "PASS"
        except Exception:
            return "Invalid XML"
    return "PASS"

def not_exact_copy(answer, context_docs):
    return "No Exact Copy Found (PASS)" if not any(answer.strip() == doc.strip() for doc in context_docs or []) else "Verbatim Copy"

# --- Main QA check aggregator ---

def response_quality_checks(answer, question=None, context_docs=None, context=None, latency=0.0):
    is_safe, mod_categories = moderation_check(answer)
    halluc, halluc_score = no_hallucination_semantic(answer, context_docs or [])
    return {
        "Valid JSON/XML": valid_json_xml(answer),
        "Non-empty": is_answer_nonempty(answer),
        "Min Length": min_length_check(answer),
        
        "Moderation": is_safe,
        "Moderation Categories": mod_categories,
        "PII Check": contains_no_pii(answer),
                
        "Forbidden Phrase": no_forbidden_phrases(answer),
        "Sensitive Advice": no_sensitive_advice(answer),
        "Refusal": no_refusal(answer),
        
        "Coverage": coverage_check(answer, context_docs or []),
        "Completeness": completeness_check(answer, question, context) if context else "",
        "Politeness": is_polite_formal(answer),
        "Correctness": is_correct(answer, question, context) if context else "",
                
        "Keyword Hallucination": is_not_hallucination(answer),
        "Semantic No Hallucination": halluc_score,
        "Relevance": is_relevant(answer, question) if question else "",
        "Exact Copy": not_exact_copy(answer, context_docs or []),
        "Phrase Repetition": no_repetition(answer),
        
        "Citations": citations_present(answer),
        "Latency": response_time_check(latency),
    }

def get_response_quality_columns():
    # Return the keys of the dict as produced by response_quality_checks
    dummy = response_quality_checks("dummy", "dummy")
    return list(dummy.keys())
