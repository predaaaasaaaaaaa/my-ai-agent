import json
import os
from groq import Groq
from feedbacks import CUSTOMER_FEEDBACKS

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# 1 Defining the Tool (function) that i want to call
def analyze_product_sentiment(product_name):
    """
    This function YOU execute when the LLM asks for it.
    It reads feedback data and returns sentiment analysis.
    """
    # Filter feedbacks for the specific product
    product_feedbacks = [
        fb for fb in CUSTOMER_FEEDBACKS if fb["product"].lower() == product_name.lower()
    ]
    if not product_feedbacks:
        return {
            "product": product_name,
            "status": "no_data",
            "message": f"No feedback fount for {product_name}",
        }
    # Calculate sentiment metrics
    total_feedbacks = len(product_feedbacks)
    average_rating = sum(fb["rating"] for fb in product_feedbacks) / total_feedbacks

    # Categorize sentiments
    positive = sum(1 for fb in product_feedbacks if fb["rating"] >= 4)
    neutral = sum(1 for fb in product_feedbacks if fb["rating"] == 3)
    negative = sum(1 for fb in product_feedbacks if fb["rating"] >= 2)

    # Get sample comments
    recent_comments = [fb["comment"] for fb in product_feedbacks[:3]]

    return {
        "product": product_name,
        "total_feedbacks": total_feedbacks,
        "average_rating": round(average_rating, 2),
        "sentiment_breakdown": {
            "positive": positive,
            "neutral": neutral,
            "negative": negative,
        },
        "sample_comments": recent_comments,
    }


# Tool definition - This is what the LLM sees

tools = [
    {
        "type": "function",
        "function": {
            "name": "analyze_product_sentiment",
            "description": "Analyzes customer sentiment and feedback for a specific product. Returns rating statistics, sentiment breakdown, and sample customer comments.",
            "parameters": {
                # JSON Schema object
                "type": "object",
                "properties": {
                    "product_name": {
                        "type": "string",
                        "description": "The name of the product to analyze (e.g., 'keyboard', 'mouse')",
                    },
                },
                "required": ["product_name"],
            },
        },
    }
]

# The complete agent loop


def run_customer_support_agent(user_question):
    """
    Main function that handles the conversation with funcion calling
    """
    # Initial messages
    messages = [
        {
            "role": "system",
            "content": "You are a helpful customer support assistant for an online store. When asked about customer feedback or sentiment, use the analyze_product_sentiment function to get accurate data. Provide friendly, informative responses based on the data.",
        },
        {"role": "user", "content": user_question},
    ]

    # Step 1: Sent initial requests to LLM with tools available
    print(f"\n User asked: {user_question}\n")

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        tools=tools,
        tool_choice="auto",  # Let the LLM decides if it needs a tool
        max_tokens=1024,
    )

    response_message = response.choices[0].message

    # Step 2: Check if the LLM wants to call a function
    if response_message.tool_calls:
        print("LLM decided to use a tool! \n")

        # Add the LLM's response to messages
        messages.append(response_message)

        # Step 3: Execute each tool call the LLM requested
        for tool_call in response_message.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)

            print(f"LLM wants to call {function_name}")
            print(f"With parameters {function_args}")

            # Step 4: YOU execute the actual function
            if function_name == "analyze_product_sentiment":
                function_response = analyze_product_sentiment(
                    product_name=function_args.get("product_name")
                )
            else:
                function_response = {"error": "Funtion not found!"}

            print(f"Function returned {json.dumps(function_response, indent=2)}\n")

            # Step 5: Add function result back to messages
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": function_name,
                    "content": json.dumps(function_response),
                }
            )

        # Step 6: Send function results back to LLM
        print("Sending results back to LLM for final answer...\n")

        final_response = client.chat.completions.create(
            model="llama-3.3-70b-versatile", messages=messages, max_tokens=1024
        )

        final_answer = final_response.choices[0].message.content

    else:
        # LLM didn't need to use a Tool, it answers directly
        print("LLM answered directly without using tools\n")

        final_answer = response_message.content

    return final_answer


# Example Usage
if __name__ == "__main__":
    # TEST THE AGENT
    question = "How are customers feeling about our keyboard?"
    answer = run_customer_support_agent(question)

    print("=" * 60)
    print("FINAL ANSWER:")
    print("=" * 60)
    print(answer)
