# Party

**English** | [日本語](README.ja.md)

**A Python Discord bot for rolling dice and checking the bot's connection latency.**
Use slash commands to interact with it, with Japanese and English responses based on your Discord language settings.

Version **0.3.1** · In prerelease development · [Changelog](CHANGELOG.md)

[What you can do](#what-you-can-do) · [Getting started](#getting-started) · [Usage](#usage) · [Troubleshooting](#troubleshooting) · [Documentation](#documentation)

## What you can do

| I want to… | Command | What it does |
| --- | --- | --- |
| See available commands | `/help` | Lists commands and their descriptions. |
| Learn how commands work | `/commands` | Opens a guide with buttons to switch pages. |
| Check the bot's connection | `/ping` | Shows WebSocket latency to Discord in milliseconds. |
| Roll a die | `/roll` | Rolls one die with 2–1000 sides. |

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

- **See the command list:** Use `/help`. The `!help` prefix command is disabled.
- **Browse command details:** Use `/commands` and switch pages with the arrow buttons.
  Buttons expire after 180 seconds of inactivity; run the command again to continue.
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
