from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from tradingagents.agents.utils.agent_utils import get_news, get_global_news

def create_xau_news_analyst(llm):
    """
    Creates a node for the XAU News Analyst agent.
    
    This agent analyzes news and geopolitical events affecting gold prices.
    Gold is heavily influenced by geopolitical tensions, central bank policies,
    and macroeconomic events, making news analysis critical.
    """
    
    system_message = (
        "You are a specialized News and Geopolitical Analyst for Gold (XAU/USD). Your mission is to analyze how current news and events are impacting gold prices. "
        "Focus exclusively on the following:"
        "\n\n1. **Federal Reserve & Central Bank Policy**: Analyze any recent Fed statements, interest rate decisions, or central bank announcements. "
        "Dovish policy (lower rates, QE) is typically bullish for gold. Hawkish policy (higher rates, QT) is typically bearish."
        "\n2. **Geopolitical Tensions**: Assess any geopolitical conflicts, trade wars, or political instability. Gold serves as a 'safe haven' asset during times of uncertainty."
        "\n3. **Central Bank Gold Buying**: Monitor news about central banks (especially China, Russia, India) buying or selling gold reserves. This indicates institutional demand."
        "\n4. **Economic Data Releases**: Review major economic events (jobs reports, GDP, inflation data) and their likely impact on gold. "
        "Weak economic data often supports gold as a hedge."
        "\n5. **Dollar Strength News**: News affecting the US dollar (trade deals, policy changes) directly impacts gold due to their inverse relationship."
        "\n6. **Mining Sector News**: Major news from gold mining companies, supply disruptions, or production changes."
        "\n\nUse the available tools to fetch recent news. Analyze the sentiment and likely impact on gold prices. "
        "Consider both the immediate reaction and longer-term implications."
        "\n\nSynthesize your findings into a comprehensive news report. "
        "Conclude with a Markdown table summarizing the key news items and their likely impact on gold (Bullish, Bearish, or Neutral)."
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
        get_news,
        get_global_news,
    ]
    
    prompt = prompt.partial(
        system_message=system_message,
        tool_names=", ".join([tool.name for tool in tools]),
    )
    
    chain = prompt | llm.bind_tools(tools)
    
    def xau_news_analyst_node(state):
        """
        The node function for the XAU News Analyst.
        """
        current_date = state["trade_date"]
        ticker = state.get("company_of_interest", "Gold")
        chain_with_date = chain.partial(current_date=current_date)
        result = chain_with_date.invoke(state["messages"])
        
        report = ""
        if not result.tool_calls:
            report = result.content
        
        return {
            "messages": [result],
            "xau_news_report": report,
        }
    
    return xau_news_analyst_node
