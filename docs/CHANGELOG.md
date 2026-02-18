# Changelog

All notable changes to this project will be documented in this file.

The format is (read: strives to be) based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

---

## [0.2.6] - 2026-02-17
### Added:
- io.export_help_svg()
- export_svg flag to cli_helptree.py

---

## [0.2.5] - 2026-02-13
### Changed:
- Improve metadata by adding kind key, for app versus command.
- Establish sane ordering with commands first and sub apps after, in both data for JSON and in helptree prints.

---

## [0.2.4] – 2026-02-11
### Changed:
- Update screenshots.

---

## [0.2.3] – 2026-02-11
### Added:
- Add .whl, tar.gz, and checksum upload to release via publish.yml

---

## [0.2.2] – 2026-02-11
### Fixed:
- Stabilie demo cli.py contents.
- Remove erroneous AGPL3+ label.
- Fix browse-exports command to reference the path in io.py

---

## [0.2.1] – 2026-02-11
### Added:
- io.py, for JSON and TXT file export
- Flags: --export-json and --export-txt

### Changed:
- Move contents of helptree.py -> cli_helptree.py, so that helptre.py can be used as the core functionality.
- Better separation of concerns.
- Don't truncate short descriptions.

### Fixed:
- Before, only flat apps could be seen. Now there is recursive investigation of click groups so that nested sub apps can be represented.

---

## [0.1.8] – 2026-01-28
### Changed:
- Update versioning to not rely on datacopy of pyproject.toml and instead use _version.__version__

---

## [0.1.7] – 2026-01-22
### Fixed:
- Remove the erroneous AGPL reference in the pyproject.toml, which had been copied from pdflinkcheck.

---

## [0.1.5] – 2026-01-22
### Fixed:
- Expose `add_typer_helptree()` in __init__.py
- Update screenshot.

---

## [0.1.4] – 2026-01-22
### Fixed:
- Troubleshoot screenshot update.

---

## [0.1.3] – 2026-01-22
### Added:
- In readme, mention projects that use typer-helptree
- Change OSI Development Status to "5 - Production/Stable"

---

## [0.1.2] – 2026-01-22
### Added:
- Example python cli.py usage.
- User story in README.md.

---

## [0.1.1] – 2026-01-22
### Added:
- Screenshot.
- PyPI stable.

---

## [0.1.0] – 2026-01-22
### Added:
- Inital commit.
- Copied files and portions from pdflinkcheck code, at v1.3.35.
- Rename project to typer_helptree.
- Start github repository at https://github.com/City-of-Memphis-Wastewater/typer-helptree
- For CI actions, copy and adjust from Dworshak.
- Update to Pyhabitat v1.1.26, with new is_in_git_repo() function.

