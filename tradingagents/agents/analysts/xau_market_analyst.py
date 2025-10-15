from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from tradingagents.agents.utils.agent_utils import get_stock_data, get_indicators

def create_xau_market_analyst(llm):
    """
    Creates a node for the XAU Market Analyst agent.
    
    This agent analyzes technical patterns and price action for gold (XAU/USD).
    It focuses on chart patterns, support/resistance levels, and technical indicators
    specific to gold trading.
    """
    
    system_message = (
        "You are a specialized Technical Market Analyst for Gold (XAU/USD). Your mission is to provide detailed technical analysis of gold's price action. "
        "Focus exclusively on the following:"
        "\n\n1. **Trend Analysis**: Analyze the trend using moving averages (50 SMA, 200 SMA, 10 EMA). Is gold in an uptrend, downtrend, or range-bound? "
        "Identify key support and resistance levels."
        "\n2. **Momentum Indicators**: Use RSI to identify overbought (>70) or oversold (<30) conditions. Use MACD for trend strength and potential reversals."
        "\n3. **Volatility Analysis**: Analyze Bollinger Bands for volatility and potential breakouts. Use ATR to assess current volatility levels for risk management."
        "\n4. **Price Patterns**: Identify any significant chart patterns (e.g., double tops/bottoms, triangles, head and shoulders) that may indicate future direction."
        "\n\nFor gold trading, pay special attention to:"
        "- Key psychological levels ($1,800, $1,900, $2,000, etc.)"
        "- Previous all-time highs as resistance"
        "- Long-term moving averages as dynamic support/resistance"
        "\n\nUse the available tools to fetch price data and calculate indicators. First call get_stock_data to retrieve the historical price CSV, "
        "then call get_indicators with specific indicator names (e.g., 'close_50_sma', 'rsi', 'macd', 'boll', 'atr')."
        "\n\nSynthesize your findings into a comprehensive technical report. "
        "Conclude with a Markdown table summarizing the key technical factors and their implications (Bullish, Bearish, or Neutral)."
    )
    
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a helpful AI assistant, collaborating with other assistants."
                " Use the provided tools to progress towards answering the question."
                " The asset of interest is Gold (XAU/USD)."
                " For your reference, the current date is {current_date}."
                "\n\nTool Names: {tool_names}"
                "\n\n{system_message}",
            ),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )
    
    tools = [
        get_stock_data,
        get_indicators,
    ]
    
    prompt = prompt.partial(
        system_message=system_message,
        tool_names=", ".join([tool.name for tool in tools]),
    )
    
    chain = prompt | llm.bind_tools(tools)
    
    def xau_market_analyst_node(state):
        """
        The node function for the XAU Market Analyst.
        """
        current_date = state["trade_date"]
        # Use the ticker from state (e.g., "GC=F" or "XAUUSD=X")
        chain_with_date = chain.partial(current_date=current_date)
        result = chain_with_date.invoke(state["messages"])
        
        report = ""
        if not result.tool_calls:
            report = result.content
        
        return {
            "messages": [result],
            "xau_market_report": report,
        }
    
    return xau_market_analyst_node
