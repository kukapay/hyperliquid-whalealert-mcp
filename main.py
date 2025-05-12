import os
from typing import List, Dict, Any
from dataclasses import dataclass
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP, Context
from mcp.server.fastmcp.prompts import base

# Load environment variables
load_dotenv()
API_KEY = os.getenv("COINGLASS_API_KEY")
if not API_KEY:
    raise ValueError("COINGLASS_API_KEY not set in .env")

# API configuration
API_BASE_URL = "https://open-api-v4.coinglass.com/api/hyperliquid/whale-alert"
HEADERS = {"CG-API-KEY": API_KEY}

# Define application context for lifecycle management
@dataclass
class AppContext:
    client: httpx.AsyncClient

@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    """Manage HTTP client lifecycle"""
    async with httpx.AsyncClient(headers=HEADERS) as client:
        yield AppContext(client=client)

# Initialize MCP server
mcp = FastMCP(
    name="Hyperliquid Whale Alert",
    dependencies=["httpx", "python-dotenv", "pandas"],
    lifespan=app_lifespan
)

# Helper function to fetch whale alert data
async def fetch_whale_data(client: httpx.AsyncClient) -> List[Dict[str, Any]]:
    try:
        response = await client.get(API_BASE_URL)
        response.raise_for_status()
        data = response.json()
        if data.get("code") != "0":
            raise ValueError(f"API error: {data.get('msg')}")
        return data.get("data", [])
    except httpx.HTTPStatusError as e:
        raise ValueError(f"HTTP error: {str(e)}")
    except Exception as e:
        raise ValueError(f"Failed to fetch whale data: {str(e)}")

# Helper function to convert JSON to Markdown list
def json_to_markdown_list(data: List[Dict[str, Any]]) -> str:
    if not data:
        return "No whale alert data available."
    
    markdown_lines = []
    for tx in data:
        # Map position_action to human-readable
        action = "Open" if tx.get("position_action") == 1 else "Close"
        
        # Convert timestamp (milliseconds) to readable format
        create_time = datetime.fromtimestamp(tx.get("create_time") / 1000.0).strftime("%Y-%m-%d %H:%M:%S")
        
        # Format transaction as Markdown list item
        item = (
            f"- **{tx.get('symbol')} Transaction**:\n"
            f"  - User Address: {tx.get('user')}\n"
            f"  - Position Size: {tx.get('position_size')}\n"
            f"  - Entry Price: ${tx.get('entry_price')}\n"
            f"  - Liquidation Price: ${tx.get('liq_price')}\n"
            f"  - Position Value (USD): ${tx.get('position_value_usd')}\n"
            f"  - Action: {action}\n"
            f"  - Create Time: {create_time}"
        )
        markdown_lines.append(item)
    
    return "\n".join(markdown_lines)

# Tool
@mcp.tool()
async def get_whale_alerts(ctx: Context) -> str:
    """Fetch recent whale alerts and return as a Markdown table"""
    client = ctx.request_context.lifespan_context.client
    data = await fetch_whale_data(client)
    return json_to_markdown_list(data)

# Prompt
@mcp.prompt()
def summarize_whale_activity() -> List[base.Message]:
    """Summarize recent whale activity"""
    prompt_text = (
        "Summarize recent whale transactions on Hyperliquid. "
        "Include key metrics like total position value, number of transactions, "
        "and notable symbols."
    )
    return [
        base.UserMessage(prompt_text),
        base.AssistantMessage("I'll analyze the whale transaction data and provide a summary.")
    ]

# Run the server
if __name__ == "__main__":
    mcp.run()