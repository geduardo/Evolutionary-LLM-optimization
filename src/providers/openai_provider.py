import openai
import os

def generate_response_openai(model: str, max_tokens: int, input_text: str) -> openai.types.Completion:
    """
    Generate a response using the OpenAI API.

    Args:
        model (str): The model to use for generating the response.
        max_tokens (int): The maximum number of tokens to generate.
        input_text (str): The input text to generate a response for.

    Returns:
        openai.types.Completion: The generated completion object.

    Raises:
        ValueError: If the OPENAI_API_KEY environment variable is not set.
        Exception: If an error occurs during the API call.
    """
    # Read the API key from an environment variable
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set")

    try:
        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=model,
            max_tokens=max_tokens,
            messages=[
                {"role": "user", "content": input_text}
            ]
        )
        return response
    
    except Exception as e:
        print(f"An error occurred: {e}")
        raise
