import os
from groq import Groq

def generate_response(messages):
    api_key = os.environ.get('GROQ_API_KEY')
    model = os.environ.get('LLM_MODEL_NAME', 'llama3-70b-8192')
    
    if not api_key:
        print("Error: GROQ_API_KEY is not set in environment.")
        return "I'm having a little trouble connecting to my brain right now. Please try again in a moment!"
    
    try:
        client = Groq(api_key=api_key)
        chat_completion = client.chat.completions.create(
            messages=messages,
            model=model,
            temperature=0.7,
            max_tokens=512
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"Error calling Groq: {e}")
        return "I'm having a little trouble connecting to my brain right now. Please try again in a moment!"
