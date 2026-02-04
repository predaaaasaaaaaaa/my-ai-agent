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
