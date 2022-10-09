import os

from .Development import Development
from .Production import Production
from .PreProduction import PreProduction

env_name = os.getenv('INT_ENV', default='dev')

app_config = {
    'dev': Development,
    'pre': PreProduction,
    'prod': Production
}

config = app_config[env_name]
config_obj = app_config[env_name].__dict__