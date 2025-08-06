from fastmcp import FastMCP, Context

mcp = FastMCP("ReflectiveReasoner")


@mcp.tool()
async def reflect_and_prompt(input_text: str, ctx: Context) -> str:
    """
    Analyze the input and return a new prompt for deeper self-inquiry.
    """
    await ctx.info(f"Reflecting on: {input_text}")
    return (
        f"You received this statement: '{input_text}'.\n"
        "Now perform self-analysis: What assumptions are you making? "
        "What potential flaws exist? And what would you do next?"
    )


if __name__ == "__main__":
    mcp.run(transport="http")
