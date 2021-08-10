import re
import os
import logging
import yaml
import jericho
import langid
from attr import dataclass
from mautrix.types import EventType, MessageType, UserID, RoomID
from mautrix.util.config import BaseProxyConfig
from maubot import Plugin, MessageEvent
from maubot.handlers import command
from maubot.handlers import event
from typing import Type, Tuple, Dict
from mautrix.util.config import BaseProxyConfig, ConfigUpdateHelper


logger = logging.getLogger(__name__)


class Config(BaseProxyConfig):
    def do_update(self, helper: ConfigUpdateHelper) -> None:

        logger.info("HELPER BASE {}".format(helper.base))
        logger.info("HELPER CONFIG {}".format(helper.source))
      
        helper.copy("game_path")
        helper.copy("languages")
        helper.copy("accepted_actions")
        helper.copy("discarded_actions")
        helper.copy("reset_command_list")


class JerichoBot(Plugin):

    allowed_msgtypes: Tuple[MessageType, ...] = (MessageType.TEXT, MessageType.EMOTE)
    env: None
    
    async def start(self) -> None:
        await super().start()

        self.config.load_and_update()

        logger.info("FILES {}".format(os.getcwd()))
        
        langid.set_languages(self.config["languages"])  # ISO 639-1 codes      
        self.env = jericho.FrotzEnv(self.config["game_path"])
        self.first_message = True
    
    @event.on(EventType.ROOM_MESSAGE)
    async def event_handler(self, evt: MessageEvent) -> None:

        logger.debug("Received message {} WTF".format(evt))

        if (evt.sender == self.client.mxid or
            evt.content.msgtype != MessageType.TEXT):
            # FIXME: discarded emotes: not in self.allowed_msgtypes):
            return

        logger.debug("Evt content {}".format(evt.content))
        logger.debug("Evt content/Body {}".format(evt.content.body))
        logger.debug("Config {}".format(self.config))
                             
        action = evt.content.body

        logger.debug("Action {}".format(action))

        # discard non alphanumeric characters
        action = re.sub(r'[^a-zA-Z0-9? ]', '', action)
        action = action.strip()
        
        if len(action) == 0:
            return
        
        # Check if action should be discarded
        if action.lower() in self.config["discarded_actions"]:
            logger.info("Discarded action {}-filtered".format(action))
            return

        # Check if action should be dicarded by language 
        if action.lower() not in self.config["accepted_actions"]:
            lang, score = langid.classify(action)
            
            if lang != "en":
                logger.info("Discarded action {}-{}".format(action, lang))
                return

        # if it is the first message
        if self.first_message:
            observation, info = self.env.reset()

            self.first_message = False

        elif action in self.config["reset_command_list"]:
            observation, info = self.env.reset()
            
        elif self.env.story_file != self.config["game_path"].encode('utf-8'):
            # Game configuration has changed
            self.env = jericho.FrotzEnv(self.config["game_path"])
            observation, info = self.env.reset()

        else:
            # The resulting text-observation, reward, and game-over indicator is returned.
            observation, reward, done, info = self.env.step(action)
            # Total score and move-count are returned in the info dictionary
                           
        await evt.reply(observation)

    @classmethod
    def get_config_class(cls) -> Type[BaseProxyConfig]:
        return Config
