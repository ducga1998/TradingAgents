from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from tradingagents.dataflows.fred_api import get_dxy_data, get_real_yields, get_inflation_data, get_fred_series

def create_xau_macro_analyst(llm):
    """
    Creates a node for the XAU Macro Analyst agent.

    This agent specializes in analyzing macroeconomic factors that influence the price of gold (XAU/USD).
    It replaces the traditional fundamentals analyst for equity trading.
    """

    system_message = (
        "You are a specialized Macroeconomic Analyst for Gold (XAU/USD). Your mission is to provide a detailed analysis of the key macro drivers affecting gold's price. "
        "DO NOT analyze company fundamentals. Instead, focus exclusively on the following:"
        "\n\n1.  **US Dollar Index (DXY)**: Analyze its recent trend (e.g., past 90 days). Is it strengthening or weakening? Explain how this trend typically impacts gold."
        "\n2.  **Real Yields**: Analyze the trend in 10-year real yields. Are they rising or falling? Explain the inverse relationship between real yields and gold (i.e., opportunity cost)."
        "\n3.  **Inflation Data**: Review the latest inflation metrics (CPI, PCE). Is inflation running hot or cooling down? Explain how inflation expectations affect gold's appeal as a hedge."
        "\n4.  **Fed Policy & VIX (Optional)**: Briefly mention the current Federal Reserve stance (if known) and the VIX level as a measure of market fear."
        "\n\nUse the available tools to fetch the necessary data. Synthesize your findings into a comprehensive report. "
        "Conclude your report with a Markdown table summarizing the key macro factors and their likely impact on gold (Bullish, Bearish, or Neutral)."
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
        get_dxy_data,
        get_real_yields,
        get_inflation_data,
        get_fred_series, # For VIX or other specific series
    ]

    prompt = prompt.partial(
        system_message=system_message,
        tool_names=", ".join([tool.name for tool in tools]),
    )

    chain = prompt | llm.bind_tools(tools)

    def xau_macro_analyst_node(state):
        """
        The node function for the XAU Macro Analyst.
        """
        current_date = state["trade_date"]
        # The ticker is XAU, but the tools are specific to macro data.
        chain_with_date = chain.partial(current_date=current_date)
        result = chain_with_date.invoke(state["messages"])

        report = ""
        if not result.tool_calls:
            report = result.content

        return {
            "messages": [result],
            "xau_macro_report": report,
        }

    return xau_macro_analyst_node