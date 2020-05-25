"""App configuration."""


class DefaultConfig:
    SECRET_KEY = 'dev'


class DevelopmentConfig(DefaultConfig):
    DEBUG = True


class ProductionConfig(DefaultConfig):
    SECRET_KEY = '3O9TN?y6MpncKNm_xuz/VdGyvBjMHi-haH2Mq6c+AFk'
