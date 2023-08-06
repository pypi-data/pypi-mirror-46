=====
Usage
=====

To use zevents in a project::

    import zevents

The zevents package defines two standard events that can be used to control an
event-driven application: TickEvent and QuitEvent. TickEvent aims at being sent
in the main application loop to process queues in the internal event manager.

Here is an example of how to use those events to control an echo console
application using an event-based logic.

The KeyboardController class subscribes to Tick events, reacts to those by
asking the user to enter a few words and sends a Quit event if the user inputs
a `quit`::

    from zevents import Event
    from zevents.dispatch import listener


    # We create events by subsclassing the zevents.Event class
    class TickEvent(Event):
        pass

    class QuitEvent(Event):
        pass

    # For a class to be able to listen at zevents, decorate it as listener
    @listener
    class KeyboardController:
        """Controller responsible to handle keyboard events."""

        # Available actions
        actions = {
            "quit": QuitEvent.send,
        }

        @TickEvent.listen
        def _on_tick(self, event):
            """Handles the Tick events."""
            user = input("Say something or enter quit: ")
            action = self.actions.get(
                user.lower().strip(), lambda: print(user)
            )
            action()

The EchoApplication class could be written as follows::

    from zevents import Event
    from zevents.dispatch import Listener


    # For a class to be able to listen at zevents, you can also subclass Listener
    class EchoApplication(Listener):
        """Represents the application itself."""

        def __init__(self):
            super().__init__()
            self.running = False
            self.controller = KeyboardController()

        @QuitEvent.listen
        def _on_quit(self, event):
            """Handles Quit events."""
            self.running = False

        def run(self):
            """Starts the application event loop."""
            self.running = True
            while self.running:
                # We send a Tick event in each loop
                TickEvent.send()

Let's run this application::

    >>> app = EchoApplication()
    >>> app.run()

