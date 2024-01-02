# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [2024-01-02] 1.0.3
- docs: added docs own `requirements.txt` with sphinx rtd theme (#19)
- build: now build automatically reads the current git tag, instead of relying
    on `version.py` and `get_version()` function (removed)

NOTE: switching to gitflow to handle branches and versions.

## [2023-08-04] 1.0.2
- docs: added `.readthedocs.yaml` file as required by Read The Docs (#18)

## [2020-02-22] 1.0.1
- docs: added an `important` block to guide about how to avoid `RecursionError`.
- docs: added 'setup logging' page

## [2018-10-21] 1.0
First stable version, provides two patterns, sham and sheriff-deputy.
