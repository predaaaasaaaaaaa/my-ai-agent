import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

completion = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "system", "content": "You're a helpful assistant."},
        {
            "role": "user",
            "content": "Write a Limerick about the Python programming Language.",
        },
    ],
)

response = completion.choices[0].message.content
print(response)
