galatea-hal
=============

## Overview
Galatea Hal is our own internal bot for common tasks.  

Hal is hosted on BeepBoop. Visit [Beep Boop](https://beepboophq.com/docs/article/overview) to get the scoop on the the Beep Boop hosting platform. 

### First Conversations

Here is an example interaction dialog that works with this bot:
```
Joe Dev [3:29 PM]
hi @hal

Hal BOT [3:29 PM]
Nice to meet you, @hal!

Joe Dev [3:30 PM]
help @hal

Hal BOT [3:30 PM]
I'm your friendly Slack bot written in Python.  I'll ​*​_respond_​*​ to the following commands:
>`hi @hal` - I'll respond with a randomized greeting mentioning your user. :wave:
> `@hal joke` - I'll tell you one of my finest jokes, with a typing pause for effect. :laughing:
> `@hal attachment` - I'll demo a post with an attachment using the Web API. :paperclip:

Joe Dev [3:31 PM]
@hal: joke

Hal BOT [3:31 PM]
Why did the python cross the road?

[3:31]
To eat the chicken on the other side! :laughing:
```

## Development
I hear you want to contribute to hal.  Awesome.  Here are some guidelines.

### Assumptions
We assume you understand the following:
- How to develop in Python2 
  - Make sure to download latest version of Python 2.x.  https://www.python.org/downloads/
  - You can use your favorite editor.  I like community edition of pycharm:  https://www.jetbrains.com/pycharm/download/#section=windows) 
- How to interact with GitHub. 
  - This is a good set up guide:  https://help.github.com/articles/set-up-git/
- What docker is
- The slack realtime API:  https://api.slack.com/rtm  
- How BeeBoop works: https://beepboophq.com/docs 
- How Wit.wi works: https://wit.ai/

### Dev Process
- Ask Raj to add you as a collaborator
- Fork this repository
- Make your changes
- Test your changes
- Send Raj a pull request

### Code Organization
If you want to add or change an event that the bot responds (e.g. when the bot is mentioned, when the bot joins a channel, when a user types a message, etc.), you can modify the `_handle_by_type` method in `event_handler.py`.

The `slack_clients.py` module provides a facade of two different Slack API clients which can be enriched to access data from Slack that is needed by your Bot:

1. [slackclient](https://github.com/slackhq/python-slackclient) - Realtime Messaging (RTM) API to Slack via a websocket connection.
2. [slacker](https://github.com/os/slacker) - Web API to Slack via RESTful methods.

The `slack_bot.py` module implements and interface that is needed to run a multi-team bot using the Beep Boop Resource API client, by implementing an interface that includes `start()` and `stop()` methods and a function that spawns new instances of your bot: `spawn_bot`.  It is the main run loop of your bot instance that will listen to a particular Slack team's RTM events, and dispatch them to the `event_handler`.

### Testing locally (on windows)

Create a bot for yourself to test hal:  https://galaslack.slack.com/apps/manage/A0F7YS25R-bots .  This bot should be called test-hal-<your name> (e.g. test-hal-raj).  This will ensure that your changes don't break production hal.  Note: be polite and disable your bot when you are not using it.

To start your local version of hal, run the following steps:
- cd to your project root folder (i.e. where you have requirements.txt)
- pip install -r requirements.txt
- set SLACK_TOKEN=[YOUR TEST HAL BOT's SLACK TOKEN]
- set WIT_ACCESS_TOKEN=[YOUR WIT ACCESS TOKEN]
- python ./bot/app.py

Things are looking good if the console prints something like:

	Connected <your bot name> to <your slack team> team at https://<your slack team>.slack.com.

If you want change the logging level, also `set LOG_LEVEL=<your level>`

### Deploying to prod
Changes pushed to the remote master branch will automatically deploy a new version of hal

## License

See the [LICENSE](LICENSE.md) file for license rights and limitations (MIT).
