# revit_mcp_server.py
import httpx
from mcp.server.fastmcp import FastMCP, Context

# Create MCP server
mcp = FastMCP("SimpleRevitMCP")

# Configuration
REVIT_HOST = "localhost"
REVIT_PORT = 48884  # Default pyRevit Routes port
BASE_URL = f"http://{REVIT_HOST}:{REVIT_PORT}/simple-mcp-api"

# Helper function to make requests to pyRevit Routes
async def call_revit_api(endpoint, method="GET", data=None):
    """Make request to pyRevit Routes API with timeout and error handling"""
    url = f"{BASE_URL}/{endpoint}"
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:  # Add a timeout
            if method == "GET":
                response = await client.get(url)
            else:
                response = await client.post(url, json=data)
            return response.json()
    except httpx.ConnectError:
        raise ConnectionError(f"Cannot connect to Revit API at {url}. Is Revit running?")
    except httpx.TimeoutException:
        raise TimeoutError(f"Request to {url} timed out")
    except Exception as e:
        raise Exception(f"Error communicating with Revit API: {str(e)}")
    

### TOOLS AND METHODS

@mcp.resource("revit://model/summary")
async def get_model_summary() -> str:
    """Get a summary of the active Revit model"""
    try:
        model_data = await call_revit_api("model/summary")
        return f"""
        Project: {model_data['name']}
        Elements: {model_data['elements']}
        Views: {model_data['views']}
        """
    except Exception as e:
        return f"Error fetching model summary: {str(e)}"

# Run the server
if __name__ == "__main__":
    mcp.run()