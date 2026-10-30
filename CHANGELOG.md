# Changelog

## [0.1.2] - 2026-10-31

### Added

- Added the `/roll` command with a required `maximum` argument from 2 to 1000. It rolls one die, displays an embed with a result from 1 through `maximum`, and allows three uses per user every ten seconds.
- Added a description for the `/roll` command's `maximum` option and Japanese translations for the command description, option description, and result embed title.

### Changed

- Grouped Japanese translations into common, help, ping, and roll dictionaries, merging them into `JA_TRANSLATIONS` while preserving existing translations and lookup behavior.
- Normalized spacing in the `/ping` command decorator.
- Updated the README for three slash commands, their arguments and cooldowns, Japanese localization, installation permissions, and manual testing.

### Fixed

- Disabled discord.py's built-in `!help` prefix command, which did not use the slash command cooldowns. Use `/help` for the command list.
- Handled `ValueError` from `NaN` WebSocket latency in `/ping`, returning the localized measurement failure message already used for `OverflowError`.

## [0.1.1] - 2026-10-29

### Added

- Added uv project configuration (`pyproject.toml`, `uv.lock`, and `.python-version`) with runtime dependency requirements and pytest as a development dependency.
- Added a security policy describing supported versions and best-effort vulnerability handling.

### Changed

- Set the project's Python requirement to 3.15 or later and documented pip setup and uv installation and startup using the lockfile.
- Limited shared slash command error logging to unexpected errors, included tracebacks, and enabled root logger configuration at startup.

### Fixed

- Handled `OverflowError` during `/ping` latency measurement with a localized failure message displayed in the channel.
- Standardized the `/ping` command description and its Japanese translation key to `Check bot latency.`.
- Corrected the README and the v0.1.0 release notes to document the existing per-user cooldown of one use every five seconds for each command.
- Clarified the README descriptions of error logging and the visibility of shared error handler responses and ping measurement failure messages.
- Corrected the documented v0.1.0 release date to 2026-10-24.

## [0.1.0] - 2026-10-24

This is the first prerelease for version 0.1.0.

### Added

- Added the `/help` command, which displays an embed listing the registered slash commands and their descriptions.
- Added the `/ping` command, which displays the bot's WebSocket latency in milliseconds.
- Added Japanese translations for command descriptions, the help embed title, command responses, and error messages based on the user's Discord language setting.
- Added the `MyBot` class to register the Japanese translator and synchronize global slash commands during startup.
- Added support for loading the `TOKEN` environment variable from a `.env` file.
- Added validation for the `TOKEN` environment variable. The bot displays an error message and exits with status code `1` if the variable is missing, empty, or contains only whitespace.
- Added a shared slash command error handler with messages for missing permissions, command cooldowns, and unexpected errors.
- Added error responses visible only to the user who ran the command, using follow-up messages when the interaction has already received a response.
- Added console output for the number of synchronized commands, the logged-in bot, and command errors.

### Command Behavior

- English is used for Discord languages other than Japanese and for messages without a Japanese translation.
- The `/help` and `/ping` commands do not have custom permission checks configured in this prerelease.
- Each command has a per-user cooldown of one use every five seconds.
