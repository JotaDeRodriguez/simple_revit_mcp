import asyncio
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_client():
    print("Connecting to MCP server...")
    try:
        # Connect to your MCP server
        server_params = StdioServerParameters(
            command="python",
            args=["mcp_client_server.py"]
        )
        
        async with stdio_client(server_params) as (read, write):
            print("Connection established, initializing session...")
            async with ClientSession(read, write) as session:
                # Initialize connection
                await session.initialize()
                print("Session initialized!")
                
                # List all resources
                print("Requesting resources...")
                resources = await session.list_resources()
                print(f"Available resources: {[r.uri for r in resources.resources]}")
                
                # Only try to read the model summary if it exists
                if any(r.uri == "revit://model/summary" for r in resources.resources):
                    # Read the model summary resource
                    print("Requesting model summary...")
                    content, mime_type = await session.read_resource("revit://model/summary")
                    print("\nModel summary:")
                    print(content)
                else:
                    print("Model summary resource not found!")
    except Exception as e:
        print(f"Error: {type(e).__name__}: {e}", file=sys.stderr)
        raise

if __name__ == "__main__":
    print("Starting test client...")
    asyncio.run(test_client())