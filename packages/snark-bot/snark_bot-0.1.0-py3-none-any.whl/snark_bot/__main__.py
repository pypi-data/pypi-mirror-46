from slack import RTMClient
from smart_getenv import getenv

from snark_bot.bot import SlackBot


name = getenv("SLACK_BOT_NAME", type=str)
token = getenv("SLACK_BOT_TOKEN", type=str)
pattern = getenv("SLACK_BOT_RESPONSE_PATTERN", type=str)
remarks_location = getenv("SNARKY_REMARKS_LOCATION", type=str)

bot = SlackBot(name, pattern, remarks_location, token=token)


@RTMClient.run_on(event="message")
def _message_trigger(**kwargs):
    bot.process_message(**kwargs)


if __name__ == "__main__":
    bot.start()
