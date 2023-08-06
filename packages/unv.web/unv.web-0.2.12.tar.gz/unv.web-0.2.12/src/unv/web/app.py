import jinja2

from aiohttp import web

from unv.app.settings import SETTINGS as APP_SETTINGS

from .helpers import (
    url_for_static, url_with_domain, inline_static_from, make_url_for_func
)
from .settings import SETTINGS


def setup_jinja2(app: web.Application):
    if not SETTINGS.jinja2_enabled:
        return

    app['jinja2'] = jinja2.Environment(**SETTINGS.jinja2_settings)
    app['jinja2'].globals.update({
        'url_for': make_url_for_func(app),
        'url_for_static': url_for_static,
        'url_with_domain': url_with_domain,
        'inline_static_from': inline_static_from,
        'for_developemnt': APP_SETTINGS.is_development,
        'for_production': APP_SETTINGS.is_production,
        'for_testing': APP_SETTINGS.is_testing
    })


def setup(app: web.Application):
    setup_jinja2(app)
