# slackbot
A simple python wrapper for the [Slack](https://slack.com) api

## Requirements

* [SlackClient](https://github.com/slackapi/python-slackclient)

## Installation

```
pip install simple-slackbot
```

## Usage

### Generate a slack api token

First you need to get the slack api token for your bot. You can create a bot on the [slack website](https://api.slack.com) and manage permissions.

### Instantiate a SlackBot

```
from slackbot import SlackBot

slackbot = SlackBot()
```

By default, the SlackBot retrieved the slack token from environment variable `SLACK_API_TOKEN`.
You can overwrite the default behaviour by instantiating with the `token` argument. 

If running it in a Jupyter notebook, instantiate with `run_async=True`.

### Send a message

You can send messages to any channel (using the channel name or id), or any user (just set `channel=@<username>`) 
`slackbot.send_message(channel='#general', message='Hello!')`

### Send a file

You can also send files over slack, to any channel or user.

`slackbot.send_file(channel='#general', file='<filepath>', message='Check out this file!')`

### More using the slack api directly

You can access methods from the raw slack client to use them directly.

`slackbot.client.chat_postMessage(...)`