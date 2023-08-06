# -*- coding: utf-8 -*-

"""Implements the ZEvents core system.
"""

from collections import defaultdict, OrderedDict
from contextlib import contextmanager
import inspect
import queue
import re
import threading
import weakref


class EventManager:
    """Class responsible for the mechanics of event management.

    EventManager provides the interface to subscribe or unsubscribe a
    handler to or from the notification feed of events of different types. This
    class also provides the method to fire an event object.
    """

    def __init__(self):
        self._lock = threading.Lock()
        # Subscribers dictionnary. Keys are event types. Values are Orderdicts
        # of weakly-referenced functions or methods
        self._subscribers = defaultdict(OrderedDict)
        # Queues for pending subscriptions, unsubscription and notifications
        self._actions = queue.Queue()

    def notify(self, event):
        """Sends an event notification to all the subscribers."""
        self._actions.put(['_notify', type(event), event])
        # Process the queued subscriptions, unsubscriptions and notifications
        with self._non_blocking_lock() as locked:
            if locked: self._process_actions()

    def subscribe(self, event_type, handler):
        """Subscribes a handler function to the notification feed of a given
        event.
        """
        self._actions.put(['_subscribe', event_type, handler])

    def unsubscribe(self, event_type, handler):
        """Unsubscribes a handler function from the notification feed of a
        given event.
        """
        self._actions.put(['_unsubscribe', event_type, handler])

    def _process_actions(self):
        """Processes pending actions."""
        while not self._actions.empty():
            action, *args = self._actions.get()
            getattr(self, action)(*args)

    def _subscribe(self, event_type, handler):
        """Subscribes an event handler."""
        weak_handler = self._make_weakref(handler)
        # We subscribe the handler to all superclass events
        for klass in event_type.__mro__:
            if issubclass(klass, Event):
                self._subscribers[klass][weak_handler] = True

    def _unsubscribe(self, event_type, handler):
        """Unsubscribes an event handler."""
        weak_handler = self._make_weakref(handler)
        for klass in event_type.__mro__:
            if weak_handler in self._subscribers[klass]:
                del self._subscribers[klass][weak_handler]


    def _notify(self, event_type, event):
        """Notifies subscribers."""
        # We Empty the notification queue
        for weak_handler in self._subscribers[event_type]:
            handler = weak_handler()
            handler(event)

    def _make_weakref(self, handler):
        """Builds a weakref to a handler function or method."""
        # By default, suppose the handler is a function
        ref = weakref.ref
        # User WeakMethod if it is a bound method
        if inspect.ismethod(handler) and hasattr(handler, '__self__'):
            ref = weakref.WeakMethod
        return ref(handler)

    @contextmanager
    def _non_blocking_lock(self):
        """Context manager for non-blocking acquisition of self._lock."""
        locked = self._lock.acquire(blocking=False)
        try:
            yield locked
        finally:
            if locked:
                self._lock.release()


class Event:
    """Base class of all events in the notification system.

    Event is the base class used to create all the specialized events. It
    provides default implementations to send notification for the underlying
    event or to subscribe/unsubscribe to/from the notification feed of this
    particular event.
    """

    manager = EventManager()

    def __init__(self):
        """Initializes new events."""
        self.name = self._generate_event_name()

    def _generate_event_name(self):
        """Generates an event name."""
        parts = re.split(r"event", self.__class__.__name__, flags=re.I)
        parts = [part.strip() for part in parts if part.strip()]
        parts = parts + ["Event"] if parts else ["Generic Event"]
        return " ".join(parts).title()

    @classmethod
    def send(cls, *args, **kargs):
        """Sends a notification to all the subscribers listening to this event.
        """
        event = cls(*args, **kargs)
        cls.manager.notify(event)

    @classmethod
    def subscribe(cls, handler):
        """Subscribes a handler function to the notification feed of this event.
        """
        cls.manager.subscribe(cls, handler)

    @classmethod
    def unsubscribe(cls, handler):
        """Unsubscribes a handler function from the notification feed of this
        event.
        """
        cls.manager.unsubscribe(cls, handler)

    @classmethod
    def listen(cls, func):
        """Decorator used to subscribe to an event."""
        params = list(inspect.signature(func).parameters.keys())
        if len(params) == 1:
            # This is a normal function
            cls.subscribe(func)
        elif len(params) == 2 and params[0] == 'self':
            # This is an unbound instance function
            if not hasattr(func, "_zevents"):
                setattr(func, "_zevents", [])
            func._zevents.append(cls)
        else:
            raise TypeError(
                f"Cannot subscribe {func.__qualname__}. Incorrect signature."
            )

        return func

    def __str__(self):
        """Converts the current event to a string representation."""
        return f'[{self.name}]'
