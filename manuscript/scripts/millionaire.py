import json

from query_llm import ask_llm

"""An example of how to use structured outputs. 
The idea is to create a who wants to be a millionaire style game,
where the LLM generates questions and answers. 

Because we have to "render" the question and decide what is correct, 
we ask the LLM to return a structured JSON output.

There are three examples
1) generate_question, just naively returns the question as text - almost impossible to reliably parse.
2) generate_question_structured, asks the LLM to return a JSON string
3) generate_question_structured_examples: same as 2 but with an example of the expected output format. This is the most reliable.
"""


def get_question_prompt(amount):
    question_prompt = f"""You are creating a question in the style of the game show'Who Wants to Be a Millionaire'. 
Create a ${amount} question with 4 options and indicate the correct answer."""
    return question_prompt

def generate_question(amount):
    question_prompt = get_question_prompt(amount)
    return ask_llm(question_prompt)

def generate_question_structured(amount):
    question_prompt = get_question_prompt(amount)
    structured_prompt = f"""{question_prompt}
Return the question in the following JSON format:
{{
    "question": "The question text",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "answer": "The correct option (A, B, C, or D)"
}}
"""
    return ask_llm(structured_prompt)

def generate_question_structured_example(amount):
    question_prompt = get_question_prompt(amount)
    structured_prompt = f"""{question_prompt}
Return the question in the following JSON format:
{{
    "question": "The question text",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "answer": "The correct option (A, B, C, or D)"
}}

Example:
{{
    "question": "What is the capital of France?",
    "options": ["Berlin", "Madrid", "Paris", "Rome"],
    "answer": "C"
}}
"""
    return ask_llm(structured_prompt)

def extract_dict_from_response(response):
    try:
        start = response.index("{")
        end = response.rindex("}") + 1
        json_str = response[start:end]
        return json.loads(json_str)
    except (ValueError, json.JSONDecodeError) as e:
        print(f"Error extracting JSON: {e}")
        return None

def single_question(amount):
    structured_data = generate_question_structured_example(amount)
    question_dict = extract_dict_from_response(structured_data)
    if question_dict is None:
        print("Failed to extract question data.")
        return
    print(f"**** {amount} $ Question ****")
    print(f"Question: {question_dict['question']}")
    for i, option in enumerate(question_dict['options']):
        print(f"{chr(65+i)}. {option}")


def run_game():
    #print(generate_question_structured())
    single_question(1000)

if __name__=="__main__":
    run_game()

