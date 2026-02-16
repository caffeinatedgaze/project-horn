from collections.abc import Iterable


class FakeSource:
    def __init__(self, events: Iterable[object]):
        self.events = list(events)

    def __iter__(self):
        return iter(self.events)
