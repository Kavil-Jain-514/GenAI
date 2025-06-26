import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

# Self cosistency prompting
# One word or number can have different meaning in English language.
# So based on the context and meaning of the sentence, we get different response.
system_prompt = """
    You are AI assitant, who is expert in differentiating meaning of the same words or numbers based on the context of the sentence provided by the user.
    
    Example:
    Input: Which is greater? 9.8 or 9.11?
    Output: 9.8 is greater.

    Input: Which chapter in the book is greater, 9.8 or 9.11?
    Output: 9.11 is greater.

"""
result = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "system", "content": system_prompt},
              {"role": "user", "content": "Which chapter of book is greater 5.11 or 5.3?"}
            ]
    )

print(result.choices[0].message.content)