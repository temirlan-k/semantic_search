from config.config import Environment, Settings
from main.builders.base import AbstractAppBuilder
from main.builders.dev import DevAppBuilder


BUILDERS = {
    Environment.DEV: DevAppBuilder,
}


def get_builder(settings: Settings) -> AbstractAppBuilder:
    builder_class = BUILDERS[settings.environment]
    return builder_class(settings)