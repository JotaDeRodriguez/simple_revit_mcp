# revit_mcp_server.py
import httpx
from mcp.server.fastmcp import FastMCP
import json
import sys

# Create MCP server
mcp = FastMCP("SimpleRevitMCP")

# Configuration
REVIT_HOST = "localhost"
REVIT_PORT = 48884  # Default pyRevit Routes port
BASE_URL = f"http://{REVIT_HOST}:{REVIT_PORT}/simple-mcp-api"

@mcp.tool()
async def get_model_summary() -> str:
    """Get a summary of the active Revit model"""
    # First try the live connection to Revit
    try:
        url = f"{BASE_URL}/model/summary/"
        print(f"Attempting to connect to {url}", file=sys.stderr)
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url)
            print(f"Response status: {response.status_code}", file=sys.stderr)
            
            if response.status_code == 200:
                # Get the data from the response
                data = response.json()
                print(f"Received data: {data}", file=sys.stderr)
                
                # Format the response nicely
                project_name = data.get("Project Name", "Unknown")
                elements = data.get("elements", [])
                views = data.get("views", [])
                
                formatted_response = f"""
                Project: {project_name}
                Elements: {', '.join(elements[:5])}{'...' if len(elements) > 5 else ''}
                Views: {', '.join(views[:5])}{'...' if len(views) > 5 else ''}
                """
                print(f"Returning formatted response", file=sys.stderr)
                return formatted_response
            else:
                error_msg = f"Error from Revit API: {response.status_code} - {response.text}"
                print(error_msg, file=sys.stderr)
                return error_msg
    except Exception as e:
        error_msg = f"Error connecting to Revit: {str(e)}"
        print(error_msg, file=sys.stderr)
        
        # If connection to Revit fails, return fallback data
        return f"""
        {error_msg}
        
        Test data (fallback):
        Project: Test Project
        Elements: Wall, Door, Window, Floor, Ceiling
        Views: Floor Plan, Elevation, Section, 3D View
        """

# Run the server
if __name__ == "__main__":
    mcp.run()