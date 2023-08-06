import re
import random

from slack import RTMClient, WebClient


class SlackBot(object):
    def __init__(self, name: str, pattern: str, remarks_location: str, **kwargs):
        self.name = name
        self.pattern = pattern
        self.remarks_location = remarks_location

        self.slack_id = None
        self._rtm_client = RTMClient(**kwargs)
        self.slack_client = WebClient(**kwargs)

        self.remarks = self.get_file_contents()

    def start(self):
        self._rtm_client.start()

    def process_message(self, **kwargs):
        data = kwargs.get("data")
        text = data.get("text")

        if text:
            match = re.match(self.pattern, text, re.I)
            if match is not None:
                channel_id = data.get("channel")
                thread_ts = data.get("ts")

                self.slack_client.chat_postMessage(
                    channel=channel_id,
                    thread_ts=thread_ts,
                    text=self.get_random_response(),
                )

    def get_file_contents(self) -> list:
        with open(self.remarks_location) as file:
            return file.readlines()

    def get_random_response(self) -> str:
        remarks_length = len(self.remarks)

        return self.remarks[random.randint(0, remarks_length - 1)]
