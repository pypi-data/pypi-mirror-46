from requests import post
import json

ROBOT_LISTENER_API_VERSION = 2


class GuiStatusListener(object):
    ROBOT_LISTENER_API_VERSION = 2

    def _postrequest(self, payload):
        self.queue.append(payload)
        current = None
        try:
            while self.queue:
                current = self.queue.pop()
                post(self.endpoint, json=json.dumps(current))
        except:  # noqa: E722
            if current is not None:
                self.queue.append(current)

    def __init__(self, endpoint="http://127.0.0.1:31337"):
        self.queue = []
        self.endpoint = endpoint

    def start_suite(self, name, attrs):
        self._postrequest({"suite_text": f"Running {name}"})

    def end_suite(self, name, attrs):
        self._postrequest({"suite_text": f"Done {name}"})

    def start_test(self, name, attrs):
        self._postrequest({"task_text": f"Running {name}"})

    def end_test(self, name, attrs):
        self._postrequest({"task_text": f"Running {name}"})

    def start_keyword(self, name, attrs):
        self._postrequest({"keyword_text": f"Running {name}"})

    def end_keyword(self, name, attrs):
        self._postrequest({"keyword_text": f"Done {name}"})

    def log_message(self, message):
        self._postrequest({"log_text": f"{message['message']}"})

    def close(self):
        pass
