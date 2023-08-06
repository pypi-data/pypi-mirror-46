import datetime
import json
from inspect import getframeinfo, stack

from discord_webhook import DiscordWebhook

from smartlogging.message import Message


class SmartLogger:

    Message.create_table()

    def __init__(self, discord_url=None):
        self.discord_url = discord_url
        self.message = None
        self.message_json = None
        self.message_dict = None

    @staticmethod
    def wipe_log():
        Message.drop_table()
        Message.create_table()

    @staticmethod
    def wipe_feed():
        pass

    @staticmethod
    def get_feed(feed):
        feed_messages = Message.select().where(Message.feed == feed)
        return [{"message": x.message, "feed": x.feed, "created": x.created} for x in feed_messages]

    @staticmethod
    def get_log():
        return [{"message": x.message, "feed": x.feed, "created": x.created} for x in Message.select()]

    def ping_discord(self):
        webhook = DiscordWebhook(url=self.discord_url,
                                 content="{} , on feed: {}, at: {}".format(self.message_dict["message"],
                                                                           self.message_dict["feed"],
                                                                           self.message_dict["created"]))
        webhook.execute()

    def log(self, message, feed, discord_push=False, tracking=True):
        if tracking:
            caller = getframeinfo(stack()[1][0])
            message = message + " called in: {} on line: {}".format(caller.filename, caller.lineno)
        now = datetime.datetime.now()
        self.message = Message.create(message=message, feed=feed, created=now)
        self.message.save()
        self.message_dict = {
            "message": message,
            "feed": feed,
            "created": now
        }
        if discord_push:
            self.ping_discord()
        json_package = self.message_dict
        json_package["created"] = json_package["created"].strftime("%m/%d/%Y, %H:%M:%S")
        self.message_json = json.dumps(json_package)


if __name__ == "__main__":
    web_url = 'https://discordapp.com/api/webhooks/569139126637428737/3vwjDtslpPIvF3yZUKkreCM0oihU7LnAGKo8wWawCAGs4TVk5DTrsH3AkgE71Sd7T-BN'

    test = SmartLogger(discord_url=web_url)
    test.log(message="this is a test", feed="two")
    print(test.message_json)
    print(test.message_dict)
    # print(test.get_log())
    # print(test.get_feed(feed="one"))
