from typing import Dict


class EventObject:
    def __init__(self):
        self._listeners: Dict = {}

    def add_listener(self, event_name: str, listener: callable):
        if event_name not in self._listeners:
            self._listeners[event_name] = []

        self._listeners[event_name].append(listener)

    def emit(self, event_name: str, *args, **kwargs):
        if event_name in self._listeners:
            for listener in self._listeners[event_name]:
                listener(*args, **kwargs)
