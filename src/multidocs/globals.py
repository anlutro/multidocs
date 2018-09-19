import multidocs.settings
import multidocs.config

__all__ = ["settings", "config"]

settings = multidocs.settings.get_settings()
config = multidocs.config.get_config()
