import functools

import ujson as json

from aiohttp import web

from .helpers import render_template


def as_json(f):
    """Return json response from passed dict result."""
    @functools.wraps(f)
    async def wrapper(request, *args, **kwargs):
        data = await f(request, *args, **kwargs)
        return web.json_response(data, dumps=json.dumps)
    return wrapper


def render(
        template_name: str, context_processors: dict = None,
        status: int = web.HTTPOk.status_code):
    """Render jinja2 template by given name and custom context processors."""
    context_processors = context_processors or {}

    def decorator(f):
        @functools.wraps(f)
        async def wrapper(request, *args, **kwargs):
            context = await f(request, *args, **kwargs)
            return await render_template(
                request, template_name, context, context_processors, status)
        return wrapper

    return decorator
