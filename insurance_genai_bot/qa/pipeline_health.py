import time

def measure_latency(fn, *args, **kwargs):
    start = time.time()
    result = fn(*args, **kwargs)
    latency = time.time() - start
    return result, latency

def check_prompt_success(response):
    # Example: check if LLM actually responded
    return bool(response and isinstance(response, str) and len(response.strip()) > 0)

def health_report(fn, *args, **kwargs):
    result, latency = measure_latency(fn, *args, **kwargs)
    success = check_prompt_success(result)
    return {"success": success, "latency": latency, "result": result}
