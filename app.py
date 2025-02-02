from phi.agent import Agent

from phi.storage.agent.sqlite import SqlAgentStorage
from dotenv import load_dotenv
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.yfinance import YFinanceTools
import streamlit as st
load_dotenv()
from phi.model.groq import Groq
from phi.model.xai import xAI

web_agent = Agent(
        name="Web Agent",
        role="Searching the web for real-timeabout companies, and public sentiment.",
        model=Groq(id="llama-3.3-70b-versatile"),
        tools=[DuckDuckGo()],
        instructions=["Search for the latest news articles, social media trends, and public discussions related to the user's query.\n" +
                    "Respond in JSON format only, no additional text" +
                    "{['symbol': 'The company stock ticker','score': Impact estimation (-10 to +10) based on the company stock price.,'event_summary': 'A brief description of the event.'}]}"],
        storage=SqlAgentStorage(table_name="web_agent", db_file="agents.db"),
        add_history_to_messages=False,
        markdown=False,
    )


finance_agent = Agent(
        name="Finance Agent",
        role="Accessing and analyzing financial data and trends from structured finance databases.",
        model=Groq(id="llama-3.3-70b-versatile"),
        tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, company_info=True, company_news=True)],
        instructions=["Use financial tools (e.g., Yahoo Finance) to gather stock prices, company-specific news, and analyst recommendations.\n" +
                    "Respond in JSON format only, no additional text:\n" +
                    "{['symbol': 'The company stock ticker','score': Impact estimation (-10 to +10) based on the company stock price.,'event_summary': 'Include quantitative data relevant to the user query.'}]}"],
        storage=SqlAgentStorage(table_name="finance_agent", db_file="agents.db"),
        add_history_to_messages=False,
        markdown=False,
    )

grok_agent = Agent(
        name="Grok Agent",
        role="Combining web search and x.com data.",
        model=xAI(id="grok-beta"),
        tools=[DuckDuckGo()],
        instructions=["Use both web tools and x.com public tweets to gather a comprehensive view of trends, and sentiment.\n" +
                    "Respond in JSON format only, no additional text:\n" +
                    "{['symbol': 'The company stock ticker','score': Impact estimation (-10 to +10) based on the event's likely effect on the company stock price.,'event_summary': 'Combine news and data.'}]}"],
        show_tool_calls=False,
        markdown=False,
    )

agent_team = Agent(
        team=[web_agent, finance_agent, grok_agent],
        name="Agents Team",
        role="Orchestrating tasks across specialized agents to produce the most accurate and comprehensive responses.",
        instructions=["Delegate tasks based on prompt requirements:\n" +
                    "Web Agent: For real-time news and sentiment analysis.\n" +
                    "Finance Agent: For financial data and analytics.\n" +
                    "Grok Agent: For tunring insights into a well-structured response.\n" +
                    "Respond in JSON format only, no additional text:\n" +
                    "{\n" +
                    '   "symbol": "TICKER",\n' +
                    '   "score": NUMBER_BETWEEN_NEGATIVE_10_AND_10,\n' +
                    '   "event_summary": "SUMMARY",\n' +
                    '   "analysis": {\n' +
                    '       "web_insights": "WEB_FINDINGS",\n' +
                    '       "financial_data": "FINANCIAL_METRICS",\n' +
                    '       "combined_web_analysis": "SYNTHESIS"\n' +
                    "    }\n" +
                    "}\n" +
                    "Deduplicate or reconcile overlapping findings.\n" +
                    "Provide a clear, actionable summary for the user."],
        show_tool_calls=False,
        markdown=False,
    )

# Streamlit App
st.title("AI Agent Finance Team")
st.write("Interact with your AI agents to get financial data and web search results.")

# User input
user_query = st.text_input("Enter your query:")

# Dropdown to select the agent
agent_selection = st.selectbox(
    "Select an Agent",
    options=["Web Agent", "Finance Agent", "Grok Agent", "Agents Team"],
)

# Agent map
agent_map = {
    "Web Agent": web_agent,
    "Finance Agent": finance_agent,
    "Grok Agent": grok_agent,
    "Agents Team": agent_team,
}
# monitor announcments of new tech products and which are generating buzz today
if st.button("Submit Query"):
    if user_query.strip():
        selected_agent = agent_map[agent_selection]
        # prompt = agent_team.generate_prompt(selected_agent.name, user_query)
        response = selected_agent.run(user_query)
        print(response)

        try:
            # Process response and send to Discord
            # response_content = agent_team.process_and_send_response(
            #     response,
            #     selected_agent.name
            # )

            # Debug: Show extracted text
            st.write("Extracted text:")
            st.write(response)

            # Show Discord status
            st.success("Results sent to Discord successfully!")

        except Exception as e:
            st.error(f"Error processing response: {str(e)}")
            st.text("Raw response:")
            st.text(response)
    else:
        st.warning("Please enter a query before submitting.")