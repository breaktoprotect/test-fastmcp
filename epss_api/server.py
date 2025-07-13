from fastmcp import FastMCP
import aiohttp
from typing import Optional

# Create the MCP server instance
mcp = FastMCP("EPSS CVE Lookup Server")


@mcp.tool()
async def get_epss_by_cve(cve_id: str) -> dict:
    """Fetch EPSS information for a given CVE ID from the public EPSS API."""
    url = f"https://api.first.org/data/v1/epss?cve={cve_id}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                raise ValueError(
                    f"Failed to fetch EPSS data for {cve_id}: {resp.status}"
                )
            data = await resp.json()
            if not data.get("data"):
                raise ValueError(f"No EPSS data found for {cve_id}")
            return data["data"][0]


@mcp.tool()
async def get_multiple_epss_of_multiple_cve(cve_id: str) -> dict:
    """
    Fetch EPSS information for multiple CVE IDs (comma-separated) from the public EPSS API.
    Returns a dictionary mapping each CVE ID to its EPSS data or error message.
    """
    cve_ids = [c.strip() for c in cve_id.split(",") if c.strip()]
    results = {}
    url = "https://api.first.org/data/v1/epss?cve="
    async with aiohttp.ClientSession() as session:
        for cve in cve_ids:
            try:
                async with session.get(url + cve) as resp:
                    if resp.status != 200:
                        results[cve] = {
                            "error": f"Failed to fetch EPSS data: {resp.status}"
                        }
                        continue
                    data = await resp.json()
                    if not data.get("data"):
                        results[cve] = {"error": "No EPSS data found"}
                    else:
                        results[cve] = data["data"][0]
            except Exception as e:
                results[cve] = {"error": str(e)}
    return results


@mcp.tool()
async def get_epss_by_cve_in_time_series(
    cve_id: str, date: Optional[str] = None
) -> dict:
    """
    Fetch EPSS time-series information for a CVE ID from the public EPSS API.
    Returns historical EPSS scores for the 30 days prior to the specified date.

    Args:
        cve_id: The CVE ID to query (e.g., CVE-2022-25204)
        date: Optional date to get 30 days of historical data from (e.g., 2022-03-05).
             If not provided, returns the last 30 days from today.

    Returns:
        Dictionary containing time-series EPSS data for the CVE showing scores over time

    Raises:
        ValueError: If the API request fails or no data is found
    """
    url = "https://api.first.org/data/v1/epss"
    params = {"cve": cve_id, "scope": "time-series"}

    if date:
        params["date"] = date

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as resp:
                if resp.status != 200:
                    raise ValueError(
                        f"Failed to fetch EPSS time-series data for {cve_id}: HTTP {resp.status}"
                    )

                data = await resp.json()

                if not data.get("data"):
                    raise ValueError(f"No time-series EPSS data found for {cve_id}")

                return {"cve_id": cve_id, "time_series_data": data["data"]}

    except aiohttp.ClientError as e:
        raise ValueError(
            f"Network error while fetching EPSS time-series data: {str(e)}"
        )


# if __name__ == "__main__":
#     # mcp.run()
#     mcp.add_middleware(TraceMiddleware())
#     mcp.run(transport="http", host="127.0.0.1", port=5001)
