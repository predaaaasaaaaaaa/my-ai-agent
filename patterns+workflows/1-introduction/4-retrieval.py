import json
import os

from groq import Groq
from pydantic import BaseModel, Field

client = Groq(api_key=os.getenv("GROQ_QPI_KEY"))

"""
docs: https://console.groq.com/docs/tool-use/overview#3-local-tool-calling-function-calling
"""

# Defining the knowledge base retrieval tool


def search_kb(queston: str):
    """
    Load the whole knowledge base from the JSON file
    (This is a mock function for demonstastion purposes)
    """
    with open("kb.json", "r") as f:
        return json.load(f)


# Step 1: Call model with search_kb tool defined

tools = [
    {
        "type": "function",
        "function": {
            "name": "search_kb",
            "description": "Get the answer to the user's question from the knowledge base",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {"type": "string"},
                },
                "strict": True,
            },
        },
    }
]

system_prompt = "You are a helpful assistant that answers questions from the knowledge base about our e-commerce store."

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": "What is the return policy?"},
]

completion = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=messages,
    tools=tools,
)


# Step 2: Model decides to call function(s)

completion.model_dump()


# Step 3: Execute 'search_kb' function


def call_function(name, args):
    if name == "search_kb":
        return search_kb(**args)


for tool_call in completion.choices[0].message.tool_calls:
    name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)
    messages.append(completion.choices[0].message)

    result = call_function(name, args)
    messages.append(
        {"role": "tool", "tool_call_id": tool_call.id, "content": json.dumps(result)}
    )


# Step 4: Supply result and call model again
