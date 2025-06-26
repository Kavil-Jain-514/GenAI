from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

# Few Shot Prompting
# Contains few system prompts, or context or instructions or examples.
# Writing examples gives better results
system_prompt = """
    You are an AI assistant whose name is Aryan and performs only mathematical questions.
    For any other question reply with Baigan

    Examples:
    Input: What is 2 + 2
    Output: 4

    Input: What is the color of Sky?
    Output: Baigan
"""
result = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "system", "content": system_prompt},
              {"role": "user", "content": "What is corn?"}
            ]
    )

print(result.choices[0].message.content)