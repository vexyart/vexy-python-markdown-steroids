# Contributing

## Set up a development environment

1. Clone the repository. The default branch is `master`.

    ```bash
    git clone https://github.com/vexyart/vexy-python-markdown-steroids.git
    cd vexy-python-markdown-steroids
    ```

2. Create the environment with the package and its development tools
   (`pytest`, `pytest-cov`, `ruff`):

    ```bash
    uv sync --extra dev
    ```

## Run the tests

```bash
uv run python -m pytest -q
```

There is one test file per extension in `tests/`, for example
`tests/test_keys.py` and `tests/test_md_mako.py`, plus
`tests/test_version.py` and `tests/test_issue102_rendering.py`. The suite has
163 tests.

With coverage:

```bash
uv run python -m pytest --cov=mdx_steroids --cov-report=term-missing
```

## Add or change an extension

1. Put the extension in its own module, `mdx_steroids/<name>.py`.
2. Define options in the extension class as
   `self.config = {"option": [default, "description"]}` and call
   `super().__init__(*args, **kwargs)` afterwards.
3. Register processors in `extendMarkdown(self, md)` with an explicit priority.
   Check the [priority table](architecture.md#where-each-extension-runs) so the
   new processor runs at the right moment relative to the others.
4. Add a module-level `makeExtension(*args, **kwargs)` that returns the
   extension.
5. Add `tests/test_<name>.py` with input Markdown and the expected HTML.
6. Add a page in `src_docs/md/extensions/` and list it in the `nav` of
   `src_docs/mkdocs.yml`.

New source files start with a `this_file:` comment that gives their path.

## Build the package and the documentation

```bash
./build.sh            # documentation and package
./build.sh docs       # documentation only, into docs/
./build.sh package    # dist/*.whl and dist/*.tar.gz, then twine check
```

The documentation source is in `src_docs/md/`, its configuration in
`src_docs/mkdocs.yml`. `src_docs/build.sh` builds it with ProperDocs and the
MaterialX theme in strict mode, so a broken link or any other warning fails the
build. For a live preview that also reloads when files in `mdx_steroids/`
change:

```bash
src_docs/build.sh serve
```

Do not edit `docs/` by hand. The `Docs` workflow rebuilds it and commits it
after every push to `master` that changes `src_docs/`. GitHub Pages serves it at
<https://vexy.dev/vexy-python-markdown-steroids/>.

## Release

The version comes from the latest `vX.Y.Z` git tag through `hatch-vcs`.
`./publish.sh` makes a release:

1. `uvx gitnextver` commits pending changes, tags the next `vX.Y.Z` and pushes.
2. `./build.sh package` builds the wheel and source distribution.
3. `uv publish dist/*` uploads them to PyPI. It needs `UV_PUBLISH_TOKEN` or
   another `uv publish` credential.

The repository has no CI workflow that uploads to PyPI.

## Report a problem

Open an issue at
<https://github.com/vexyart/vexy-python-markdown-steroids/issues> with the
Markdown input, the extension options and the HTML you got.
