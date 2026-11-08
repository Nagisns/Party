# Command Guide

[English](COMMANDS.md) | [日本語](../ja/COMMANDS.ja.md)

[README](../../README.md) | [Setup](SETUP.md) | [Development](DEVELOPMENT.md)

## Commands

| Command | Description |
|---|---|
| `/commands` | Displays a command reference with navigation buttons. |
| `/help` | Displays an embed listing the registered slash commands and their descriptions. |
| `/ping` | Displays the bot's WebSocket latency in milliseconds. |
| `/roll` | Rolls one die with the specified number of sides and displays the result in an embed. |

The commands listed above can be selected from Discord's slash command picker.
The `/commands`, `/help`, and `/ping` commands take no arguments.

### Roll

The `/roll` command requires `maximum`, an integer from **2 to 1000** specifying the number of
sides. The result is an integer from **1 through `maximum`**, inclusive.

For example, to roll a six-sided die:

```text
/roll maximum:6
```

### Command Reference

The `/commands` reference opens with a table of contents, followed by detail
pages for `/help`, `/ping`, and `/roll`. Use the left and right arrow buttons
to move between pages. Navigation wraps from the first page to the last and
from the last page to the first. Page changes update the same message in the
channel, and anyone who can view it can use its buttons.

After 180 seconds of inactivity, the navigation buttons are disabled and the
message shows an expiration notice in the language of the user who opened
the reference. Run `/commands` again to open a new reference. Each user can
run `/commands` once every five seconds.

## Cooldowns

Each of `/commands`, `/help`, and `/ping` has a per-user cooldown of one use
every five seconds. The `/roll`
command allows three uses per user every ten seconds. Each command has its
own cooldown.

## Language

Japanese users receive Japanese command and argument descriptions, command
reference page titles, descriptions, and expiration notices, help and roll
embed titles, ping responses, and error messages. Other Discord language
settings use English.
Messages without a Japanese translation also use the original English text.
The command names remain `/commands`, `/help`, `/ping`, and `/roll` in both
languages. The `/commands` reference keeps the language of the user who
opened it throughout navigation, including when another user presses a button.

## Welcome Message

The welcome embed is visible in the system channel and is sent when the bot
joins a server. Its title and description use Japanese when
`guild.preferred_locale` is Japanese (`ja`), and English for other locales.
Discord defines this as a Community guild's preferred locale and defaults
it to `en-US`; see the
[guild structure documentation](https://docs.discord.com/developers/resources/guild#guild-object-guild-structure).

## Response Visibility

Normal command responses are visible in the channel. If measuring ping
raises `OverflowError` or `ValueError`, including for `NaN` latency, the
failure message is also visible in the channel.

Command errors are visible only to the user who ran the command.
For error handling and log details, see the [Development Guide](DEVELOPMENT.md).
