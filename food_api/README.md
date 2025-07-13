# Food API for FastMCP 2.0

This is a simple mock API using FastMCP 2.0 that allows you to retrieve a food item by its ID. The data is hardcoded with 5 items (including beer).

## How to Run

1. Make sure you have the dependencies installed (see Pipfile).
2. Run the server:

```bash
C:/Users/JS/.virtualenvs/test-fastmcp2-JLaVmqAk/Scripts/python.exe -m food_api.server
```

## API Method

-   **get_food_by_id**: Retrieve a food item by its ID.
    -   **Input:** `id` (integer)
    -   **Output:** `{ "id": int, "description": str, "quantity": int }`

## Example Items

-   Beer (id: 1)
-   Apple (id: 2)
-   Bread (id: 3)
-   Cheese (id: 4)
-   Banana (id: 5)

This API is for demonstration and testing purposes only.
