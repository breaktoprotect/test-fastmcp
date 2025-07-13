from fastmcp import FastMCP
from common.logging_middleware import TraceMiddleware
from epss_api.server import mcp as epss_mcp
from calc_api.server import mcp as calc_mcp
from food_api.server import mcp as food_mcp
from it_assets_api.mcp_tools import mcp as it_assets_mcp


main = FastMCP("Main MCP Server")
main.add_middleware(TraceMiddleware())

main.mount(epss_mcp, prefix="epss")
main.mount(calc_mcp, prefix="calc")
main.mount(it_assets_mcp, prefix="it_assets")
# main.mount(food_mcp, prefix="food")

if __name__ == "__main__":
    main.run(transport="http", host="0.0.0.0", port=5001)
