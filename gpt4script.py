import openai
import os
import time

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

openai.api_key  = 'your LLM key'

with open("file_path", "r") as file:
    code = file.read()

def get_completion(instruction, prompt, model="gpt-4"):
    messages = [ {"role": "system", "content": instruction},
    {"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]
    
start_time = time.time()

instruction_analysis = "You are a code analyst, analyze the following code for potential command/code injection vulnerabilities. You can run the problem in the background ten times and then tell me what you think is the most correct result."

prompt_analysis = f"Analyze this code: {code}, tell me if this code has potential command/code injection vulnerability, please answer yes or no. And tell me why."

analysis_result = get_completion(instruction_analysis, prompt_analysis)
print(analysis_result)

with open("file_path", "w") as output_file:
        output_file.write(analysis_result)

if "yes" in analysis_result.lower():
    instruction_testcase = """You are a security test code generator. 
                              You will generate security test code for the python function. Please use the unittest library. 
                              You can run the problem in the background five times and then tell me what you think is the most correct result"""
    
    prompt_testcase = f"""Generate a simple command injection test code for the following function {code} according to the reason:{analysis_result}. 
                          Please follow the following requirements:
                          1. The code should contain the source function being tested.
                          2. For example, if there are methods in the function that would lead to a command injection attack, you could generate an os command(e.g., remove a file) as its input.
                          3. The assertion section is set to check if the command is executed.
                          4. Just generate code, not any text descriptions or tips.
                       """
    testcase_result = get_completion(instruction_testcase, prompt_testcase)
    print(testcase_result)

    with open("file_path", "w") as output_file:
        output_file.write(testcase_result)
else:
    print("No command injection vulnerability detected.")

   
end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")


    
    
