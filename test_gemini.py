from gemini_config import gemini

try:
    # Test simple text generation
    prompt = "Explain how AI works in simple terms"
    response = gemini.generate_response(prompt)
    
    print("\nAI Response:")
    print("-" * 50)
    print(response)

except Exception as e:
    print(f"An error occurred: {str(e)}")