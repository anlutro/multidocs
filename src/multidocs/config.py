import os
import os.path
import yaml


_conf_values = None


def read_config():
    conf_file = os.environ.get("MULTIDOCS_CONFIG_FILE")
    if conf_file:
        if not os.path.exists(conf_file):
            raise RuntimeError("MULTIDOCS_CONFIG_FILE %r does not exist" % conf_file)
        if not os.path.isfile(conf_file):
            raise RuntimeError("MULTIDOCS_CONFIG_FILE %r is not a file" % conf_file)
        with open(conf_file) as fh:
            return yaml.safe_load(fh)


def get_config():
    global _conf_values
    if _conf_values is None:
        _conf_values = read_config()
    return _conf_values
