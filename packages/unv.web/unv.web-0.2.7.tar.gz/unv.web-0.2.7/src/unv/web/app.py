import copy
import jinja2

from aiohttp import web

from unv.app.settings import SETTINGS as APP_SETTINGS

from .helpers import (
    url_for_static, url_with_domain, inline_static_from, make_url_for_func
)
from .settings import SETTINGS


def setup_jinja2(app: web.Application):
    settings = copy.deepcopy(SETTINGS.get('jinja2', {}))
    if not settings.pop('enabled'):
        return

    settings['enable_async'] = True
    settings['loader'] = jinja2.ChoiceLoader([
        jinja2.PackageLoader(package)
        for package in APP_SETTINGS['components']
    ])
    if 'jinja2.ext.i18n' not in settings.setdefault('extensions', []):
        settings['extensions'].append('jinja2.ext.i18n')

    app['jinja2'] = jinja2.Environment(**settings)
    app['jinja2'].globals.update({
        'url_for_static': url_for_static,
        'inline_static_from': inline_static_from,
        'url_with_domain': url_with_domain,
        'url_for': make_url_for_func(app),
        'for_development': APP_SETTINGS['env'] == 'development',
        'for_production': APP_SETTINGS['env'] == 'production'
    })


def setup(app: web.Application):
    setup_jinja2(app)
