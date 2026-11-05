# Party

[English](README.md) | [日本語](README.ja.md)

A Discord bot built with Python and `discord.py`, featuring slash commands
and Japanese localization.

The current release is **0.2.1**. The project is in prerelease development.
See the [changelog](CHANGELOG.md) for release history.

## Features

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

During startup, the bot discovers and loads command extensions from
`src/cogs/` and event extensions from `src/events/`, registers its Japanese
translator, and synchronizes its global slash commands. The console reports
the total number of registered Cog event listeners, the number of synchronized
commands, and the logged-in bot. The listener count includes each registered
listener, including multiple listeners for the same event.

Once the bot is running, use `/help`, `/ping`, or `/roll maximum:6` in your
server. The `!help` prefix command is disabled; use `/help` for the command
list.

## Adding Commands

Commands are organized as Cog extensions in `src/cogs/`. At startup, the bot
discovers modules and packages directly inside `cogs` and loads them in
alphabetical order. Names beginning with `_` are excluded, so use that prefix
for helper modules that should not be loaded as extensions.

To add a command, create a module such as `src/cogs/example.py`, define its
Cog and commands, and expose an `async def setup(bot)` entry point that calls
`await bot.add_cog(...)`. Restart the bot to discover the new extension and
synchronize its commands; no changes to `src/mybot.py` are needed.

Every discovered extension must provide the setup entry point. If an
extension fails to load, startup stops before command synchronization.

## Adding Event Listeners

Event listeners are organized as Cog extensions in `src/events/`. Mark each
listener with `commands.Cog.listener()` and expose an `async def setup(bot)`
entry point that registers the Cog with `await bot.add_cog(...)`. Use a unique
Cog name, and remove the original handler when moving an event from `bot.py`
to avoid running both handlers.

At startup, command extensions load first, followed by event extensions.
Modules and packages directly inside each directory load in alphabetical
order, and names beginning with `_` are excluded. Restart the bot to discover
new event extensions; no changes to `src/mybot.py` are needed. Event listeners
are registered when their Cogs are added and do not require `tree.sync()`.

## Testing

This prerelease does not include an automated test suite. To check the bot
manually after setup:

1. Start the bot and confirm that the console reports
   `Registered 2 event listeners.` and `Synced 3 commands.`,
   followed by a successful login.
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
9. With the bot running, invite it to a test server with a configured system
   channel and the required greeting permissions. Confirm that exactly one
   welcome embed appears in that channel. Repeat with a server whose preferred
   locale is Japanese and one with another locale; check that the title and
   description use Japanese and English respectively.
10. Check a test server without a system channel and one where the bot cannot
    send messages to the system channel. Confirm that joining produces no
    greeting in those cases and that a permission failure is logged as a
    warning. The bot should continue responding to slash commands.

When adding an extension, restart the bot and confirm that its commands or
event listeners are registered without editing `src/mybot.py`. Check that
helper modules whose names begin with `_` are not loaded as extensions. For a
new event listener, check the listener count and trigger the corresponding
event. To verify these steps, use a test bot and server so command
synchronization does not affect an existing deployment.

## Localization and Error Handling

Japanese users receive Japanese command and argument descriptions, help
and roll embed titles, ping responses, and error messages. Other Discord
language settings use English. Messages without a Japanese translation
also use the original English text. The command names remain `/help`,
`/ping`, and `/roll` in both languages.

The welcome embed is visible in the system channel and is sent when the bot
joins a server. Its title and description use Japanese when
`guild.preferred_locale` is Japanese (`ja`), and English for other locales.
Discord defines this as a Community guild's preferred locale and defaults
it to `en-US`; see the
[guild structure documentation](https://docs.discord.com/developers/resources/guild#guild-object-guild-structure).
Greeting permission errors are logged as warnings; other HTTP delivery
failures are logged with tracebacks. These failures do not stop the bot from
serving commands.

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
