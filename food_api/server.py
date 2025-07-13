import mcp.types as types
from mcp.server import Server
import mcp.server.stdio
from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions
import asyncio

# Hardcoded food items
FOOD_ITEMS = [
    {"id": 1, "description": "Beer", "quantity": 24},
    {"id": 2, "description": "Apple", "quantity": 10},
    {"id": 3, "description": "Bread", "quantity": 5},
    {"id": 4, "description": "Cheese", "quantity": 2},
    {"id": 5, "description": "Banana", "quantity": 12},
    {"id": 6, "description": "Chocolate", "quantity": 11},
]

server = Server("food-api")


@server.call_tool()
async def get_food_by_id(id: int) -> dict:
    for item in FOOD_ITEMS:
        if item["id"] == id:
            return item
    raise ValueError(f"Food item with id {id} not found.")


async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="food-api",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())
