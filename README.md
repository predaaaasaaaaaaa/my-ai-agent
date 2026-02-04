# 🤖 AI Customer Support Agent

An intelligent customer support assistant built with Python and the Groq API that analyzes customer sentiment and feedback for online store products using function calling.

## ✨ Features

- 🔍 **Sentiment Analysis** - Automatically analyzes customer feedback and ratings
- 🎯 **Smart Function Calling** - LLM intelligently decides when to use tools
- 📊 **Detailed Metrics** - Provides average ratings, sentiment breakdown, and sample comments
- ⚡ **Powered by Groq** - Fast inference using Llama 3.3 70B model
- 🛠️ **Pure Python** - Built from scratch without heavyweight frameworks

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Groq API Key ([Get one here](https://console.groq.com))

### Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/ai-customer-support-agent.git
cd ai-customer-support-agent
```

2. Install dependencies
```bash
pip install groq
```

3. Set up your Groq API key
```bash
# Windows
set GROQ_API_KEY=your_api_key_here

# macOS/Linux
export GROQ_API_KEY=your_api_key_here
```

### Usage

Run the agent:
```bash
python main.py
```

Example interaction:
```python
question = "How are customers feeling about our new keyboard?"
answer = run_customer_support_agent(question)
print(answer)
```

## 📁 Project Structure
```
ai-customer-support-agent/
│
├── main.py                 # Main agent logic with function calling
├── feedbacks.py           # Customer feedback data storage
└── README.md             # You are here!
```

## 🎯 How It Works

1. **User asks a question** about product sentiment
2. **LLM decides** if it needs to call the sentiment analysis function
3. **Python executes** the function, analyzing real feedback data
4. **Results are sent back** to the LLM
5. **LLM generates** a natural language response based on the data

### Function Calling Flow
```
User Query → LLM → Tool Call Request → Python Function → Data Analysis → LLM → Final Answer
```

## 🔧 Configuration

### Supported Models

The agent uses Groq's models that support function calling:

- `llama-3.3-70b-versatile` (Recommended)
- `llama-3.1-70b-versatile`
- `llama-3.1-8b-instant`
- `mixtral-8x7b-32768`

Change the model in `main.py`:
```python
model="llama-3.3-70b-versatile"
```

### Adjusting Response Length

Modify `max_tokens` for longer/shorter responses:
```python
max_tokens=4096  # Detailed responses
max_tokens=1024  # Medium responses
max_tokens=512   # Short responses
```

## 📊 Example Output
```
🤔 User asked: How are customers feeling about our new keyboard?

🔧 LLM decided to use a tool!

📞 LLM wants to call: analyze_product_sentiment
📝 With parameters: {'product_name': 'keyboard'}

✅ Function returned:
{
  "product": "keyboard",
  "total_feedbacks": 4,
  "average_rating": 4.0,
  "sentiment_breakdown": {
    "positive": 3,
    "neutral": 0,
    "negative": 1
  }
}

🤖 Sending results back to LLM for final answer...

FINAL ANSWER:
Based on customer feedback, the keyboard is receiving mostly positive 
reviews with an average rating of 4.0 out of 5 stars. Out of 4 total 
feedbacks, 3 are positive and 1 is negative. Customers love the smooth 
typing experience and excellent build quality, though one customer 
mentioned concerns about key feel and noise level.
```

## 🛠️ Adding New Products

Add feedback in `feedbacks.py`:
```python
CUSTOMER_FEEDBACKS = [
    {
        "product": "your_product_name",
        "rating": 5,
        "comment": "Customer feedback here",
        "date": "2024-01-15"
    },
    # Add more...
]
```

## 🤝 Contributing

Contributions are welcome! Feel free to:

- 🐛 Report bugs
- 💡 Suggest new features
- 🔧 Submit pull requests

## 🙏 Acknowledgments

- Built with [Groq](https://groq.com) - Lightning-fast LLM inference
- Powered by Meta's Llama 3.3 model
- Inspired by modern AI agent architectures


⭐ If you found this project helpful, please give it a star!