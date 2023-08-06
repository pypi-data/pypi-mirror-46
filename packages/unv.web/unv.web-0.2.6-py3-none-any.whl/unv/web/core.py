import os
import glob
import pathlib
import asyncio

import uvloop

from aiohttp import web

from unv.app.helpers import get_app_components
from unv.app.settings import IS_DEBUG

from .deploy import DEPLOY_SETTINGS


def link_component_static_dirs(component):
    component_path = pathlib.Path(
        os.path.realpath(component.__file__)).parent
    static_path = component_path / 'static'
    public_dir = DEPLOY_SETTINGS.static_public_dir
    private_dir = DEPLOY_SETTINGS.static_private_dir

    public_app_dirs = str(static_path / public_dir.name / '*')
    for directory in glob.iglob(public_app_dirs):
        os.system('mkdir -p {}'.format(public_dir))
        os.system('ln -sf {} {}'.format(directory, public_dir))

    private_app_dirs = str(static_path / private_dir.name / '*')
    for directory in glob.iglob(private_app_dirs):
        os.system('mkdir -p {}'.format(private_dir))
        os.system('ln -sf {} {}'.format(directory, private_dir))


def create_app(link_static: bool = False):
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    app = web.Application(debug=IS_DEBUG)

    for component in get_app_components():
        component.setup(app)
        if link_static:
            link_component_static_dirs(component)

    return app


def run_app(app):
    web.run_app(
        app,
        host=DEPLOY_SETTINGS.host,
        port=DEPLOY_SETTINGS.port + DEPLOY_SETTINGS.instance,
        access_log=None
    )
