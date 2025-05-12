# Hyperliquid WhaleAlert MCP

An MCP server that provides real-time whale alerts on Hyperliquid, flagging positions with a notional value exceeding $1 million.

![GitHub License](https://img.shields.io/github/license/kukapay/hyperliquid-whalealert-mcp)
![Python Version](https://img.shields.io/badge/python-3.10+-blue)
![Status](https://img.shields.io/badge/status-active-brightgreen.svg)

## Features

- **Tool: `get_whale_alerts`**: Fetches recent whale transactions and returns them as a Markdown table using `pandas` for clean formatting.
- **Prompt: `summarize_whale_activity`**: Generates a summary of whale transactions, including metrics like total position value and notable symbols.

## Prerequisites

- **Python**: Version 3.10 or higher.
- **CoinGlass API Key**: Obtain from [CoinGlass](https://www.coinglass.com/) (required for API access).
- **uv**: Package and dependency manager ([install uv](https://docs.astral.sh/uv/)).

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/kukapay/hyperliquid-whalealert-mcp.git
   cd hyperliquid-whalealert-mcp
   ```

2. **Install Dependencies**:
   ```bash
   uv sync
   ```
   This installs dependencies specified in `pyproject.toml`.

3. **Claude Desktop Integration**:
   Install the server in Claude Desktop:
   ```bash
   uv run mcp install mcp.py --name "Hyperliquid Whale Alert"
   ```
   
    Or update the configuration file manually:
  
    ```
    {
      "mcpServers": {
        "hyperliquid-whalealert": {
          "command": "uv",
          "args": [ "--directory", "/path/to/hyperliquid-whalealert-mcp", "run", "main.py" ],
          "env": { "COINGLASS_API_KEY": "your_api_key" }
        }
      }
    }
    ```       
    Replace `/path/to/hyperliquid-whalealert-mcp` with your actual installation path and `COINGLASS_API_KEY` with your API key.

## Usage

### Using the Tool

The `get_whale_alerts` tool fetches whale transaction data and returns it as a Markdown list. Example output:

```markdown
- **ETH Transaction**:
  - User Address: 0x3fd4444154242720c0d0c61c74a240d90c127d33
  - Position Size: 12700
  - Entry Price: $1611.62
  - Liquidation Price: $527.2521
  - Position Value (USD): $21003260
  - Action: Close
  - Create Time: 2025-05-20 12:31:57
- **BTC Transaction**:
  - User Address: 0x1cadadf0e884ac5527ae596a4fc1017a4ffd4e2c
  - Position Size: 33.54032
  - Entry Price: $87486.2
  - Liquidation Price: $44836.8126
  - Position Value (USD): $2936421.4757
  - Action: Close
  - Create Time: 2025-05-20 12:31:17
```
  
To invoke the tool:
- In the MCP Inspector, select `get_whale_alerts` and execute.
- In Claude Desktop, use the registered server and call the tool via the UI or API.

### Using the Prompt

The `summarize_whale_activity` prompt generates a summary of whale transactions. Example interaction (in a compatible client):

```plaintext
/summarize_whale_activity
```

Response:
```
I'll analyze the whale transaction data and provide a summary.
```

This can be extended by LLMs to provide detailed metrics like total position value or notable symbols.


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

