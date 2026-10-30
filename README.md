# Party

A Discord bot built with Python and `discord.py`, featuring slash commands
and Japanese localization.

The current release is **0.1.2**. The project is in prerelease development.
See the [changelog](CHANGELOG.md) for release history.

## Features

- **Help:** Displays an embed listing the available slash commands.
- **Ping:** Shows the bot's WebSocket latency in milliseconds.
- **Roll:** Rolls a die with 2 to 1000 sides and displays the result in an embed.
- **Japanese Localization:** Displays command and argument descriptions and
  responses in Japanese when the user's Discord language is set to Japanese.
- **Error Messages:** The shared slash command error handler sends localized
  error messages visible only to the user who ran the command.

## Commands

| Command | Description |
|---|---|
| `/help` | Displays an embed listing the registered slash commands and their descriptions. |
| `/ping` | Displays the bot's WebSocket latency in milliseconds. |
| `/roll` | Rolls one die with the specified number of sides and displays the result in an embed. |

All three commands can be selected from Discord's slash command picker.
The `/help` and `/ping` commands take no arguments. The `/roll` command
requires `maximum`, an integer from **2 to 1000** specifying the number of
sides. The result is an integer from **1 through `maximum`**, inclusive.

For example, to roll a six-sided die:

```text
/roll maximum:6
```

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

During startup, the bot registers its Japanese translator and synchronizes
its global slash commands. The console reports the number of synchronized
commands and the logged-in bot.

Once the bot is running, use `/help`, `/ping`, or `/roll maximum:6` in your
server. The `!help` prefix command is disabled; use `/help` for the command
list.

## Testing

This prerelease does not include an automated test suite. To check the bot
manually after setup:

1. Start the bot and confirm that the console reports three synchronized
   commands and a successful login.
2. Run `/help` and confirm that the embed lists `/help`, `/ping`, and `/roll`
   with their descriptions.
3. Run `/ping` and confirm that the response includes latency in milliseconds.
4. Run `/roll maximum:2` and `/roll maximum:1000`. Confirm that each result
   appears in an embed and is between 1 and the specified maximum, inclusive.
5. Confirm that the command picker requires `maximum` and rejects values
   below 2 or above 1000.
6. Wait for any earlier cooldowns to expire. Run `/help` or `/ping` twice
   within five seconds, and `/roll` four times within ten seconds. Confirm
   that exceeding each command's limit returns an error visible only to you.
7. Set your Discord language to Japanese and repeat the commands. Check the
   command descriptions, the `maximum` option description, help and roll
   embed titles, ping response, and cooldown messages.
8. Send `!help` and confirm that the bot does not respond to that prefix
   command.

## Localization and Error Handling

Japanese users receive Japanese command and argument descriptions, help
and roll embed titles, ping responses, and error messages. Other Discord
language settings use English. Messages without a Japanese translation
also use the original English text. The command names remain `/help`,
`/ping`, and `/roll` in both languages.

Normal command responses are visible in the channel. If measuring ping
raises `OverflowError` or `ValueError`, including for `NaN` latency, the
failure message is also visible in the channel.
The shared slash command error handler sends error messages only to the
user who ran the command, using a follow-up message if the interaction has
already received a response. Unexpected command errors are logged to the
console with tracebacks.

The error handler has dedicated messages for missing permissions and
command cooldowns, plus a general message for unexpected errors. None of
the commands currently has custom permission checks. Each of `/help` and
`/ping` has a per-user cooldown of one use every five seconds. The `/roll`
command allows three uses per user every ten seconds. Each command has its
own cooldown.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE)
file for details.

## Acknowledgements

- [discord.py](https://discordpy.readthedocs.io/)
- [python-dotenv](https://github.com/theskumar/python-dotenv)

This README was written with assistance from ChatGPT.
