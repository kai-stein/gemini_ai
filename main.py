import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from prompts import system_prompt
from call_function import available_functions,call_function

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
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
        )
    
    if response.usage_metadata is None:
        raise RuntimeError("No responce from model / no metadata")
    
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count }")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    
    if not response.function_calls:
        print("Response:")
        print(response.text)
        return

    for function_call in response.function_calls:
        print(f"Calling function: {function_call.name}({function_call.args})")
        function_call_result = call_function(function_call,args.verbose)
        if function_call_result.parts[0].function_response is None:
            raise Exception("No function responce")
        if function_call_result.parts[0].function_response.response is None:
            raise Exception("No function_response.response")
        if args.verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")

        
if __name__ == "__main__":
    main()
