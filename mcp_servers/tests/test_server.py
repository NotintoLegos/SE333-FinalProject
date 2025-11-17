import importlib
import sys
import types


def test_add_function():
    # Provide a lightweight dummy `fastmcp` module before importing server
    fastmcp_mod = types.ModuleType("fastmcp")

    class FastMCP:
        def __init__(self, name):
            self.name = name

        def tool(self, fn):
            # decorator that returns the function unchanged
            return fn

        def run(self, **kwargs):
            return None

    fastmcp_mod.FastMCP = FastMCP
    sys.modules["fastmcp"] = fastmcp_mod

    # Import server after injecting dummy fastmcp
    server = importlib.import_module("server")

    # The add function should correctly add two integers
    assert server.add(2, 3) == 5


def test_server_run_as_main():
    # Ensure the module's __main__ block runs without error (mcp.run is a no-op in dummy)
    import runpy

    # Re-inject dummy fastmcp for the runpy execution environment
    import types as _types, sys as _sys
    fastmcp_mod = _types.ModuleType("fastmcp")

    class FastMCP:
        def __init__(self, name):
            self.name = name

        def tool(self, fn):
            return fn

        def run(self, **kwargs):
            return None

    fastmcp_mod.FastMCP = FastMCP
    _sys.modules["fastmcp"] = fastmcp_mod

    # Execute server as a script (this will call mcp.run(transport="sse") in __main__)
    runpy.run_module("server", run_name="__main__")
