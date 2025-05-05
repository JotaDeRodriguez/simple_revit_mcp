import asyncio
import sys
import mcp
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from pprint import pprint

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
                for i, resource in enumerate(resources.resources):
                    print(f"Resource {i+1}: URI={resource.uri}, Name={resource.name}")

                target_uri = "revit://model/summary"
                try:
                    print(f"\nAttempting to read resource: {target_uri}")
                    result = await session.read_resource(target_uri)

                    # Print raw result for detailed debugging
                    print("Raw result type:", type(result))
                    print("Raw result structure:", dir(result))

                    # Handle different possible response formats
                    if hasattr(result, 'contents') and result.contents:
                        print("\nModel summary:")
                        for content in result.contents:
                            if hasattr(content, 'text') and content.text:
                                print(content.text)
                    elif isinstance(result, tuple):
                        # Handle tuple format (meta, contents)
                        if len(result) >= 2 and isinstance(result[1], list):
                            for content in result[1]:
                                if hasattr(content, 'text') and content.text:
                                    print("\nModel summary:")
                                    print(content.text)
                    else:
                        print(f"Could not extract content from result: {result}")

                except Exception as e:
                    print(f"Error reading resource: {type(e)}: {e}")
                    import traceback
                    traceback.print_exc()

    except Exception as e:
        print(f"Error: {type(e)}: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        raise

if __name__ == "__main__":
    print("Starting test client...")
    asyncio.run(test_client())