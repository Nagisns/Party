<div align="center">

# Party

**English** | [日本語](README.ja.md)

A Discord bot built with discord.py, featuring slash commands
for polls, dice rolls, latency checks, and an interactive command guide.
Responds in Japanese or English based on your Discord language settings.

![Python](https://img.shields.io/badge/Python-3.15-3776AB?logo=python&logoColor=white)
![discord.py](https://img.shields.io/badge/discord.py-5865F2?logo=discord&logoColor=white)
![python-dotenv](https://img.shields.io/badge/python--dotenv-ECD53F?logo=dotenv&logoColor=black)
[![License: MIT](https://img.shields.io/badge/License-MIT-green)](LICENSE)

</div>

Version **0.4.1** · In prerelease development · [Changelog](CHANGELOG.md)

[What you can do](#what-you-can-do) · [Getting started](#getting-started) · [Usage](#usage) · [Troubleshooting](#troubleshooting) · [Project Structure](#project-structure) · [Documentation](#documentation)

## What you can do

| I want to… | Command | What it does |
| --- | --- | --- |
| See available commands | `/help` | Lists commands and their descriptions. |
| Learn how commands work | `/commands` | Opens a guide with buttons to switch pages. |
| Check the bot's connection | `/ping` | Shows WebSocket latency to Discord in milliseconds. |
| Roll a die | `/roll` | Rolls one die with 2–1000 sides. |
| Create a poll | `/poll` | Creates a single-choice poll with two or three answers, open for 1–240 hours. |

The bot also sends a welcome message when it joins a server.
This requires a configured system channel and permission for the bot to send the message there.

## Getting started

### 1. Prepare what you need

- **Python 3.15 or later**, as specified in the [project configuration](pyproject.toml)
- **A Discord bot and its bot token**
- **A Discord server where you can install the bot**

If you have not created and invited a bot yet, follow the [Setup Guide](docs/en/SETUP.md) first.
Then clone or download this repository and open a terminal in **the folder containing this README**.
Run all commands below from that folder.

### 2. Install the required packages

```bash
python -m pip install "discord.py>=2.7.1" "python-dotenv>=1.2.4"
```

If you use uv, see the alternative instructions in the [Setup Guide](docs/en/SETUP.md).

### 3. Set your bot token

Create a file named `.env` next to this README and save the following content.
Replace `your_bot_token_here` with your own bot token.

```env
TOKEN=your_bot_token_here
```

> **Keep your token private.** Do not publish `.env` or commit it to Git.
> This project's `.gitignore` already excludes `.env`.

### 4. Start the bot and check it works

```bash
python src/bot.py
```

When the terminal shows `Logged in as ...`, the bot is connected to Discord.
Run `/help` in the server where you installed it and check that the command list appears.
Keep the program running while you use the bot.
To stop it, press `Ctrl+C` in the terminal.

## Usage

Type `/` in Discord's message box and select one of Party's commands from the suggestions.

**Example: roll a six-sided die**

Select `/roll`, set `maximum` (the number of sides) to `6`, and send the command.

```text
/roll maximum:6
```

The result is a number from 1 to 6. `maximum` accepts **integers from 2 to 1000**.

**Example: create a poll**

Select `/poll` and enter a question and two answers. Set `hour` to `1` for a one-hour poll:

```text
/poll question:Pizza? option1:Yes option2:No hour:1
```

You can add a third answer with `option3`. If you omit `hour`, voting stays open for 24 hours.
See the [poll instructions](docs/en/COMMANDS.md#poll) for all parameters.

- **See the command list:** Use `/help`. The `!help` prefix command is disabled.
- **Browse command details:** Use `/commands` and switch pages with the arrow buttons.
  Buttons expire after 180 seconds of inactivity; run the command again to continue.
  The five-page guide covers `/help`, `/ping`, `/roll`, and `/poll`.
- **Use Japanese:** Set your Discord language to Japanese. Command names stay in English.
- **Response visibility:** Normal responses appear in the channel. Shared command error messages are visible only to the person who ran the command.

See the [Command Guide](docs/en/COMMANDS.md) for cooldowns and details about language settings.

## Troubleshooting

| What happened? | What to check |
| --- | --- |
| The bot exits with a missing or empty `TOKEN` error | Check that `.env` is next to this README and that `TOKEN` has a value. |
| Commands do not appear in Discord's suggestions | Check the startup logs, then review installation settings and command permissions in the [Setup Guide](docs/en/SETUP.md). |
| Repeated commands return a cooldown error | Commands have usage limits. Check the [Command Guide](docs/en/COMMANDS.md#cooldowns) and wait before trying again. |
| No welcome message arrives | Check the server's system channel setting and the bot's Send Messages and Embed Links permissions there. |

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
│   ├── cogs/             # Slash command extensions
│   │   ├── commands.py   # Interactive command guide
│   │   ├── help.py       # Command list
│   │   ├── ping.py       # Latency check
│   │   ├── poll.py       # Poll creation
│   │   └── roll.py       # Dice rolls
│   └── events/           # Event listener extensions
│       ├── guild_join.py # Welcome message when joining a server
│       └── ready.py      # Connection and server statistics logging
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

## Documentation

| What you need | Guide |
| --- | --- |
| Bot creation, invitation, permissions, and startup with uv | [Setup](docs/en/SETUP.md) |
| Command arguments, cooldowns, language settings, and response visibility | [Commands](docs/en/COMMANDS.md) |
| Adding command and event extensions, automatic loading, error handling, and manual testing | [Development](docs/en/DEVELOPMENT.md) |
| Changes in each version | [Changelog](CHANGELOG.md) |

## License and acknowledgements

Released under the [MIT License](LICENSE).
Built with [discord.py](https://discordpy.readthedocs.io/) and [python-dotenv](https://github.com/theskumar/python-dotenv).

This README was written with assistance from ChatGPT.
