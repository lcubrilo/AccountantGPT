from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()  # This loads the variables from .env

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
      {"role": "user", "content": "Hello, world!"}
  ]
)
print(response.choices[0].message.content)