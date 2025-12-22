import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from prompts import system_prompt

def main():
    print("Hello from gemini-ai!")

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    model_name = os.environ.get("AI_MODEL_NAME")

    if not api_key:
        raise RuntimeError("No api key in .env file")

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=model_name, 
        contents=messages,
        config=types.GenerateContentConfig(system_instruction=system_prompt),
        )
    
    if response.usage_metadata is None:
        raise RuntimeError("No responce from model / no metadata")
    
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count }")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    
        

    print(response.text)


if __name__ == "__main__":
    main()
