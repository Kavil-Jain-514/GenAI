from google import genai
from google.genai import types


client = genai.Client(api_key='AIzaSyCUswQMHicwDi8XxuDnOBhrUvw-QEFG53Q')

#Zero Shot Prompting

respone = client.models.generate_content(model='gemini-2.0-flash-001', contents="Why is blood red?")
print(respone.text)