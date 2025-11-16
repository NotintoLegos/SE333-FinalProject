import subprocess
import re
from pathlib import Path
from typing import Optional, Dict, Any
import fastmcp

mcp_git = fastmcp.FastMCP("GitTools")

# Git ignore patterns
EXCLUDE_PATTERNS = [
    '*.class', '*.jar', '*.war', '*.ear', 'target/', 'build/',
    '*.iml', '*.ipr', '*.iws', '.idea/', '*.log', 'logs/',
    'node_modules/', 'dist/', 'out/', '.gradle/', '.venv/',
    '__pycache__/', '*.pyc', '*.pyo', '*.pyd', '.Python', 'env/'
]

@mcp_git.tool()
def git_status(repo_path: str = ".") -> Dict[str, Any]:
    """Return git status including clean status, staged changes, and conflicts"""
    try:
        repo_path = Path(repo_path).absolute()
        
        # Check if it's a git repository
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=repo_path,
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            return {"error": "Not a git repository or git command failed"}
        
        lines = result.stdout.strip().split('\n') if result.stdout else []
        
        staged = []
        unstaged = []
        untracked = []
        conflicts = []
        
        for line in lines:
            if not line.strip():
                continue
                
            status = line[:2]
            file_path = line[3:]
            
            # Check for merge conflicts
            if status in ('UU', 'AA', 'DD', 'DU', 'UD'):
                conflicts.append({"file": file_path, "status": status})
            elif status[0] in ('A', 'M', 'D', 'R', 'C'):  # Staged changes
                staged.append({"file": file_path, "status": status[0]})
            elif status[1] in ('A', 'M', 'D', 'R', 'C'):  # Unstaged changes
                unstaged.append({"file": file_path, "status": status[1]})
            elif status == '??':  # Untracked files
                untracked.append(file_path)
        
        return {
            "is_clean": len(lines) == 0,
            "staged_changes": staged,
            "unstaged_changes": unstaged,
            "untracked_files": untracked,
            "conflicts": conflicts,
            "summary": f"Staged: {len(staged)}, Unstaged: {len(unstaged)}, Untracked: {len(untracked)}, Conflicts: {len(conflicts)}"
        }
        
    except Exception as e:
        return {"error": f"Failed to get git status: {str(e)}"}

