import os
try:
    import google.generativeai as genai
except ImportError:
    genai = None

def generate_response(context: str, query: str) -> str:
    """
    Generates a response from the AI based on the provided context and query.
    
    Args:
        context (str): The information from the current node and its children.
        query (str): The user's question.
        
    Returns:
        str: The AI's response.
    """
    
    # Construct the system prompt
    system_prompt = (
        "You are a helpful assistant for a chatbot platform. "
        "Your goal is to answer the user's question based ONLY on the provided context. "
        "If the answer is not in the context, politely say you don't know."
    )
    
    full_prompt = f"{system_prompt}\n\nContext:\n{context}\n\nUser Question:\n{query}"
    
    api_key = os.getenv('GEMINI_API_KEY')
    
    if api_key:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-flash-latest')
            response = model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            return f"Error generating response: {str(e)}"
        
    # Mock Response for development/testing (fallback)
    return f"[MOCK AI RESPONSE] (API Key missing) based on context: {context[:200]}..."
