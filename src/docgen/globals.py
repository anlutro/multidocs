import docgen.settings
import docgen.config
import docgen.jinja2

__all__ = ["settings", "config", "j2"]

settings = docgen.settings.get_settings()
config = docgen.config.get_config()
j2 = docgen.jinja2.get_jinja2_env()
