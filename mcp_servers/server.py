# server.py
from fastmcp import FastMCP
from test_generator import mcp as mcp_test
from coverage_analyzer import mcp as mcp_coverage

mcp = FastMCP("Demo 🚀")

mcp.include(mcp_test)
mcp.include(mcp_coverage)

@mcp.tool
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.tool()
def get_project_status(project_path: str) -> dict:
    """Get overall status of a Maven project"""
    import subprocess
    try:
        # Check if it's a valid Maven project
        result = subprocess.run(
            ["mvn", "compile"], 
            cwd=project_path, 
            capture_output=True, 
            text=True
        )
        return {
            "is_maven_project": Path(project_path).joinpath("pom.xml").exists(),
            "compilation_success": result.returncode == 0,
            "compilation_output": result.stdout if result.returncode != 0 else "Compilation successful"
        }
    except Exception as e:
        return {"error": str(e)}
    
if __name__ == "__main__":
    mcp.run(transport="sse")
