# Development Guide

[English](DEVELOPMENT.md) | [日本語](../ja/DEVELOPMENT.ja.md)

[README](../../README.md) | [Setup](SETUP.md) | [Commands](COMMANDS.md)

Complete the [Setup Guide](SETUP.md) before adding extensions or running manual checks.

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

## Startup and Error Handling

During startup, the bot discovers and loads command extensions from
`src/cogs/` and event extensions from `src/events/`, registers its Japanese
translator, and synchronizes its global slash commands. The console reports
the total number of registered Cog event listeners, the number of synchronized
commands, and the logged-in bot. The listener count includes each registered
listener, including multiple listeners for the same event.
The listener and synchronized command counts are written as `INFO` logs.

Greeting permission errors are logged as warnings; other HTTP delivery
failures are logged with tracebacks. These failures do not stop the bot from
serving commands.

The shared slash command error handler sends error messages only to the
user who ran the command, using a follow-up message if the interaction has
already received a response. Unexpected command errors are logged to the
console with tracebacks.
HTTP failures when sending these error responses are also logged with
tracebacks.

The error handler has dedicated messages for missing permissions and
command cooldowns, plus a general message for unexpected errors. None of
the commands currently has custom permission checks.

## Testing

This prerelease does not include an automated test suite. To check the bot
manually after setup:

1. Start the bot and confirm that the console shows `INFO` logs reporting
   the registered event listener and synchronized command counts,
   followed by a successful login.
2. Run `/help` and confirm that the embed lists `/commands`, `/help`, `/ping`,
   and `/roll` with their descriptions.
3. Run `/commands` and confirm that the reference opens at `page: 1/4`.
   Use both arrow buttons to visit all four pages, including navigation from
   the first page to the last and back. Check the command details and page
   numbers, and click the buttons quickly to check that updates stay consistent.
   After 180 seconds without button activity, confirm that both navigation
   buttons are disabled and an expiration notice asks you to run `/commands`
   again. Run it again to open a new reference.
4. Run `/ping` and confirm that the response includes latency in milliseconds.
5. Run `/roll maximum:2` and `/roll maximum:1000`. Confirm that each result
   appears in an embed and is between 1 and the specified maximum, inclusive.
6. Confirm that the command picker requires `maximum` and rejects values
   below 2 or above 1000.
7. Wait for any earlier cooldowns to expire. Run each of `/commands`, `/help`,
   and `/ping` twice within five seconds, and `/roll` four times within ten
   seconds. Confirm that exceeding each command's limit returns an error
   visible only to you.
8. Set your Discord language to Japanese and repeat the commands. Check the
   command descriptions, the `maximum` option description, command reference
   page titles and descriptions on all four pages, help and roll embed titles,
   ping response, and cooldown messages. Wait for the reference to time out
   and confirm that its expiration notice is also in Japanese.
9. Send `!help` and confirm that the bot does not respond to that prefix
   command.
10. With the bot running, invite it to a test server with a configured system
    channel and the required greeting permissions. Confirm that exactly one
    welcome embed appears in that channel. Repeat with a server whose preferred
    locale is Japanese and one with another locale; check that the title and
    description use Japanese and English respectively.
11. Check a test server without a system channel and one where the bot cannot
    send messages to the system channel. Confirm that joining produces no
    greeting in those cases and that a permission failure is logged as a
    warning. The bot should continue responding to slash commands.

When adding an extension, restart the bot and confirm that its commands or
event listeners are registered without editing `src/mybot.py`. Check that
helper modules whose names begin with `_` are not loaded as extensions. For a
new event listener, check the listener count and trigger the corresponding
event. To verify these steps, use a test bot and server so command
synchronization does not affect an existing deployment.
