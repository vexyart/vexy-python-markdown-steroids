<!-- this_file: DEPENDENCIES.md -->
# Dependencies

## Issue 102 runtime dependency audit

- Python-Markdown: extension lifecycle and parsing API.
- PyMdown Extensions: keyboard names and case-preserving wiki slugs.
- Mako: embedded documentation templates and includes.
- lxml and cssselect: selector-based exclusions and translation attributes.
- BeautifulSoup4 and html5lib: optional HTML normalization.
- PyYAML: YAML metadata with string-preserving BaseLoader.
- filetype, imageio and requests: existing smart-image MIME, dimensions and URL reading.
- json-flatten: existing keyboard map flattening.

The latter dependencies are now declared by the package rather than assumed to exist in a documentation build environment.
