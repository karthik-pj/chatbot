def classify_intent(query):
    """
    Very basic heuristic function to classify intent.
    In a real-world app, this could be an LLM call or a fast classifier model.
    """
    q = query.lower().strip()
    
    greetings = ['hi', 'hello', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening', 'hi there']
    if any(q == g or q.startswith(g + " ") or q.startswith(g + ",") or q.startswith(g + "!") for g in greetings):
        return 'greeting'
        
    # Basic keyword check for external context (mock logic)
    external_keywords = ['what is python', 'where is usa', 'who is pm', 'capital of', 'weather in']
    if any(k in q for k in external_keywords):
        return 'external_out_of_scope'
        
    return 'company_in_scope' # Default to passing it to the main prompt logic
