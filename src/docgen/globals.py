__all__ = ['settings', 'config']


from . import _settings, _config
settings = _settings.get_settings()
config = _config.get_config()
