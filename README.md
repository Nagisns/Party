# Party

[English](README.md) | [日本語](README.ja.md)

A Discord bot built with Python and `discord.py`, featuring slash commands
and Japanese localization.

The current release is **0.3.1**. The project is in prerelease development.
See the [changelog](CHANGELOG.md) for release history.

## Features

- **Command Reference:** Browse command details across four embed pages using
  previous and next buttons.
- **Help:** Displays an embed listing the available slash commands.
- **Ping:** Shows the bot's WebSocket latency in milliseconds.
- **Roll:** Rolls a die with 2 to 1000 sides and displays the result in an embed.
- **Welcome Message:** Sends a welcome embed to the server's system channel
  when the bot joins, if a system channel is configured and the bot has
  permission to send it. The title and description use Japanese when the
  server's preferred locale is Japanese, and English for other locales.
- **Japanese Localization:** Displays command and argument descriptions and
  responses in Japanese when the user's Discord language is set to Japanese.
- **Error Messages:** The shared slash command error handler sends localized
  error messages visible only to the user who ran the command.
- **Automatic Extension Loading:** Discovers and loads command and event
  extensions at startup.

## Commands

| Command | Description |
|---|---|
| `/commands` | Displays a command reference with navigation buttons. |
| `/help` | Displays an embed listing the registered slash commands and their descriptions. |
| `/ping` | Displays the bot's WebSocket latency in milliseconds. |
| `/roll` | Rolls one die with the specified number of sides and displays the result in an embed. |

See the [Command Guide](docs/en/COMMANDS.md) for arguments, examples,
cooldowns, language settings, and response behavior.

## Requirements

- Python 3.15 or later, as specified in `pyproject.toml`
- A Discord bot application and its bot token
- A Discord server where you can install the bot
- `discord.py` 2.7.1 or later
- `python-dotenv` 1.2.4 or later

## Quick Start

Clone or download this repository, then open a terminal in the project directory.

1. Create a Discord bot and invite it to your server by following the
   [Setup Guide](docs/en/SETUP.md).
2. Install the dependencies:

   ```bash
   python -m pip install "discord.py>=2.7.1" "python-dotenv>=1.2.4"
   ```

3. Create `.env` in the project directory and set your bot token:

   ```env
   TOKEN=your_bot_token_here
   ```

   Keep the token private and do not commit `.env` to Git.

4. Start the bot:

   ```bash
   python src/bot.py
   ```

Once the bot is running, try `/help` or `/roll maximum:6` in your server.
For uv commands, permission settings, and environment variable behavior,
see the [Setup Guide](docs/en/SETUP.md).

## Documentation

| Guide | Contents |
|---|---|
| [Setup](docs/en/SETUP.md) | Bot creation, installation, permissions, environment variables, and startup. |
| [Commands](docs/en/COMMANDS.md) | Usage, arguments, cooldowns, localization, and response visibility. |
| [Development](docs/en/DEVELOPMENT.md) | Adding extensions, startup and error handling, and manual testing. |

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE)
file for details.

## Acknowledgements

- [discord.py](https://discordpy.readthedocs.io/)
- [python-dotenv](https://github.com/theskumar/python-dotenv)

This README was written with assistance from ChatGPT.
