from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()
# Zero Shot Prompting
# Direct, simple tone, simple conversation, questions.
# No pre-context or System prompt given to the model.
result = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "user", "content": "What is up?"}
    ]
)

print(result.choices[0].message.content)