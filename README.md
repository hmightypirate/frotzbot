# Frotzbot

A maubot that allows you to play classic adventure text interactive fiction games

The bot uses Jericho https://github.com/microsoft/jericho for running the games. All games supported by Jericho will be run by this bot (basically all .z1 to .z6 z-machine games)

# Preparation

1) Install and build maubot following the instructions in https://docs.mau.fi/maubot/usage/setup/index.html

2) Get a token for your bot user using *mbc* https://docs.mau.fi/maubot/usage/cli/auth.html

3) Upload the plugin to maubot:

```
mbc build --upload
```

4) Create a client using the web server of maubot using the bot credentials

5) Instantiate the plugin (before this step, check the plugin configuration section)

## Dependencies

The plugin has several external dependencies. You can install them with:

```
pip install -r requirements.txt
```


# Plugin Configuration

*base-config.yaml* contains the base configuration of the plugin:


* *game_path* is the path to your game relative to maubot (games are not included in the plugin)
* *languages* are the language profiles that will be used in the chat. The bot discards messages that are not written in english (it uses langid for the language detection of the message)
* *accepted_actions*: this is a whitelist of actions that are not correctly detected by the language detection algorithm
* *discarded_actions*: this is a blacklist of actions that should always be discarded
* *reset_command_list*: a list of commands that allow you to reset the game



## Configuration Updates

If *game_path* is changed after the plugin in instantiated the game will reset in the next valid action. 











