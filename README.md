# rss-to-tg

Requires Python 3.4.

```
usage: rss-to-tg.py [-h] [-t TIME] [-p PRELOAD] [-z SOURCETZ] [-l LOCALTZ]
                    [-v] [--message-format MSGFORMAT] [--parse-mode PARSEMODE]
                    [--time-format TIMEFMT]
                    address destination_id token

Sends RSS messages to a Telegram chat/channel.

positional arguments:
  address               The address of the RSS feed.
  destination_id        The ID (or username, dependent on the type of
                        conversation) to be used as a destination
  token                 The Telegram bot API token to be used.

optional arguments:
  -h, --help            show this help message and exit
  -t TIME               The amount of seconds between each request to the RSS
                        feed
  -p PRELOAD            The amount of seconds in the past that posts must be
                        in order to be sent in the first iteration.
  -z SOURCETZ           The timezone used in the RSS feed.
  -l LOCALTZ            The timezone to be used for the time in the message.
  -v                    Enable verbosity
  --message-format MSGFORMAT
                        The final message. Will be passed on to format(). Read
                        telegram.py for more info.
  --parse-mode PARSEMODE
                        The parse mode to be used by Telegram.
  --time-format TIMEFMT
                        The formatting for the time in the message. Uses
                        strftime(), so https://docs.python.org/2/library/time.
                        html#time.strftime contains more info.
```
