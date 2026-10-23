# Changelog

## [0.1.0] - 2026-10-23

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
- The `/help` and `/ping` commands do not have permission checks or cooldowns configured in this prerelease, although the shared error handler supports these error types.
