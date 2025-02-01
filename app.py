import streamlit as st

import plotly.graph_objects as go
import yfinance as yf
from phi.agent.agent import Agent
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.googlesearch import GoogleSearch

from styles import style

COMMON_STOCKS = {
    'NVIDIA': 'NVDA', 'APPLE': 'AAPL', 'GOOGLE': 'GOOGL', 'MICROSOFT': 'MSFT',
    'TESLA': 'TSLA', 'AMAZON': 'AMZN', 'META': 'META', 'NETFLIX': 'NFLX',
    'TCS': 'TCS.NS', 'RELIANCE': 'RELIANCE.NS', 'INFOSYS': 'INFY.NS',
    'WIPRO': 'WIPRO.NS', 'HDFC': 'HDFCBANK.NS', 'TATAMOTORS': 'TATAMOTORS.NS',
    'ICICIBANK': 'ICICIBANK.NS', 'SBIN': 'SBIN.NS'
}

st.set_page_config(page_title="Stocks Analysis AI Agents", page_icon="", layout="wide")

st.markdown(style, unsafe_allow_html=True)


def initialize_agents():
    if 'first_time' not in st.session_state:
        try:
            st.session_state.web_agent = Agent(
                name="Web Search Agent",
                role="Search the web for information",
                model=Groq(),
                tools=[GoogleSearch(fixed_max_results=5), DuckDuckGo(fixed_max_results=5)]
            )
            st.session_state.finance_agent = Agent(
                name="Financial AI Agent",
                role="Providing financial insights",
                model=Groq(),
                tools=[YFinanceTools()]
            )
            st.session_state.multi_ai_agent = Agent(
                name='Stock Market Agent',
                role='Stock market analysis specialist',
                model=Groq(),
                team=[st.session_state.web_agent, st.session_state.finance_agent]
            )
            st.session_state.agents_initialized = True
            return True
        except Exception as e:
            st.error(f"Agent initialization error: {str(e)}")
            return False
    st.session_state.first_time = True


def get_stock_data(symbol):
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        hist = stock.history(period="1y")
        return info, hist
    except Exception as e:
        st.error(f"Error fetching data: {str(e)}")
        return None, None


def create_price_chart(hist_data, symbol):
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=hist_data.index, open=hist_data['Open'],
        high=hist_data['High'], low=hist_data['Low'],
        close=hist_data['Close'], name='OHLC'
    ))
    fig.update_layout(
        title=f'{symbol} Price Movement',
        template='plotly_white',
        xaxis_rangeslider_visible=False,
        height=500
    )
    return fig


def main():

    st.title("Stocks Analysis AI Agents")

    stock_input = st.text_input("Enter Company Name", help="e.g., APPLE, TCS")

    if st.button("Analyze", use_container_width=True):
        if not stock_input:
            st.error("Please enter a stock name")
            return

        symbol = COMMON_STOCKS.get(stock_input.upper()) or stock_input

        if initialize_agents():
            with st.spinner("Analyzing..."):
                info, hist = get_stock_data(symbol)

                if info and hist is not None:
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.markdown(
                            f"<div class='card'><div class='metric-value'>${info.get('currentPrice', 'N/A')}</div><div class='metric-label'>Current Price</div></div>",
                            unsafe_allow_html=True)
                    with col2:
                        st.markdown(
                            f"<div class='card'><div class='metric-value'>{info.get('forwardPE', 'N/A')}</div><div class='metric-label'>Forward P/E</div></div>",
                            unsafe_allow_html=True)
                    with col3:
                        st.markdown(
                            f"<div class='card'><div class='metric-value'>{info.get('recommendationKey', 'N/A').title()}</div><div class='metric-label'>Recommendation</div></div>",
                            unsafe_allow_html=True)

                    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
                    st.plotly_chart(create_price_chart(hist, symbol), use_container_width=True)


                    if 'longBusinessSummary' in info:
                        st.markdown("<div class='card'>", unsafe_allow_html=True)
                        st.markdown("### Company Overview")
                        st.write(info['longBusinessSummary'])
                        st.markdown("</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
