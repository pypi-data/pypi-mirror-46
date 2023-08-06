from unv.app.core import create_component_settings


SCHEMA = {
    'autoreload': {'type': 'boolean', 'required': True},
    'jinja2': {
        'type': 'dict',
        'required': True,
        'schema': {
            'enabled': {'type': 'boolean'}
        }
    }
}

DEFAULTS = {
    'autoreload': False,
    'jinja2': {'enabled': True},
}

SETTINGS = create_component_settings('web', DEFAULTS, SCHEMA)
