def convert_source_to_html(source, target_dir):
	print('source =', source)
	for child in source.children:
		print('  child =', child)
		print(child.url)
		for grandchild in child.children:
			print('    child =', grandchild)
	print(target_dir)
