from typing import List, Type

from reworked_platform.db.crud.oauth import OAuthCrud
from reworked_platform.schemas.user import UserBase
from reworked_platform.web.api.agent.tools.code import Code
from reworked_platform.web.api.agent.tools.image import Image
from reworked_platform.web.api.agent.tools.search import Search
from reworked_platform.web.api.agent.tools.sidsearch import SID
from reworked_platform.web.api.agent.tools.tool import Tool
from reworked_platform.web.api.agent.tools.market_research import MarketResearch
from reworked_platform.web.api.agent.tools.content_generation import ContentGeneration
from reworked_platform.web.api.agent.tools.web_development import WebDevelopment
from reworked_platform.web.api.agent.tools.campaign_analysis import CampaignAnalysis

# Import affiliate marketing tools
from reworked_platform.web.api.agent.tools.affiliate_product_research import AffiliateProductResearch
from reworked_platform.web.api.agent.tools.competitor_affiliate_analysis import CompetitorAffiliateAnalysis
from reworked_platform.web.api.agent.tools.conversion_optimization import ConversionOptimization
from reworked_platform.web.api.agent.tools.affiliate_revenue_scaling import AffiliateRevenueScaling


async def get_user_tools(
    tool_names: List[str], user: UserBase, crud: OAuthCrud
) -> List[Type[Tool]]:
    tools = list(map(get_tool_from_name, tool_names)) + get_default_tools()
    return [tool for tool in tools if await tool.dynamic_available(user, crud)]


def get_available_tools() -> List[Type[Tool]]:
    return get_external_tools() + get_default_tools() + get_marketing_tools() + get_affiliate_tools()


def get_available_tools_names() -> List[str]:
    return [get_tool_name(tool) for tool in get_available_tools()]


def get_external_tools() -> List[Type[Tool]]:
    return [
        # Wikipedia,  # TODO: Remove if async doesn't work
        Image,
        Code,
        SID,
    ]


def get_default_tools() -> List[Type[Tool]]:
    return [
        Search,
    ]


def get_marketing_tools() -> List[Type[Tool]]:
    return [
        MarketResearch,
        ContentGeneration,
        WebDevelopment,
        CampaignAnalysis,
    ]


def get_affiliate_tools() -> List[Type[Tool]]:
    return [
        AffiliateProductResearch,
        CompetitorAffiliateAnalysis,
        ConversionOptimization,
        AffiliateRevenueScaling,
    ]


def get_tool_name(tool: Type[Tool]) -> str:
    return format_tool_name(tool.__name__)


def format_tool_name(tool_name: str) -> str:
    return tool_name.lower()


def get_tools_overview(tools: List[Type[Tool]]) -> str:
    """Return a formatted string of name: description pairs for all available tools"""

    # Create a list of formatted strings
    formatted_strings = [
        f"'{get_tool_name(tool)}': {tool.description}" for tool in tools
    ]

    # Remove duplicates by converting the list to a set and back to a list
    unique_strings = list(set(formatted_strings))

    # Join the unique strings with newlines
    return "\n".join(unique_strings)


def get_tool_from_name(tool_name: str) -> Type[Tool]:
    for tool in get_available_tools():
        if get_tool_name(tool) == format_tool_name(tool_name):
            return tool

    return get_default_tool()


def get_default_tool() -> Type[Tool]:
    return Search


def get_default_tool_name() -> str:
    return get_tool_name(get_default_tool())