@mcp_git.tool()
def git_add_all(repo_path: str = ".", exclude_patterns: Optional[list] = None) -> Dict[str, Any]:
    """Stage all changes with intelligent filtering, excluding build artifacts and temporary files"""
    try:
        repo_path = Path(repo_path).absolute()
        exclude_patterns = exclude_patterns or EXCLUDE_PATTERNS
        
        # First, get current status to see what would be added
        status_result = git_status(repo_path)
        if "error" in status_result:
            return status_result
        
        # Add all changes
        result = subprocess.run(
            ["git", "add", "."],
            cwd=repo_path,
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            return {"error": f"Failed to stage changes: {result.stderr}"}
        
        # Now unstage the excluded patterns
        for pattern in exclude_patterns:
            subprocess.run(
                ["git", "reset", pattern],
                cwd=repo_path,
                capture_output=True
            )
        
        # Verify what was actually staged
        final_status = git_status(repo_path)
        
        return {
            "success": True,
            "message": "Changes staged successfully (excluding build artifacts)",
            "staged_files": final_status.get("staged_changes", []),
            "excluded_patterns": exclude_patterns
        }
        
    except Exception as e:
        return {"error": f"Failed to stage changes: {str(e)}"}

@mcp_git.tool()
def git_commit(message: str, repo_path: str = ".", include_coverage: bool = True) -> Dict[str, Any]:
    """Automated commit with standardized messages, optionally including coverage statistics"""
    try:
        repo_path = Path(repo_path).absolute()
        
        # Get current coverage if available and requested
        coverage_info = ""
        if include_coverage:
            coverage_data = parse_jacoco_report(str(repo_path))
            if "line_coverage" in coverage_data and not "error" in coverage_data:
                coverage_info = f"\n\nCode Coverage: {coverage_data['line_coverage']:.1f}% line coverage"
        
        # Construct final commit message
        full_message = f"{message}{coverage_info}"
        
        result = subprocess.run(
            ["git", "commit", "-m", full_message],
            cwd=repo_path,
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            return {"error": f"Commit failed: {result.stderr}"}
        
        # Get the commit hash
        commit_hash_result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_path,
            capture_output=True,
            text=True
        )
        
        return {
            "success": True,
            "message": "Commit created successfully",
            "commit_hash": commit_hash_result.stdout.strip() if commit_hash_result.returncode == 0 else "Unknown",
            "commit_message": full_message
        }
        
    except Exception as e:
        return {"error": f"Commit failed: {str(e)}"}

@mcp_git.tool()
def git_push(remote: str = "origin", branch: str = "main", repo_path: str = ".") -> Dict[str, Any]:
    """Push to remote with upstream configuration, handling authentication through existing credential helpers"""
    try:
        repo_path = Path(repo_path).absolute()
        
        # First, set upstream if not already set
        set_upstream = subprocess.run(
            ["git", "push", "--set-upstream", remote, branch],
            cwd=repo_path,
            capture_output=True,
            text=True
        )
        
        if set_upstream.returncode == 0:
            return {
                "success": True,
                "message": f"Successfully pushed to {remote}/{branch} and set upstream",
                "output": set_upstream.stdout
            }
        
        # If setting upstream failed, try regular push
        result = subprocess.run(
            ["git", "push", remote, branch],
            cwd=repo_path,
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            return {
                "error": f"Push failed: {result.stderr}",
                "hint": "Check your credentials and network connection"
            }
        
        return {
            "success": True,
            "message": f"Successfully pushed to {remote}/{branch}",
            "output": result.stdout
        }
        
    except Exception as e:
        return {"error": f"Push failed: {str(e)}"}

@mcp_git.tool()
def git_pull_request(base: str = "main", title: str = "", body: str = "", repo_path: str = ".") -> Dict[str, Any]:
    """Create a pull request against the specified base branch with standardized templates"""
    try:
        repo_path = Path(repo_path).absolute()
        
        # Get current branch name
        branch_result = subprocess.run(
            ["git", "branch", "--show-current"],
            cwd=repo_path,
            capture_output=True,
            text=True
        )
        
        if branch_result.returncode != 0:
            return {"error": "Failed to get current branch name"}
        
        current_branch = branch_result.stdout.strip()
        
        # Generate default title if not provided
        if not title:
            # Get last commit message for title
            commit_result = subprocess.run(
                ["git", "log", "-1", "--pretty=%s"],
                cwd=repo_path,
                capture_output=True,
                text=True
            )
            title = commit_result.stdout.strip() if commit_result.returncode == 0 else "Automated changes"
        
        # Generate default body if not provided
        if not body:
            # Get coverage information
            coverage_data = parse_jacoco_report(str(repo_path))
            coverage_info = ""
            if "line_coverage" in coverage_data and not "error" in coverage_data:
                coverage_info = f"**Code Coverage**: {coverage_data['line_coverage']:.1f}% line coverage\n\n"
            
            # Get commit history for this branch
            log_result = subprocess.run(
                ["git", "log", f"{base}..{current_branch}", "--oneline"],
                cwd=repo_path,
                capture_output=True,
                text=True
            )
            
            commit_history = ""
            if log_result.returncode == 0 and log_result.stdout:
                commits = log_result.stdout.strip().split('\n')
                commit_history = "**Changes in this PR:**\n" + "\n".join([f"- {commit}" for commit in commits[-5:]]) + "\n\n"
            
            body = f"""{coverage_info}{commit_history}
This pull request was automatically generated by the Testing Agent MCP.

**Changes include:**
- Automated test generation and improvements
- Code coverage enhancements
- Test execution results
"""
        
        # Note: GitHub CLI (gh) is commonly used for creating PRs
        # You might need to install it: https://cli.github.com/
        
        # Try using GitHub CLI if available
        gh_result = subprocess.run(
            ["gh", "pr", "create", 
             "--base", base,
             "--title", title,
             "--body", body],
            cwd=repo_path,
            capture_output=True,
            text=True
        )
        
        if gh_result.returncode == 0:
            # Extract PR URL from output
            pr_url = gh_result.stdout.strip()
            return {
                "success": True,
                "message": "Pull request created successfully",
                "pull_request_url": pr_url,
                "branch": current_branch,
                "base": base
            }
        else:
            # Fallback: Return instructions for manual PR creation
            return {
                "success": False,
                "message": "GitHub CLI not available or failed",
                "instructions": f"Please create PR manually from {current_branch} to {base}",
                "title": title,
                "body": body,
                "branch": current_branch,
                "base": base
            }
        
    except Exception as e:
        return {"error": f"Failed to create pull request: {str(e)}"}

# Helper function (you'll need to import or define this)
def parse_jacoco_report(report_path: str) -> Dict[str, Any]:
    """Parse JaCoCo XML report - you should import this from your coverage_analyzer"""
    # This is a simplified version - use your actual implementation
    try:
        report_file = Path(report_path) / "target/site/jacoco/jacoco.xml"
        if report_file.exists():
            tree = ET.parse(report_file)
            root = tree.getroot()
            # Your actual parsing logic here
            return {"line_coverage": 85.5}  # Example
        return {"error": "No coverage report found"}
    except:
        return {"error": "Failed to parse coverage report"}