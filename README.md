# AI Agent Finance Team

## Overview
The **AI Agent Finance Team** is a **Streamlit-based web application** that enables users to interact with multiple AI agents specializing in **web search, financial analysis, and sentiment tracking**. The agents utilize **PhiData's AI framework** along with models like **Groq and xAI (Grok)** to gather and process real-time insights about companies, stock prices, and financial trends.

## Features
✅ **Web Search Agent**: Fetches real-time news and public sentiment using **DuckDuckGo**.  
✅ **Finance Agent**: Retrieves **stock prices, analyst recommendations, and financial reports** using **Yahoo Finance tools**.  
✅ **Grok Agent**: Combines web and social media insights (X.com/Twitter) to analyze trends and market sentiment.  
✅ **AI Agent Team**: **Orchestrates** all agents to generate a **comprehensive response** with actionable insights.  
✅ **JSON Response Format**: Ensures structured, machine-readable output.  
✅ **Interactive Streamlit UI**: Allows users to select agents and run queries effortlessly.  
✅ **Discord Integration (Future)**: Sends AI-generated insights directly to **Discord**.  

## Installation
### 1️⃣ **Clone the Repository**
```sh
git clone https://github.com/your-repo/ai-agent-finance-team.git
cd ai-agent-finance-team
```

### 2️⃣ Set Up Virtual Environment (Optional but Recommended)
```
python -m venv venv
source venv/bin/activate   # On macOS/Linux
venv\Scripts\activate     # On Windows
```
### 3️⃣ Install Dependencies
```
pip install -r requirements.txt
```
### 4️⃣ Set Environment Variables

Create a .env file in the root directory and add:
```
GROQ_API_KEY=your_groq_api_key_here
```
Alternatively, set it in your system:
```
export GROQ_API_KEY=your_groq_api_key_here  # macOS/Linux
set GROQ_API_KEY=your_groq_api_key_here      # Windows
```
## Usage

### Run the Streamlit App
```
streamlit run app.py
```
### Interact with the Agents

Enter your query in the text input field.

Select an AI Agent from the dropdown (Web Agent, Finance Agent, Grok Agent, or Agent Team).

Click Submit Query to fetch insights.

View JSON-formatted results in the app.

## API Agents Overview

### 1️⃣ Web Agent

Searches the web for real-time news & public sentiment.

Returns a structured JSON response with impact scores & event summaries.

### 2️⃣ Finance Agent

Fetches financial data using Yahoo Finance tools.

Provides stock prices, company news, analyst recommendations, and more.

### 3️⃣ Grok Agent

Leverages xAI’s Grok model to combine web and social media insights.

Analyzes trending discussions & evaluates potential market impact.

### 4️⃣ Agent Team

Orchestrates all three agents for a unified financial + web + social media analysis.

Deduplicates, structures data, and provides a final comprehensive report.

## Example Query

What are the latest analyst recommendations for NVDA?

### Example Response (JSON)

{
    "symbol": "NVDA",
    "score": 7.5,
    "event_summary": "Strong buy rating from analysts with a 15% price target increase.",
    "analysis": {
        "web_insights": "Recent bullish sentiment across financial news portals.",
        "financial_data": "Stock price surged 3% after earnings report.",
        "combined_web_analysis": "Positive outlook due to AI chip demand increase."
    }
}

## Future Enhancements

- 🚀 Real-time Stock Charts using Plotly
- 🚀 Sentiment Analysis Score Visualization
- 🚀 Integration with Discord for Instant Alerts
- 🚀 Automated Market Trend Predictions

## Contributors

- Ramana Ambore (@RamanaAmbore)

## License

This project is licensed under the MIT License.

