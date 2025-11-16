import fastmcp
from test_generator import mcp_test
from coverage_analyzer import mcp_coverage
from git_tools import mcp_git

# Create main MCP instance
mcp = fastmcp.FastMCP("TestingAgent")

# Import all tools from all modules
mcp.include(mcp_test)
mcp.include(mcp_coverage)
mcp.include(mcp_git)

# Optional: Add a combined workflow tool
@mcp.tool()
def automated_test_workflow(project_path: str, commit_message: str = "Automated test improvements") -> Dict[str, Any]:
    """Complete automated testing workflow: test, commit, and push changes"""
    results = {}
    
    # Run tests
    results['test_execution'] = execute_tests(project_path)
    
    # Analyze coverage
    results['coverage'] = parse_jacoco_report(project_path)
    
    # Git operations
    results['git_status'] = git_status(project_path)
    results['git_add'] = git_add_all(project_path)
    results['git_commit'] = git_commit(commit_message, project_path)
    results['git_push'] = git_push(repo_path=project_path)
    
    return results

if __name__ == "__main__":
    mcp.run(transport="sse")