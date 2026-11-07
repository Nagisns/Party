# Changelog

## [0.3.1] - 2026-11-08

### Changed

- Routed startup event listener and synchronized command counts through `logging.info`.
- Rewrote command reference descriptions and their Japanese translations using triple-quoted strings with `dedent().strip()` to improve readability while preserving the text and translation keys.
- Added explicit type annotations to command reference state, timeout handling, and Cog initialization.
- Updated release metadata, both README files, and manual verification instructions. Made `0.3.1` the supported release in the current series, replacing `0.3.0`.

### Fixed

- Disabled command reference navigation buttons after 180 seconds of inactivity and added an expiration notice in the original user's language, including Japanese, with instructions to run `/commands` again.
- Ignored missing command reference messages during timeout updates and logged other HTTP failures with tracebacks.
- Caught and logged HTTP failures when sending shared slash command error responses, including follow-up messages.

## [0.3.0] - 2026-11-06

### Added

- Added the `/commands` slash command with a four-page reference: a table of contents and detail pages for `/help`, `/ping`, and `/roll`. It takes no arguments and allows one use per user every five seconds.
- Added previous and next buttons that wrap between the first and last reference pages, with a 180-second inactivity timeout.
- Added Japanese translations for the `/commands` description and reference page titles and descriptions, using the invoking user's Discord language throughout navigation.
- Added a Japanese README and language links in both README files.
- Added `translation_checker` as a Git submodule for AST-based detection of direct `translate(...)` calls, plus a VS Code folder icon association.

### Changed

- Updated release metadata and both README files for four slash commands, command reference navigation, localization, cooldowns, and manual verification.
- Made `0.3.x` the current series and retained `0.2.1` for security fixes only. Ended support for the `0.1.x` series.

### Fixed

- Serialized command reference page updates to keep page state and the displayed embed consistent during overlapping button interactions.

## [0.2.1] - 2026-11-03

### Added

- Added Japanese translations for welcome embed titles and descriptions when the server's preferred locale is Japanese. Other locales use English.
- Added startup output showing the total number of registered Cog event listeners.
- Added Material Icon Theme folder icon associations for `cogs` and `events` in VS Code.

### Changed

- Moved `on_ready` and `on_guild_join` into separate Cog extensions under `src/events/`.
- Extracted a shared package discovery helper and extended automatic loading to event extensions. Command extensions load first, followed by event extensions, with alphabetical ordering within each package and underscore-prefixed names excluded.
- Extracted `translate_for_locale()` so welcome messages and interaction responses share translation lookup and fallback behavior.
- Limited support to the latest release in the current and immediately preceding minor series. The previous series receives security fixes only; `0.2.1` replaces `0.2.0` as the supported release in the current series.
- Added copyright notices and MIT license references to the event modules.
- Updated release metadata and the README for event extension loading, listener counts, and welcome message localization.

## [0.2.0] - 2026-11-01

### Added

- Added an English welcome embed sent to the server's system channel when the bot joins. The greeting is skipped when no system channel is configured.
- Added handling for greeting delivery failures: permission errors are logged as warnings, and other HTTP errors are logged with tracebacks.

### Changed

- Moved the `/help`, `/ping`, and `/roll` commands into separate Cog extensions under `src/cogs/`.
- Replaced the hardcoded extension list with automatic discovery of modules and packages directly inside `cogs`. Extensions load in alphabetical order, and names beginning with `_` are excluded.
- Added copyright notices and MIT license references to the Cog modules.
- Updated the README with greeting behavior and permissions, instructions for adding Cog extensions, and manual verification steps.

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
