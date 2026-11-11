import os
import argparse
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
import json
from call_function import available_functions, call_function

def generate_content(client: OpenAI, messages: list, verbose: bool) -> None:
	for num in range(20):
		response = client.chat.completions.create(
			model="openrouter/free",
			messages=messages,
			tools=available_functions,
			temperature=0,
		)

		if response.usage is not None and verbose:	
			print(f"Prompt tokens: {response.usage.prompt_tokens}\nResponse tokens: {response.usage.completion_tokens}")

		message = response.choices[0].message
		messages.append(message)
		if message.tool_calls:
			for tool_call in message.tool_calls:
				result_message = call_function(tool_call, verbose)
				messages.append(result_message)
				if not result_message["content"]:
					raise Exception("Empty result")
				if verbose is True:
					print(f"-> {result_message['content']}")
		else:
			print(message.content)
			break
	else:
		print("Limit reached, giving up now...")

def main():
	load_dotenv()
	api_key = os.environ.get("OPENROUTER_API_KEY")
	if api_key is None:
	        raise RuntimeError("key is missing")
                
	client = OpenAI(
	        base_url="https://openrouter.ai/api/v1",
	        api_key=api_key,
	)

	parser = argparse.ArgumentParser(description="Chatbot")
	parser.add_argument("user_prompt", type=str, help="Please enter your prompt")
	parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
	args = parser.parse_args()
                        
	messages = [
	        {"role": "system", "content": system_prompt},
	        {"role": "user", "content": args.user_prompt},
	]
	generate_content(client, messages, args.verbose)

if __name__ == "__main__":
	main()
