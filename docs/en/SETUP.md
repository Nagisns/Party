# Setup Guide

[English](SETUP.md) | [日本語](../ja/SETUP.ja.md)

[README](../../README.md) | [Commands](COMMANDS.md) | [Development](DEVELOPMENT.md)

## Requirements

- Python 3.15 or later, as specified in `pyproject.toml`
- A Discord bot application and its bot token
- A Discord server where you can install the bot
- `discord.py` 2.7.1 or later
- `python-dotenv` 1.2.4 or later

## Setup

### 1. Get the project

Clone or download this repository, then open a terminal in the project
directory.

### 2. Install the dependencies

```bash
python -m pip install "discord.py>=2.7.1" "python-dotenv>=1.2.4"
```

These version requirements match `pyproject.toml`. To install the locked
versions from `uv.lock` instead, use uv:

```bash
uv sync --locked --no-dev
```

### 3. Create and configure a Discord bot

1. Visit the [Discord Developer Portal](https://discord.com/developers/applications).
2. Create an application and open its **Bot** settings.
3. Generate or reset the bot token and copy it for the next step.
4. Configure a server installation with the `bot` and `applications.commands`
   scopes, following [Discord's app setup guide](https://docs.discord.com/developers/quick-start/getting-started).
5. Invite the bot using a server member account with **Manage Server**
   permission, as required for a
   [server installation](https://docs.discord.com/developers/resources/application#installation-context).
   In server text channels, members running commands need **View Channels**,
   **Send Messages**, and **Use Application Commands**. Channel overwrites
   and [application command permissions](https://docs.discord.com/developers/interactions/application-commands#permissions)
   can restrict access. See also the
   [Discord team's explanation of command invocation permissions](https://github.com/discord/discord-api-docs/discussions/5097).

For the current slash commands, no additional bot-role permissions need to
be requested at installation (`permissions=0`). Text and embed responses
use [interaction responses](https://docs.discord.com/developers/interactions/receiving-and-responding#responding-to-an-interaction),
whose permission rules differ from ordinary channel message sends. See
[Discord's interaction and webhook permission notes](https://docs.discord.com/developers/change-log#changes-to-bot-permissions-for-interactions-and-webhooks).
The bot does not need **Administrator** permission.

To receive the welcome embed, configure a system channel in the server's
settings and allow the bot **View Channel**, **Send Messages**, and **Embed
Links** in that channel. The greeting uses a normal channel message, so the
[channel message permissions](https://docs.discord.com/developers/resources/message#create-message)
apply. Check both the bot's roles and the channel's permission overwrites.
If no system channel is configured, the greeting is skipped. Permission
errors are logged as warnings; other HTTP failures are logged with tracebacks.

The bot uses the default Gateway intents. The current slash commands do not
require **Message Content Intent**, **Server Members Intent**, or
**Presence Intent**; all three privileged intents can remain disabled.
See the [discord.py intents guide](https://discordpy.readthedocs.io/en/stable/intents.html#message-content)
for details.

### 4. Configure the environment

Create a file named `.env` in the project directory:

```env
TOKEN=your_bot_token_here
```

Replace `your_bot_token_here` with your bot token. Keep the token private and
do not commit `.env` to Git; the project's `.gitignore` already excludes it.

You can also set `TOKEN` directly as an environment variable. Existing
environment variables take precedence over values loaded from `.env`, as
described in the [python-dotenv documentation](https://github.com/theskumar/python-dotenv#readme).

If `TOKEN` is missing, empty, or contains only whitespace, the bot displays
an error message and exits with status code `1`.

### 5. Run the bot

From the project directory, run:

```bash
python src/bot.py
```

If you installed the dependencies with uv, run the bot in the project's
virtual environment:

```bash
uv run --locked --no-dev python src/bot.py
```

For extension loading and startup log details, see the [Development Guide](DEVELOPMENT.md).

Once the bot is running, try `/commands`, `/help`, `/ping`, and `/roll maximum:6`
in your server. The `!help` prefix command is disabled; use `/help` for the
command list or `/commands` for command details.
