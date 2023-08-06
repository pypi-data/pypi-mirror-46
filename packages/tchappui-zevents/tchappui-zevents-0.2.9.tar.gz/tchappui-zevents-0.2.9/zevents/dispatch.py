# -*- coding: utf-8 -*-

"""Implements the decorators for easy subscriptions of methods to ZEvents
"""

from functools import wraps

def _subscribe_marked_events(instance):
    for key, obj in type(instance).__dict__.items():
        if hasattr(obj, "_zevents"):
            zevents = obj._zevents
            for zevent in zevents:
                zevent.subscribe(getattr(instance, key))

def listener(cls):
    """Class decorator to mark a class as a zevent listener."""
    func = cls.__init__

    # Wraps the class constructor to automate the subscription of methods to
    # event handlers
    @wraps(cls.__init__)
    def new_init(self, *args, **kwargs):
        _subscribe_marked_events(self)
        func(self, *args, **kwargs)

    # Patching the constructor
    cls.__init__ = new_init
    return cls

class Listener:
    """Mixin defining a class as a zevent listener."""

    def __init__(self):
        """Subscribes bound methods to the zevents they want to listen to."""
        _subscribe_marked_events(self)

