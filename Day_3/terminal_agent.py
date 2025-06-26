import json
from dotenv import load_dotenv
from openai import OpenAI
import requests
import os

load_dotenv()

client = OpenAI()

def run_command(command):
    result = os.system(command=command)
    return result

def get_weather(city: str):
    # TODO: Code an actual API call
    print("tool called", city)
    url = f"https://wttr.in/{city}?format=%C+%t"
    response = requests.get(url)
    if response.status_code == 200:
        return f"The weather in {city} is {response.text}"
    return "Something went wrong"

def add(x, y):
    return x + y

available_tools = {
    "get_weather": {
        "fn": get_weather,
        "description": "This function takes city name as an input and gives the weather of the city as output."
    },
    "add": {
        "fn": add,
        "description": "This function takes two numbers x and y and returns sum of the given input that is x + y."
    },
    "run_command": {
        "fn": run_command,
        "description": "Takes command as input, to run on system and gives the output."
    }
}

system_prompt = """
    As a helpful AI assistant, you specialize in solving user queries.
    You work on start, plan, action, and observe mode.
    For the given user queries and available tools, plan the step-by-step execution based on the planning.
    Select the relevant tool from the available tools, and based on the tool selection, you perform an action to call the tool.
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
    - get_weather: This function takes city name as an input and gives the weather of the city as output.
    - add: This function takes two numbers x and y and returns sum of the given input that is x + y.
    -run_command: Takes command as input, to run on system and gives the output.

    Example:
    User Query: What is the weather of New York?
    Output: {{"step": "start", "content": "The user is interested in weather data of new york"}}
    Output: {{"step": "plan", "content": "From the available tools, I should call get_weather"}}
    Output: {{"step": "action", "function": "get_weather", "input": "new york"}}
    Output: {{"step": "observe", "output": "12 Degree Celcius"}}
    Output: {{"step": "output", "content": "The weather of new york seems to be 12 Degree Celcius"}}

    User Query: What is 4637 + 2332?
    Output: {{"step": "start", "content": "The user is interested in addition of two numbers"}}
    Output: {{"step": "plan", "content": "From the available tools, I should call add"}}
    Output: {{"step": "action", "function": "add", "input": {"x":4637, "y": 2332}}}
    Output: {{"step": "observe", "output": "6969"}}
    Output: {{"step": "output", "content": "The additon of 4637 + 2332 is 6969"}}
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