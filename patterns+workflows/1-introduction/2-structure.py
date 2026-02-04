import os
from groq import Groq
import json
from pydantic import BaseModel


client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# Define Pyndantic Models
class KeyPhrase(BaseModel):
    phrase: str
    sentiment: str


class SentimentAnalysis(BaseModel):
    sentiment: str
    confidence_score: float
    key_phrases: list[KeyPhrase]
    summary: str


# Call the Model

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {
            "role": "system",
            "content": """You are a data analysis API that performs sentiment analysis on text.
                Respond only with JSON using this format:
                {
                    "sentiment_analysis": {
                    "sentiment": "positive|negative|neutral",
                    "confidence_score": 8,2 ,
                    "key_phrases": [
                        {
                        "phrase": "detected key phrase",
                        "sentiment": "positive|negative|neutral"
                        }
                    ],
                    "summary": "One sentence summary of the overall sentiment"
                    }
                }""",
        },
        {
            "role": "user",
            "content": "Analyze the sentiment of this customer review: 'I absolutely love this product! The quality exceeded my expectations, though shipping took longer than expected.'",
        },
    ],
    response_format={"type": "json_object"},
)

# Parse
data = json.loads(response.choices[0].message.content)
result = SentimentAnalysis(**data["sentiment_analysis"])


print(result.confidence_score)
print(result.sentiment)
print(result.summary)
print(result.key_phrases)
