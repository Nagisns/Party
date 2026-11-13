# Development Guide

[English](DEVELOPMENT.md) | [日本語](../ja/DEVELOPMENT.ja.md)

[README](../../README.md) | [Setup](SETUP.md) | [Commands](COMMANDS.md)

Complete the [Setup Guide](SETUP.md) before adding extensions or running manual checks.

## Development Environment

The project's minimum Python requirement is 3.15. The
[`.python-version`](../../.python-version) file pins Python 3.15.2 for local
development. With uv installed, create the environment and install runtime
and development dependencies from the lockfile:

```bash
uv sync --locked
```

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

The command guide uses the `GuidePage` `IntEnum` in `src/cogs/commands.py`.
`HOME` is zero and the remaining values use `auto()`. Navigation derives its
bounds from `GuidePage.HOME.value` and `len(GuidePage)`; display branches compare
against named members. When adding a guide page, update the enum, its display
branch, the table of contents, and the corresponding Japanese translation keys.
The current guide has five pages, including the home page and poll details.

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
The ready event uses a module logger to record `Logged in as ...`, `Servers:`,
`Users:`, and `Gateway latency:` at the same level. Finite latency is shown in
milliseconds to two decimal places; otherwise it is reported as `unavailable`.
These messages can appear again after a reconnect.

`Users:` is the sum of available `guild.member_count` values, including bots
and counting members of multiple servers once per server. Servers whose count
is `None` are skipped. It is not a unique-user count, and without the members
intent the cached counts are not guaranteed to remain current; see
[`Guild.member_count`](https://discordpy.readthedocs.io/en/stable/api.html#discord.Guild.member_count).

Greeting permission errors are logged as warnings; other HTTP delivery
failures are logged with tracebacks. These failures do not stop the bot from
serving commands.

`src/error_handler.py` defines `ErrorHandler`. `src/bot.py` creates an instance
and registers its bound `on_app_command_error` method with `bot.tree.error()`
before startup. The shared handler sends error messages only to the user who
ran the command, using a follow-up message if the interaction has
already received a response. Unexpected command errors are logged to the
console with tracebacks.
HTTP failures when sending these error responses are also logged with
tracebacks.

`CommandsView.on_error()` handles errors from guide button callbacks and
interaction checks. It logs the exception, translates the notification using
the language of the user who pressed the button, and calls
`ErrorHandler.send_error_message()`. That helper handles initial responses,
follow-ups after `defer()`, and HTTP failures while sending the notification.
Timeout updates keep their own handling: missing messages are ignored and
other HTTP failures are logged.

Page navigation holds a lock while calculating the candidate page, creating
its embed, sending the update, and committing the page index. `create_embed(page)`
uses the supplied index without modifying the current page. A failed update
therefore leaves the current page index unchanged.

The error handler has dedicated messages for missing permissions and
command cooldowns, plus a general message for unexpected errors. None of
the commands currently has custom permission checks.

## Testing

### Automated Tests

The pytest suite in `tests/` checks server count logging and command guide
page state after failed message updates in both navigation directions.
After installing the development dependencies as described above, run this
command from the project root:

```bash
uv run --locked pytest -v
```

GitHub Actions runs the suite on pushes to `develop` and pull requests
targeting `develop`. The tests use mocked bot and interaction objects.
Use the manual checks below to verify behavior in Discord.

### Manual Checks

After setup, check the bot manually:

1. Start the bot and confirm that the console shows `INFO` logs reporting
   the registered event listener and synchronized command counts,
   followed by the logged-in bot, server count, summed available member counts,
   and Gateway latency or `unavailable`.
2. Run `/help` and confirm that the embed lists `/commands`, `/help`, `/ping`,
   `/roll`, and `/poll` with their descriptions.
3. Run `/commands` and confirm that the reference opens at `page: 1/5`.
   Use both arrow buttons to visit all five pages, including navigation from
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
   and `/ping` twice within five seconds, `/roll` four times within ten
   seconds, and `/poll` twice within ten seconds. Confirm that exceeding each
   command's limit returns an error
   visible only to you.
8. Set your Discord language to Japanese and repeat the commands. Check the
   command descriptions, the `maximum` option description, command reference
   page titles and descriptions on all five pages, help and roll embed titles,
   ping response, poll command and all five parameter descriptions, and cooldown
   messages. Wait for the reference to time out
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
12. Create a poll with only `question`, `option1`, and `option2`. Confirm two
    answers, a 24-hour duration, and single-choice voting. Repeat with `option3`
    and with `hour:1` and `hour:240`; check the third answer and the end time.
    The bot should preserve the question and answer text as entered.
13. Check the poll input boundaries: `question` accepts 1–300 characters,
    each answer accepts 1–55 characters, and `hour` accepts integers from 1 to 240.
    Confirm that the question and first two answers are required, `option3` and
    `hour` can be omitted, and the picker rejects out-of-range values.

### Page Update Failure Checks

Use mocked interactions in separate test code for these checks.

- Make `interaction.response.defer()` succeed and
  `interaction.edit_original_response()` raise `discord.HTTPException` once.
  For each direction, verify that `view.page` is unchanged after the exception.
  Let the next update succeed and confirm that it moves one page from the last
  successful state, including first/last-page wrapping.
- When calling a button callback directly, pass its exception to `view.on_error()`
  explicitly; discord.py normally does this during dispatch. Check that the
  exception is logged and an ephemeral follow-up uses the clicking user's language.
  Also test an interaction without an initial response, where the helper should
  use `interaction.response.send_message()`.
- Make the notification send raise an HTTP exception and check the failure log.
  Delay one page update while starting another; confirm the second waits for the
  lock and uses the last successfully committed page index.

When adding an extension, restart the bot and confirm that its commands or
event listeners are registered without editing `src/mybot.py`. Check that
helper modules whose names begin with `_` are not loaded as extensions. For a
new event listener, check the listener count and trigger the corresponding
event. To verify these steps, use a test bot and server so command
synchronization does not affect an existing deployment.
