from langgraph.prebuilt import ToolNode
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.xau_config import XAU_CONFIG

# Import XAU-specific tools
from tradingagents.agents.utils.agent_utils import (
    get_stock_data,
    get_indicators,
    get_correlation,
    get_dxy_data,
    get_real_yields,
    get_inflation_data,
    get_fred_series,
    get_news,
    get_global_news,
    get_cot_positioning,
    analyze_cot_extremes,
    get_gold_etf_summary,
    get_gold_etf_flows,
)

class XAUTradingGraph(TradingAgentsGraph):
    """
    A specialized trading graph for XAU (Gold) trading.

    This graph uses a custom set of agents and tools tailored for macroeconomic
    and positioning analysis relevant to gold.
    """

    def __init__(self, debug=False, config=None):
        # Use XAU-specific config and analyst team
        xau_config = config or XAU_CONFIG
        xau_analysts = xau_config.get("analyst_team", [])

        super().__init__(
            selected_analysts=xau_analysts,
            debug=debug,
            config=xau_config
        )

    def _create_tool_nodes(self):
        """
        Override the tool node creation to use XAU-specific tools.
        """
        return {
            "xau_market": ToolNode([
                get_stock_data,       # For XAU/USD price data from yfinance (e.g., "GC=F")
                get_indicators,       # Standard technical indicators
                get_correlation,      # For correlation with DXY, etc.
            ]),
            "xau_macro": ToolNode([
                get_dxy_data,
                get_real_yields,
                get_inflation_data,
                get_fred_series,      # For VIX, etc.
            ]),
            "xau_news": ToolNode([
                get_news,             # For general and gold-specific news
                get_global_news,
            ]),
            "xau_positioning": ToolNode([
                get_cot_positioning,
                analyze_cot_extremes,
                get_gold_etf_summary,
                get_gold_etf_flows,
            ]),
        }