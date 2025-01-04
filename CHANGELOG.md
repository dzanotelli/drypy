# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [2025-01-04] 1.1.0

### Added
- added new `sentinel` decorator ([PR #21](
    https://github.com/dzanotelli/drypy/pull/21) by [@sakshilucky25](
        https://github.com/sakshilucky25))

## [2024-01-02] 1.0.4

### Fixed
- shpinx: fix conf.py, was still using old `get_version` function

## [2024-01-02] 1.0.3

### Fixed
- docs: added docs own `requirements.txt` with sphinx rtd theme (#19)
- build: now build automatically reads the current git tag, instead of relying
    on `version.py` and `get_version()` function (removed)

NOTE: switching to gitflow to handle branches and versions.

## [2023-08-04] 1.0.2

### Added
- docs: added `.readthedocs.yaml` file as required by Read The Docs (#18)

## [2020-02-22] 1.0.1

### Fixed
- docs: added an `important` block to guide about how to avoid `RecursionError`.
- docs: added 'setup logging' page

## [2018-10-21] 1.0

### Added
First stable version, provides two patterns, sham and sheriff-deputy.
