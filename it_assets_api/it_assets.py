from typing import List, Dict


# Define raw inventory logic outside the MCP resource
def get_static_inventory() -> List[Dict]:
    return [
        {
            "app_id": "APP-001",
            "name": "Core Payments API",
            "tier": "high",
            "cves": ["CVE-2024-4355", "CVE-2023-38545"],
        },
        {
            "app_id": "APP-002",
            "name": "Customer Web Portal",
            "tier": "high",
            "cves": ["CVE-2024-3094", "CVE-2022-42889"],
        },
        {
            "app_id": "APP-003",
            "name": "Trading Engine",
            "tier": "high",
            "cves": ["CVE-2023-4863"],
        },
        {
            "app_id": "APP-004",
            "name": "HR Self-Service",
            "tier": "medium",
            "cves": ["CVE-2022-42889"],
        },
        {
            "app_id": "APP-005",
            "name": "Forex Rate Service",
            "tier": "medium",
            "cves": [],
        },
        {
            "app_id": "APP-006",
            "name": "Reporting Data Mart",
            "tier": "medium",
            "cves": ["CVE-2021-44228"],
        },
        {
            "app_id": "APP-007",
            "name": "Marketing CMS",
            "tier": "low",
            "cves": ["CVE-2023-23752"],
        },
        {
            "app_id": "APP-008",
            "name": "Legacy FTP Gateway",
            "tier": "low",
            "cves": ["CVE-2018-10933"],
        },
        {"app_id": "APP-009", "name": "Chatbot Service", "tier": "low", "cves": []},
        {
            "app_id": "APP-010",
            "name": "Proof-of-Concept Sandbox",
            "tier": "low",
            "cves": ["CVE-2024-22219", "CVE-2023-34362"],
        },
    ]
