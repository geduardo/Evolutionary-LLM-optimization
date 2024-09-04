import anthropic
import os

def generate_response_anthropic(model: str, max_tokens: int, input_text: str) -> anthropic.types.Message:
    """
    Generate a response using the Anthropic API.

    Args:
        model (str): The model to use for generating the response.
        max_tokens (int): The maximum number of tokens to generate.
        input_text (str): The input text to generate a response for.

    Returns:
        anthropic.types.Message: The generated message object.

    Raises:
        ValueError: If the ANTHROPIC_API_KEY environment variable is not set.
        Exception: If an error occurs during the API call.
    """
    # Read the API key from an environment variable
    api_key = os.getenv("ANTHROPIC_API_KEY")

    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is not set")

    try:
        client = anthropic.Anthropic(api_key=api_key)
        message = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            messages=[
                {"role": "user", "content": input_text}
            ]
        )
        return message
    except Exception as e:
        print(f"An error occurred: {e}")
        raise
    
