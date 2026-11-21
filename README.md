<div align="center">

# Party

**English** | [日本語](README.ja.md)

Party is a Discord bot for creating polls and rolling dice with slash commands.
It replies in Japanese when your Discord language is Japanese and in English otherwise.

![Python](https://img.shields.io/badge/Python-3.15-3776AB?logo=python&logoColor=white)
![discord.py](https://img.shields.io/badge/discord.py-5865F2?logo=discord&logoColor=white)
![python-dotenv](https://img.shields.io/badge/python--dotenv-ECD53F?logo=dotenv&logoColor=black)
[![License: MIT](https://img.shields.io/badge/License-MIT-green)](LICENSE)

</div>

Version **0.4.3** (prerelease) · [Changelog](CHANGELOG.md)

[Getting started](#getting-started) · [Usage](#usage) · [Troubleshooting](#troubleshooting) · [Project structure](#project-structure)

## Getting started

You'll need Python 3.15 or later and a Discord server where you can install the bot.
The steps below use pip. For bot creation, tokens, server invitations, or installation with uv, see the [Setup Guide](docs/en/SETUP.md).

1. Clone or download this repository. Open a terminal in the folder containing this README and install the dependencies.

   ```bash
   python -m pip install "discord-extension-discovery==1.0.3" "discord.py>=2.7.1" "python-dotenv>=1.2.4"
   ```

2. Create a file named `.env` in the same folder. Replace `your_bot_token_here` with your bot token. Keep the token private. Git already ignores `.env` in this repository.

   ```env
   TOKEN=your_bot_token_here
   ```

3. Start the bot.

   ```bash
   python src/bot.py
   ```

When the terminal shows `Logged in as ...`, run `/help` in the server where you invited the bot.
You should see a list of commands. Leave the bot running while you use it and press `Ctrl+C` in the terminal to stop it.

## Usage

Type `/` in Discord's message box and select a Party command. If the command takes arguments, fill in the fields before sending it.

| Try in Discord | What happens |
| --- | --- |
| `/help` | Lists the available commands and their descriptions. |
| `/commands` | Opens a command guide. Use the arrow buttons to turn the pages. |
| `/ping` | Shows the bot's WebSocket latency to Discord in milliseconds. |
| `/roll maximum:6` | Rolls one six-sided die. You can choose any whole number of sides from 2 to 1000. |
| `/poll question:Pizza? option1:Yes option2:No hour:1` | Opens a Yes/No poll for one hour. Add `option3` for a third answer. Each voter picks one answer. |

Polls can stay open for 1–240 hours. Omitting `hour` sets the duration to 24 hours. For argument details, cooldowns, and who can see responses, see the [Command Guide](docs/en/COMMANDS.md).

## Troubleshooting

| Symptom | What to check |
| --- | --- |
| The bot exits because `TOKEN` is missing or empty | Check the value of `TOKEN` in the `.env` file next to this README. If you also set a `TOKEN` environment variable, its value takes precedence. |
| Commands are missing from Discord's suggestions | Look for `Synced ... commands.` in the startup logs, then check the invitation scopes and command permissions in the channel. [Setup Guide](docs/en/SETUP.md) |
| A command returns a cooldown error | Wait before trying again. The [cooldown reference](docs/en/COMMANDS.md#cooldowns) lists how often you can use each command. |
| No welcome message appears when the bot joins | Set a system channel for the server and grant the bot **View Channel**, **Send Messages**, and **Embed Links** in that channel. |

## Project Structure

The main files and directories are organized as follows:

```text
Party/
├── .github/
│   └── workflows/
│       └── tests.yml     # Runs pytest with GitHub Actions
├── docs/
│   ├── en/               # Setup, command, and development guides in English
│   └── ja/               # Japanese versions of the guides
├── src/
│   ├── bot.py            # Entry point, token loading, and bot startup
│   ├── mybot.py          # Bot class, extension loading, and command synchronization
│   ├── error_handler.py  # Shared slash command error handling
│   ├── localization.py   # Japanese translations and locale helpers
│   └── cogs/             # Command and listener extensions grouped by feature
│       ├── activities/   # /poll and /roll
│       ├── diagnostics/  # /ping and connection logging
│       ├── guide/        # /help and the interactive /commands guide
│       └── guilds/       # Welcome message when the bot joins a server
├── tests/                # Automated tests for event logging and command navigation
├── .python-version       # Python version used for local development
├── pyproject.toml        # Project metadata, dependencies, and pytest settings
├── uv.lock               # Locked dependency versions for uv
├── start.ps1             # PowerShell launcher with an optional pytest run
├── README.md             # English README
├── README.ja.md          # Japanese README
├── CHANGELOG.md          # Version history
├── SECURITY.md           # Security policy
└── LICENSE               # MIT License
```

For details on adding commands and event listeners, see the [Development Guide](docs/en/DEVELOPMENT.md).

## License and acknowledgements

Released under the [MIT License](LICENSE).
Built with [discord.py](https://discordpy.readthedocs.io/) and [python-dotenv](https://github.com/theskumar/python-dotenv).

This README was written with assistance from ChatGPT.
