# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.13] - 2026-10-04

### Fixed

- Ported legacy extensions to the current Python-Markdown and PyMdown APIs.
- Preserved Unicode, HTML tails, rewritten image URLs, reference images and explicit image widths.
- Restored title and definition-list figure captions, including multiple images per caption.
- Fixed Mako metadata ordering, included headings and render-state isolation.
- Declared all imported runtime dependencies and rebuilt the historical documentation.

### Verified

- All 163 tests pass; branch-aware coverage is 87%.

## [0.4.11] - 2026-05-12

### Fixed

- Fixed `md_mako` and `meta_yaml` for modern Python-Markdown (>=3.0): replaced
  deprecated `self.markdown` attribute with `self.md` on `Preprocessor` subclasses.

## [Unreleased]

### Changed

#### Build & Packaging
- Modernized build: switched from `setuptools` to `hatchling` + `hatch-vcs`.
- Renamed PyPI distribution from `mdx-steroids` to `vexy-python-markdown-steroids` (import package stays `mdx_steroids`).
- Removed hand-rolled `mdx_steroids/_version.py`; version is now derived from git tags via `hatch-vcs` (generated `mdx_steroids/__version__.py`, gitignored).
- Replaced `scripts/build.sh` (`python -m build`) and `scripts/release.sh` (`twine`) with root-level `build.sh` (`uvx hatch build`) and `publish.sh` (`gitnextver` + `uv publish`).
- Bumped `requires-python` to `>=3.12` and tightened dependency lower bounds.
- Updated project URLs to `https://github.com/vexyart/vexy-python-markdown-steroids`.

### Added

#### Documentation Infrastructure
- Comprehensive MkDocs-based documentation system
  - Material theme with custom CSS styling
  - Complete navigation structure for all sections
  - mkdocstrings plugin for API documentation
  - mike plugin for version management
- New documentation pages:
  - Project overview with feature cards (index.md)
  - Detailed installation guide
  - Quick start tutorial with examples
  - Comprehensive configuration guide
  - Extensions overview and selection guide
  - Detailed absimgsrc extension documentation
- Prepared documentation deployment infrastructure (GitHub Actions workflow template available)

#### Testing
- New comprehensive test suites:
  - test_keys.py - Tests for keyboard shortcut formatting
  - test_md_mako.py - Tests for Mako templating extension
  - test_img_smart.py - Tests for smart image processing

#### Code Quality
- Comprehensive docstrings added to:
  - absimgsrc.py - Google-style docstrings with examples
  - comments.py - Complete module documentation
- Type hints added throughout:
  - comments.py - Full type annotations
  - absimgsrc.py - Type hints for better IDE support

#### Build System
- Git-tag-based semantic versioning system
- Comprehensive test suite covering all extensions
- Automated CI/CD pipeline with GitHub Actions
- Multi-platform build support (Linux, Windows, macOS)
- Convenient build, test, and release scripts
- Code formatting and linting configuration
- Automated PyPI publishing on git tags

### Changed
- comments.py completely rewritten with:
  - Better code organization and structure
  - Comprehensive docstrings
  - Type hints throughout
  - Improved readability
- Updated package structure to support modern development workflows
- Improved error handling in version detection
- Enhanced build system with proper dependency management

### Fixed
- Missing `known_schemes` definition in absimgsrc.py
- Duplicate import statement in absimgsrc.py
- Version detection now works correctly in all environments
- Build system properly handles git repositories and source distributions

## [0.7.0] - Previous Release

### Added
- Original mdx-steroids functionality
- Collection of Python Markdown extensions
- Basic build system with setup.py

## 2026-10-04 — Issue 102 documentation build repair

Modernized kill_tags/replimgsrc registration and interlink configuration passing; preserved Unicode/tail text and empty HTML. Corrected indented kill_tags fixtures and added rendering regressions: 14 targeted tests pass. Removed unsupported historical SuperFences option. Historical documentation and full-suite migration remain incomplete; not published.

Evidence: `/Users/adam/Developer/vcs3/.mkdocs-build-audit/issue-102/README.md`.


## 2026-10-04 — Issue 102 extension migration continuation

Historical documentation now builds. Ported figure-caption, metadata, absolute-image and translate-no registrations; current PyMdown wiki slugs preserve case. Fixed Mako first-line loss, included headings, metadata ordering, metadata isolation and absolute auto-includes. Declared the runtime dependencies previously supplied only by build launchers. Removed unused incompatible icon/span extensions from the historical documentation config.

Verification: 65 migration tests pass; the full suite has 32 failures and 126 passes. Publication and downstream migration remain pending. Evidence is in `/Users/adam/Developer/vcs3/.mkdocs-build-audit/issue-102/`.


### Issue 102 manual-source rendering verification

- Preserve leading horizontal rules when YAML metadata is enabled.
- Figure captions now support the manuals' definition-list form, consecutive figures, and multiple images sharing one caption.
- Fresh caption/metadata/outline verification: 25 tests passed. All six existing FontLab active-manual compatibility regressions also passed.
- Full package verification and release remain pending.
