from fastmcp import FastMCP
from typing import List, Dict
from it_assets_api.it_assets import get_static_inventory

mcp = FastMCP("IT Assets Inventory and Risk MCP")


@mcp.resource("resource://it_assets/server_inventory")
def server_inventory() -> List[Dict]:
    """
    Returns a static list of application inventory records, each representing an enterprise IT system.

    Each record includes:
    - app_id (str): Unique application identifier.
    - name (str): Human-readable name of the application.
    - tier (str): Business criticality level. One of:
        - 'high': Mission-critical systems that directly impact operations or customers.
        - 'medium': Important systems that support internal operations.
        - 'low': Non-critical systems, development, or legacy apps.
    - cves (List[str]): List of CVE identifiers currently affecting the application, as detected by VA scans.

    This resource can be used as input to prioritization tools that analyze risk, patching urgency,
    or exploitability using EPSS or CVSS scores.

    Example:
    {
        "app_id": "APP-001",
        "name": "Core Payments API",
        "tier": "high",
        "cves": ["CVE-2024-4355", "CVE-2023-38545"]
    }
    """
    return get_static_inventory()


from typing import Optional


@mcp.tool()
def prioritise_apps_by_tier(tier_filter: Optional[List[str]] = None) -> List[Dict]:
    """
    Returns a list of applications that match the specified business criticality tiers
    and have at least one known vulnerability (CVE).

    Args:
        tier_filter (Optional[List[str]]): A list of business tiers to include.
            Valid values: ["high", "medium", "low"].
            If not provided, defaults to ["high"].

    Important:
        Applications marked with tier "high" are considered **critical** systems.
        These typically represent mission-critical infrastructure, customer-facing APIs,
        financial transaction processors, or other systems where vulnerabilities may have
        significant business or security impact.

    Each returned result includes:
        - app_id (str): Unique application identifier.
        - name (str): Human-readable application name.
        - cves (List[str]): CVEs affecting the application (as detected by VA scans).

    This tool is typically used to pre-filter applications before enrichment using
    exploitability scores (e.g., via get_epss_by_cve).

    Example input:
        tier_filter = ["high", "medium"]

    Example output:
        [
            {
                "app_id": "APP-001",
                "name": "Core Payments API",
                "cves": ["CVE-2024-4355", "CVE-2023-38545"]
            },
            ...
        ]
    """
    inventory = get_static_inventory()
    tiers = tier_filter if tier_filter else ["high"]

    filtered = [app for app in inventory if app["tier"] in tiers and app["cves"]]

    return filtered
