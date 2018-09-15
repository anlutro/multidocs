import os.path

from docgen.globals import config, settings
from docgen.sources import download_source

from .converter import convert_source_to_html


def generate_html():
	for source_cfg in config['sources']:
		source = download_source(**source_cfg)
		source_target_dir = os.path.join(settings.target_dir, source.slug)
		convert_source_to_html(source, source_target_dir)
