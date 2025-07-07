import json
from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

client = OpenAI()

def run_command(command):
    result = os.system(command=command)
    return result

available_tools = {
    "run_command": {
        "fn": run_command,
        "description": "Takes command as input, to run on system and gives the output."
    }
}

system_prompt = """
    As a helpful AI assistant, you specialize in creating full stack development projects.
    You work on start, plan, action, and observe mode.
    For the given user queries, use the run_command tool to run the command on the system.
    Plan the step-by-step execution based on the planning, and use the run_command tool to run the command on the system.
    Wait for the observation, and based on the observation from the tool call, resolve the user query.

    
    Rules:
    1. Follow the strict JSON output as per Output schema.
    2. Always perform one step at a time and wait for next input
    3. Carefully analyse the user query

    Output JSON Format:
    {{ 
        "step": "string",
        "content": "string",
        "function": "The name of function if the step is action",
        "input": "The input parameter for the function"
    }}

    Available Tools: 
    -run_command: Takes command as input, to run on system and gives the output.

    Example:
    User Query: Create a file called Header which will contain company name - "Rishita", and have navigaton buttons like Careers, About us, Contact us?
    Output: {{"step": "start", "content": "The user is interested in creating a new file called Header"}}
    Output: {{"step": "plan", "content": "From the available tools, I should call run_command"}}
    Output: {{"step": "action", "function": "run_command", "input": "touch Header.html"}}
    Output: {{"step": "observe", "output": "Header.html created"}}
    Output: {{"step": "output", "content": "Header.html created successfully"}}
"""

messages = [
    {"role": "system", "content": system_prompt}
]
while True:
    user_query = input('> ')
    if user_query.lower() == "bye":
        print("👋 Goodbye!")
        break
    messages.append({"role": "user", "content": user_query})
    while True:
        response = client.chat.completions.create(
        model="gpt-4o",
        response_format={"type": "json_object"},
        messages=messages
        )
        parsed_output = json.loads(response.choices[0].message.content)
        messages.append({"role": "assistant", "content": json.dumps(parsed_output)})
        if parsed_output.get("step") == "plan":
            print(f"🧠: {parsed_output.get("content")}")
            continue
        if parsed_output.get("step") == "action":
            tool_name = parsed_output.get("function")
            tool_input = parsed_output.get("input")

            if available_tools.get(tool_name, False) != False:
                tool_fn = available_tools[tool_name]["fn"]
                if isinstance(tool_input, dict):
                    output = tool_fn(**tool_input)  # for functions like add(x, y)
                else:
                    output = tool_fn(tool_input)
                messages.append({"role": "assistant", "content": json.dumps({"step": "observe", "output": output})})
                continue

        if parsed_output.get("step") == "output":
            print(f"🤖: {parsed_output.get("content")}")
            break