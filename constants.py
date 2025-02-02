groq_help_text = """ 
The key is masked for security purposes.    
## Groq API Key
To obtain a Groq API key, visit the following link:
- [Groq Developer Console](https://console.groq.com/login)

For detailed instructions, refer to the [Groq Quickstart Guide](https://console.groq.com/docs/quickstart).
"""
grok_help_text = """
The key is masked for security purposes. 
## Grok API Key
To obtain a Grok API key, visit the following link:
- [xAI API Page (Grok)](https://x.ai/api)

For a step-by-step guide, check out:
- [How to Get Your Grok API Key](https://www.merge.dev/blog/grok-api-key).
"""

groq_model_id = "llama-3.3-70b-versatile"
xai_model_id = "grok-beta"

web_agent_code = f"""
## Web Agent Python Code:
```
web_agent_text = Agent(
    name="Web Agent",
    role="Searching the web for real-time information about companies and public sentiment.",
    model=Groq(id="{groq_model_id}"),
    tools=[DuckDuckGo()],
    storage=SqlAgentStorage(table_name="web_agent", db_file="agents.db"),
    add_history_to_messages=False,
    markdown=False

)
```
"""



finance_agent_code = f"""
Finance Agent Python Code:
```
Agent(
    name="Finance Agent",
    role="Accessing and analyzing financial data and trends from structured finance databases.",
    model=Groq(id="{groq_model_id}"),
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, company_info=True, company_news=True)],
    storage=SqlAgentStorage(table_name="finance_agent", db_file="agents.db"),
    add_history_to_messages=False,
    markdown=False,
)
```
"""

grok_agent_code = f"""
Grok Agent Python Code:
```
Agent(
    name="Grok Agent",
    role="Combining web search and X.com data.",
    model=xAI(id="{xai_model_id}"),
    tools=[DuckDuckGo()],
    storage=SqlAgentStorage(table_name="grok_agent", db_file="agents.db"),
    markdown=False,
)
```
"""
agent_team_code = f"""
Agents Team Python Code:
```
web_agent_text = Agent(
    name="Web Agent",
    role="Searching the web for real-time information about companies and public sentiment.",
    model=Groq(id="{groq_model_id}"),
    tools=[DuckDuckGo()],
    storage=SqlAgentStorage(table_name="web_agent", db_file="agents.db"),
    add_history_to_messages=False,
    markdown=False,
)

finance_agent = Agent(
    name="Finance Agent",
    role="Accessing and analyzing financial data and trends from structured finance databases.",
    model=Groq(id="{groq_model_id}"),
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, company_info=True, company_news=True)],
    storage=SqlAgentStorage(table_name="finance_agent", db_file="agents.db"),
    add_history_to_messages=False,
    markdown=False,
)

grok_agent = Agent(
    name="Grok Agent",
    role="Combining web search and X.com data.",
    model=xAI(id="{xai_model_id}"),
    tools=[DuckDuckGo()],
    storage=SqlAgentStorage(table_name="grok_agent", db_file="agents.db"),
    markdown=False,
)

agent_team = Agent(
    team=[web_agent, finance_agent, grok_agent],
    name="Agents Team",
    role="Orchestrating tasks across specialized agents.",
    markdown=False,
)
```
"""
default_query = "monitor major announcements from ntt group companies"
query_help_text = "Type the query you want to ask"
agent_help_text = "Select the web agent, finance agent, grok agent or agent team to run the query"

hover_text="""
## Explanation:

- **name**: Agent's name.  
  - **Value**: `"Web Agent"` (Handles web searches).  

- **role**: Agent’s function.  
  - **Value**: `"Searching the web for real-time info on companies & sentiment."`  

- **model**: LLM used.  
  - **Value**: `Groq(id=f"{groq_model_id}")` (Uses Groq’s Llama model).  

- **tools**: External tools.  
  - **Value**: `[DuckDuckGo()]` (Uses DuckDuckGo for web searches).  

- **storage**: Data storage. Specifies how the agent stores data for long-term memory and future reference. 
  - **Value**: `SqlAgentStorage("web_agent", "agents.db")` (Saves data in SQLite).  

- **add_history_to_messages**: Determines whether the agent retains chat history for use in future interactions, allowing it to remember context and provide more coherent, personalized responses over time.  
  - **Value**: `False` (No memory retained).  

- **markdown**: Determines whether the agent uses Markdown formatting in its responses, allowing for enhanced text formatting such as headings, bold text, and links.
  - **Value**: `True` (Markdown enabled).  

- **instructions**: Provides specific guidance or rules that define how the agent should approach and handle tasks. These instructions direct the agent’s behavior and output, ensuring that it processes information according to the intended workflow or logic.  
  - **Value**: `["Search for news & sentiment, return JSON: {'symbol': 'Ticker', 'score': Impact (-10 to 10), 'event_summary': 'Brief event desc'}"]` 
"""

agent_code_map = {
    "Web Agent": web_agent_code,
    "Finance Agent": finance_agent_code,
    "Grok Agent": grok_agent_code,
    "Agents Team": agent_team_code,
}


