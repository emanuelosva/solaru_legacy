"""App configuration."""

import os


class DefaultConfig:
    SECRET_KEY = 'dev'


class DevelopmentConfig(DefaultConfig):
    DEBUG = True


class ProductionConfig(DefaultConfig):
    SECRET_KEY = "8B?9CLYHJ2d?P8tb/2uSKNDu+Er0Af*5I?zfU18GXc4"
