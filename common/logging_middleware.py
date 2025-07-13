# common/middleware.py
from fastmcp.server.middleware import Middleware, MiddlewareContext


class TraceMiddleware(Middleware):
    async def on_message(self, ctx: MiddlewareContext, call_next):
        print("→", ctx.method, ctx.message)
        result = await call_next(ctx)
        print("←", result)
        return result
