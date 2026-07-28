import asyncio
import json

from mcp import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client

server_params = StdioServerParameters(
    command="python",
    args=["-m", "mcp_server.server"],
)


async def _call_tool(tool_name: str, arguments: dict):
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            result = await session.call_tool(tool_name, arguments)

            print("=" * 80)
            print("TOOL:", tool_name)
            print("ARGS:", arguments)
            print("CONTENT:", result.content)
            print("STRUCTURED:", result.structuredContent)
            print("=" * 80)

            # Fast path
            if result.structuredContent is not None:
                return result.structuredContent

            # Fallback for list responses
            if result.content:
                text = result.content[0].text
                try:
                    return json.loads(text)
                except Exception:
                    return text

            return None


def call_tool(tool_name: str, arguments: dict):
    return asyncio.run(_call_tool(tool_name, arguments))