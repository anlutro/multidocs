import multidocs.settings
import multidocs.config
import multidocs.jinja2

__all__ = ["settings", "config", "j2"]

settings = multidocs.settings.get_settings()
config = multidocs.config.get_config()
j2 = multidocs.jinja2.get_jinja2_env()
