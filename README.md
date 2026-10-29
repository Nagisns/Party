# Party

A Discord bot built with Python and `discord.py`, featuring slash commands
and Japanese localization.

The current release is **0.1.1**. The project is in prerelease development.
See the [changelog](CHANGELOG.md) for release history.

## Features

- **Help:** Displays an embed listing the available slash commands.
- **Ping:** Shows the bot's WebSocket latency in milliseconds.
- **Japanese Localization:** Displays command descriptions and responses in
  Japanese when the user's Discord language is set to Japanese.
- **Error Messages:** The shared slash command error handler sends localized
  error messages visible only to the user who ran the command.

## Commands

| Command | Description |
|---|---|
| `/help` | Displays an embed listing the registered slash commands and their descriptions. |
| `/ping` | Displays the bot's WebSocket latency in milliseconds. |

Both commands can be selected from Discord's slash command picker and take
no arguments.

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
5. Invite the bot to your server. Allow **View Channels**, **Send Messages**,
   and **Embed Links** in the channel where you intend to use it. Users also
   need **Use Application Commands** permission. See the
   [Discord permissions reference](https://docs.discord.com/developers/topics/permissions).

The current slash commands do not read message content, so they do not
require **Message Content Intent**. The bot uses the default gateway intents.
See the [discord.py intents guide](https://discordpy.readthedocs.io/en/stable/intents.html#message-content)
for details about that intent.

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

Once the bot is running, use `/help` or `/ping` in your server.

## Testing

This prerelease does not include an automated test suite. To check the bot
manually after setup:

1. Start the bot and confirm that the console reports two synchronized
   commands and a successful login.
2. Run `/help` and confirm that the embed lists `/help` and `/ping` with
   their descriptions.
3. Run `/ping` and confirm that the response includes latency in milliseconds.
4. Set your Discord language to Japanese and repeat the commands to check
   the translated descriptions, help title, and ping response.

## Localization and Error Handling

Japanese users receive Japanese command descriptions, help titles, ping
responses, and error messages. Other Discord language settings use English.
Messages without a Japanese translation also use the original English text.
The command names remain `/help` and `/ping` in both languages.

Normal command responses are visible in the channel. If measuring ping
raises `OverflowError`, the failure message is also visible in the channel.
The shared slash command error handler sends error messages only to the
user who ran the command, using a follow-up message if the interaction has
already received a response. Unexpected command errors are logged to the
console with tracebacks.

The error handler has dedicated messages for missing permissions and
command cooldowns, plus a general message for unexpected errors. Neither
command currently has custom permission checks. Each command has a per-user
cooldown of one use every five seconds.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE)
file for details.

## Acknowledgements

- [discord.py](https://discordpy.readthedocs.io/)
- [python-dotenv](https://github.com/theskumar/python-dotenv)

This README was written with assistance from ChatGPT.
