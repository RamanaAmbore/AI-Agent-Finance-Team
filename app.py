import os

import streamlit as st
from phi.agent import Agent
from phi.model.groq import Groq
from phi.model.xai import xAI
from phi.storage.agent.sqlite import SqlAgentStorage
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.yfinance import YFinanceTools

from constants import groq_help_text, grok_help_text, query_help_text, default_query, agent_help_text, \
    agent_code_map, xai_model_id, groq_model_id, hover_text

# Load environment variables
# from dotenv import load_dotenv
# load_dotenv()

if "groq_api_key" not in st.session_state or "xai_api_key" not in st.session_state:
    st.session_state.groq_api_key = ""
    st.session_state.xai_api_key = ""
    # Initialize Agents with Updated API Keys
    st.session_state.web_agent = Agent(
        name="Web Agent",
        role="Searching the web for real-time information about companies and public sentiment.",
        model=Groq(id=f"{groq_model_id}"),
        tools=[DuckDuckGo()],
        storage=SqlAgentStorage(table_name="web_agent", db_file="agents.db"),
        add_history_to_messages=False,
        markdown=True,
        instructions=[
            "Search for the latest news articles, social media trends, and public discussions related to the user's query.\n" +
            "Respond in JSON format only, no additional text, don't summarize the event impact, list down individual events and impact" +
            "{['symbol': 'The company stock ticker','score': Impact estimation (-10 to +10) based on the company stock price.,'event_summary': 'A brief description of the event.'}]}"],
    )

    st.session_state.finance_agent = Agent(
        name="Finance Agent",
        role="Accessing and analyzing financial data and trends from structured finance databases.",
        model=Groq(id=f"{groq_model_id}"),
        tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, company_info=True, company_news=True)],
        storage=SqlAgentStorage(table_name="finance_agent", db_file="agents.db"),
        add_history_to_messages=False,
        markdown=False,
        instructions=[
            "Use financial tools (e.g., Yahoo Finance) to gather stock prices, company-specific news, and analyst recommendations.\n" +
            "Respond in JSON format only, no additional text:\n" +
            "{['symbol': 'The company stock ticker','score': Impact estimation (-10 to +10) based on the company stock price.,'event_summary': 'Include quantitative data relevant to the user query.'}]}"],
    )

    st.session_state.grok_agent = Agent(
        name="Grok Agent",
        role="Combining web search and X.com data.",
        model=xAI(id="grok-beta"),
        tools=[DuckDuckGo()],
        storage=SqlAgentStorage(table_name="grok_agent", db_file="agents.db"),
        markdown=False,
        instructions=[
            "Use both web tools and x.com public tweets to gather a comprehensive view of trends, and sentiment.\n" +
            "Respond in JSON format only, no additional text:\n" +
            "{['symbol': 'The company stock ticker','score': Impact estimation (-10 to +10) based on the event's likely effect on the company stock price.,'event_summary': 'Combine news and data.'}]}"],
    )

    st.session_state.agent_team = Agent(
        team=[st.session_state.web_agent, st.session_state.finance_agent, st.session_state.grok_agent],
        name="Agents Team",
        role="Orchestrating tasks across specialized agents to produce the most accurate and comprehensive responses.",
        markdown=False,
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
    )

    st.session_state.agent_map = {
        "Web Agent": st.session_state.web_agent,
        "Finance Agent": st.session_state.finance_agent,
        "Grok Agent": st.session_state.grok_agent,
        "Agents Team": st.session_state.agent_team,
    }
    st.session_state.user_query_key = default_query

    st.session_state.agent_selection_key = "Web Agent"

# Set the page configuration
st.set_page_config(
    page_title="AI LLM Agent Demo by Ramana Rao Ambore, FRM",  # Title of the page
    page_icon=":robot:",  # Favicon (can use emoji or image path)
    layout="wide",  # "centered" or "wide"
    initial_sidebar_state="expanded",  # "auto", "expanded", or "collapsed"
)

st.title("AI LLM Agent Demo by Ramana Rao Ambore, FRM")
st.write("Interact with your AI agents to get financial data and web search results.")

st.text_input("Enter Groq API Key",
              key="groq_api_key",
              type="password",
              help=groq_help_text)
st.text_input("Enter xAI (Grok) API Key",
              key="xai_api_key",
              type="password",
              help=grok_help_text)

# User input
st.text_input("Enter your query:",
              key="user_query_key",
              help=query_help_text)
st.selectbox("Select an Agent",
             ["Web Agent", "Finance Agent", "Grok Agent", "Agents Team"],
             key="agent_selection_key",
             help=agent_help_text)

if st.button("Submit Query"):
    if st.session_state.groq_api_key == "" or st.session_state.xai_api_key == "":
        st.warning("Please enter the api keys before submitting.")
    elif st.session_state.user_query_key.strip() == "":
        st.warning("Please enter a query before submitting.")
    else:
        os.environ["GROQ_API_KEY"] = st.session_state.groq_api_key
        os.environ["XAI_API_KEY"] = st.session_state.xai_api_key
        os.environ["OPENAI_API_KEY"] = st.session_state.xai_api_key
        selected_agent = st.session_state.agent_map[st.session_state.agent_selection_key]
        selected_agent_code = agent_code_map[st.session_state.agent_selection_key]


        # Wrap selected_agent_code in a div with class 'hover-box'
        st.markdown(selected_agent_code, unsafe_allow_html=True)

        # Wrap selected_agent_code in a div with class 'hover-box'
        st.markdown(hover_text, unsafe_allow_html=True)

        # st.write(selected_agent)
        selected_agent.print_response(st.session_state.user_query_key)


        response = selected_agent.run(st.session_state.user_query_key, temperature=0.0, max_tokens=10, top_p=0.5,
                                      frequency_penalty=0.8)
        st.write("Agent's Response:")

        st.write(response.content)
