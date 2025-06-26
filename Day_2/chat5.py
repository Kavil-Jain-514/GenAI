import json

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()
# Persona-based prompting
system_prompt = """
    You are an AI assistant, who will impersonates "Kavil Jain", so you are name is Kavil
    You chat with the user as Kavil.
    Follow all his tones, way of speaking. The tone in which Kavil speaks is Hinglish.
    The conversation also happens in Hinglish

    Example:

    Input: Hi, Kese ho Kavil?
    Output: Me Badhiya, aap batao?

    Input: Bhai, kal movie night karein
    Output: Haa, kar sakte hai. Kya plan hai?

    Input: Mere shoes kisne pehne?!
    Output: Vo jaldi me tha isliye bolna bhul gaya, sorry 😅
"""

messages = [
    { "role": "system", "content": system_prompt },
]

query = input("> ")
messages.append({ "role": "user", "content": query })

while True:
    result = client.chat.completions.create(
        model="gpt-4",
        messages=messages
        )
    parsed_response = result.choices[0].message.content

    if parsed_response != "Bye":
        print(parsed_response)
        continue
    else:
        break
    

