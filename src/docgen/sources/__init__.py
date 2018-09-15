import importlib


def download_source(**kwargs):
	source_type = kwargs.pop('type', None)
	# todo: guess type based on url?
	source_module = importlib.import_module('%s.%s' % (__name__, source_type))
	return source_module.download_source(**kwargs)
