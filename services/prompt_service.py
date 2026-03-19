from prompts.templates import SYSTEM_PROMPT, SCOPE_INSTRUCTIONS

def build_prompt(query, history, context_chunks, scope):
    history_text = ""
    for msg in history:
        role = "User" if msg.sender_type == 'user' else "Assistant"
        history_text += f"{role}: {msg.message_text}\n"
        
    context_text = "\n\n".join(context_chunks)
    scope_inst = SCOPE_INSTRUCTIONS.get(scope, SCOPE_INSTRUCTIONS['company_in_scope'])
    
    system_message = SYSTEM_PROMPT.format(
        history=history_text,
        context=context_text,
        scope_instruction=scope_inst
    )
    
    # We return the format suitable for the Together AI messages array
    return [
        {"role": "system", "content": system_message},
        {"role": "user", "content": query}
    ]
