from dotenv import load_dotenv
from openai import OpenAI

load_dotenv('../.env')

text = "The cat sat on the mat"

client = OpenAI()

response = client.embeddings.create(input=text, model='text-embedding-3-small')

print("Vector Embeddings", response.data[0].embedding)

