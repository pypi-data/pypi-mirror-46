import logging
import threading
import time

import queue as q

class CThreadException(Exception):
    """Base class of any ControllableThread exception.
    
    All exceptions that are thrown by the :mod:`cthread` module inherit from
    this exception.  This specific exception instance is however never raised.

    Args:
        message (str, optional): Information about the exception that was
            raised.
    """

    def __init__(self, message=None, *args, **kwargs):
        """Initialises the :class:`cthread.CThreadException` exception."""
        Exception.__init__(self, *args, **kwargs)

        self._message = message

    def __str__(self):
        """Overrides the __str__ method of the :class:`Exception` class."""
        if self._message == None:
            return Exception.__str__(self)
        else:
            return self._message

class InvalidArgument(CThreadException):
    """Base class of any invalid argument exception.

    This exception is raised if an invalid argument is input to any publicly
    accessible :mod:`cthread` method.  This specific exception instance is
    however never raised.

    Args:
        message (str, optional): Information about the exception that was
            raised.
    """

    def __init__(self, message=None, *args, **kwargs):
        """Initialises the :class:`cthread.InvalidArgument` exception."""
        if message == None:
            message = "Specified argument is invalid."

        CThreadException.__init__(self, message, *args, *kwargs)

class InvalidState(InvalidArgument):
    """Base class of an unrecognised thread state.
    
    This exception is raised if a thread state is not recognised.  While this
    exception is a base class of an unrecognised thread state, this specific
    instance could also be raised.

    Args:
        message (str, optional): Information about the exception that was
            raised.
    """

    def __init__(self, message=None, *args, **kwargs):
        """Initialises the :class:`cthread.InvalidState` exception."""
        if message == None:
            message = "Invalid state.  Ensure: state is <class 'int'> and " \
                    "STARTED <= state <= maxState."

        InvalidArgument.__init__(self, message, *args, **kwargs)

class InvalidMaxState(InvalidState):
    """Maximum thread state is not recognised.
    
    This exception is raised if the maximum thread state is not recognised.
    
    Args:
        message (str, optional): Information about the exception that was
            raised.
    """

    def __init__(self, message=None, *args, **kwargs):
        """Initialises the :class:`cthread.InvalidMaxState` exception."""
        if message == None:
            message = "Invalid maxState.  Ensure: maxState is <class 'int'> " \
                    "and STARTED <= maxState."

        InvalidArgument.__init__(self, message, *args, **kwargs)

class InvalidName(InvalidArgument):
    """Desired name of the thread is not a string.
    
    This exception is raised if the name of the thread is not a string.

    Args:
        message (str, optional): Information about the exception that was
            raised.
    """

    def __init__(self, message=None, *args, **kwargs):
        """Initialises the :class:`cthread.InvalidName` exception."""
        if message == None:
            message = "Invalid name.  Ensure: name is <class 'str'>."

        InvalidArgument.__init__(self, message, *args, **kwargs)

class InvalidQueue(InvalidArgument):
    """No communication method to the initialising thread.
    
    This exception is raised if an instance of a
    :class:`cthread.ControllableThread` is initialised without a means of
    communicating with the thread that initialises it.
        
    Args:
        message (str, optional): Information about the exception that was
            raised.
    """

    def __init__(self, message=None, *args, **kwargs):
        """Initialises the :class:`cthread.InvalidQueue` exception."""
        if message == None:
            message = "Invalid queue.  Ensure: queue is <class 'queue.Queue'>."

        InvalidArgument.__init__(self, message, *args, **kwargs)

class ThreadState(object):
    """Represents the state of the thread.
    
    Attributes:
        STARTED (int): Numerical encoding of the 'started' thread state.
        ACTIVE (int): Numerical encoding of the 'active' thread state.
        IDLE (int): Numerical encoding of the 'idle' thread state.
        PAUSED (int): Numerical encoding of the 'paused' thread state.
        RESUMED (int): Numerical encoding of the 'resumed' thread state.
        KILLED (int): Numerical encoding of the 'killed' thread state.
    """

    def __init__(self):
        """Initialises the thread state constants and the thread state."""

        # Public attributes #
        self.STARTED = 0
        self.ACTIVE = 1
        self.IDLE = 2
        self.PAUSED = 3
        self.RESUMED = 4
        self.KILLED = 5

        # Private attributes #
        self._maxState = self.KILLED
        self._state = self.STARTED

    def update_max_state(self, maxState):
        """Updates the maximum state of the thread.

        The `maxState` value is used to determine the validity of a state to
        supplied to the :py:attr:`cthread.ThreadState.update_state()` function.
        The state of the thread must be within a predefined range, or else it is
        an invalid state.  The `maxState` is also not a fixed constant because
        the user can define their own states, and hence the validity check of a
        state must accomodate these user-defined states.

        Args:
            maxState (int): Maximum state that the thread can take.

        Raises:
            :class:`cthread.InvalidState`: If the maximum state is <
                :py:attr:`ThreadState.STARTED`.
        """
        if not isinstance(maxState, int) or maxState < self.STARTED:
            raise InvalidState("Invalid maxState.  Ensure: maxState is " \
                    "<class 'int'> and STARTED <= maxState.")
        
        self._maxState = maxState

    def update_state(self, state):
        """Updates the state of the thread.
        
        Args:
            state (int): New state of the thread.

        Raises:
            :class:`cthread.InvalidState`: If `state` <
                :py:attr:`ThreadState.STARTED` or `state` >
                :py:attr:`ThreadState._maxState`
        """
        if not isinstance(state, int) or state < self.STARTED or \
                state > self._maxState:
            raise InvalidState()

        self._state = state

    def get_state(self):
        """Gets the state of the thread.

        Returns:
            int: State of the thread.  There are at least six possible return \
                values:

                - :py:attr:`ThreadState.STARTED`: if the thread is being \
                    initialised,
                - :py:attr:`ThreadState.ACTIVE`: if the thread is currently \
                    running,
                - :py:attr:`ThreadState.IDLE`: if the thread is currently not \
                    running,
                - :py:attr:`ThreadState.PAUSED`: if the thread is \
                    transitioning from running to not running.
                - :py:attr:`ThreadState.RESUMED`: if the thread is \
                    transitioning from not running to running.
                - :py:attr:`ThreadState.KILLED`: if the thread is in the \
                    process of terminating, and
                - Any other user-defined thread states.
        """
        return self._state

class ControllableThread(threading.Thread):
    """ Parent class for any :class:`cthread.ControllableThread`.

    Allows threads to be killed, paused and resumed, and allows for direct
    communication to the main initialising thread.

    Args:
        name (str): Name of the thread.
        queue (:class:`queue.Queue`): Priority queue for communication to the
            main thread.

    Raises:
        :class:`cthread.InvalidName`: if name is not a string.
        :class:`cthread.InvalidQueue`: if queue is not a Queue.
    """

    def __init__(self, name, queue):
        """Initialises the :class:`cthread.ControllableThread`."""
        threading.Thread.__init__(self)

        if not isinstance(name, str):
            raise InvalidName()
            
        if not isinstance(queue, q.Queue):
            raise InvalidQueue()

        self._name = name
        self._queue = queue
        self._logger = logging.getLogger(name + "_t")
        self._threadState = ThreadState()

    def _started_callback(self):
        """Thread start callback function.  May be overwritten by child."""
        self._logger.info("(Re)initialising...")

    def _active_callback(self):
        """Thread active callback function.  May be overwritten by child."""
        pass

    def _idle_callback(self):
        """Thread idle callback function.  May be overwritten by child."""
        pass

    def _paused_callback(self):
        """Thread paused callback function.  May be overwritten by child."""
        self._logger.info("Pausing...")

    def _resumed_callback(self):
        """Thread resume callback function.  May be overwritten by child."""
        self._logger.info("Resuming...")

    def _killed_callback(self):
        """Thread killed callback function.  May be overwritten by child."""
        self._logger.info("Killing...")

    def _alternative_callback(self):
        """Alternative state callback function.  May not be implemented."""
        pass

    def _is_started(self):
        """Checks if the thread state is :py:attr:`ThreadState.STARTED`.

        Returns:
            bool: Is the state of the thread :py:attr:`ThreadState.STARTED`.

                - True: If the thread state is :py:attr:`ThreadState.STARTED`, \
                    and
                - False: If the thread state is not.
        """
        return self._get_state() == self._threadState.STARTED

    def _is_active(self):
        """Checks if the thread state is :py:attr:`ThreadState.ACTIVE`.

        Returns:
            bool: Is the state of the thread :py:attr:`ThreadState.ACTIVE`.

                - True: If the thread state is :py:attr:`ThreadState.ACTIVE`, \
                    and
                - False: If the thread state is not.
        """
        return self._get_state() == self._threadState.ACTIVE

    def _is_idle(self):
        """Checks if the thread state is :py:attr:`ThreadState.IDLE`.

        Returns:
            bool: Is the state of the thread :py:attr:`ThreadState.IDLE`.

                - True: If the thread state is :py:attr:`ThreadState.IDLE`, \
                    and
                - False: If the thread state is not.
        """
        return self._get_state() == self._threadState.IDLE

    def _is_paused(self):
        """Checks if the thread state is :py:attr:`ThreadState.PAUSED`.

        Returns:
            bool: Is the state of the thread :py:attr:`ThreadState.PAUSED`.

                - True: If the thread state is :py:attr:`ThreadState.PAUSED`, \
                    and
                - False: If the thread state is not.
        """
        return self._get_state() == self._threadState.PAUSED

    def _is_resumed(self):
        """Checks if the thread state is :py:attr:`ThreadState.RESUMED`.

        Returns:
            bool: Is the state of the thread :py:attr:`ThreadState.RESUMED`.

                - True: If the thread state is :py:attr:`ThreadState.RESUMED`, \
                    and
                - False: If the thread state is not.
        """
        return self._get_state() == self._threadState.RESUMED

    def _is_killed(self):
        """Checks if the thread state is :py:attr:`ThreadState.KILLED`.

        Returns:
            bool: Is the state of the thread :py:attr:`ThreadState.KILLED`.

                - True: If the thread state is :py:attr:`ThreadState.KILLED, \
                    and
                - False: If the thread state is not.
        """
        return self._get_state() == self._threadState.KILLED

    def _update_max_state(self, maxState):
        """Updates the maximum state of the thread.

        The `maxState` value is used to determine the validity of a state to
        supplied to the :py:attr:`cthread.ThreadState.update_state()` function.
        The state of the thread must be within a predefined range, or else it is
        an invalid state.  The `maxState` is also not a fixed constant because
        the user can define their own states, and hence the validity check of a
        state must accomodate these user-defined states.

        Args:
            maxState (int): Maximum state that the thread can take.

        Raises:
            :class:`cthread.InvalidState`: If the maximum state is <
                :py:attr:`ThreadState.STARTED`.
        """
        self._threadState.update_max_state(maxState)

    def _update_state(self, state):
        """Updates the state of the thread.
        
        Args:
            state (int): New state of the thread.

        Raises:
            :class:`cthread.InvalidState`: If `state` <
                :py:attr:`ThreadState.STARTED` or `state` >
                :py:attr:`ThreadState._maxState`
        """
        self._threadState.update_state(state)

    def _get_state(self):
        """Gets the state of the thread.

        Returns:
            int: State of the thread.  There are at least six possible return \
                values:

                - :py:attr:`ThreadState.STARTED`: if the thread is being \
                    initialised,
                - :py:attr:`ThreadState.ACTIVE`: if the thread is currently \
                    running,
                - :py:attr:`ThreadState.IDLE`: if the thread is currently not \
                    running,
                - :py:attr:`ThreadState.PAUSED`: if the thread is \
                    transitioning from running to not running.
                - :py:attr:`ThreadState.RESUMED`: if the thread is \
                    transitioning from not running to running.
                - :py:attr:`ThreadState.KILLED`: if the thread is in the \
                    process of terminating, and
                - Any other user-defined thread states.
        """
        return self._threadState.get_state()

    def run(self):
        """Entry point for the thread.

        Contains the cyclic executive of the thread.  There are at least six
        possible states for the thread:

        1. STARTED
        2. ACTIVE
        3. IDLE
        4. PAUSED
        5. RESUMED
        6. KILLED
        7. Any alternative individual thread-specific states.

        Each of these states has a callback function that must be implemented
        in any of the child threads.  Of course, the alterative state callback
        should not be implemented if there are no alternative states.

        This cyclic executive will execute as long as the thread is not killed.
        """
        self._logger.info("Starting thread: {0}...".format(self._name))

        while not self._is_killed():

            # Initialise thread #
            if self._is_started():
                self._started_callback()

            # Start running the thread #
            elif self._is_active():
                self._active_callback()

            # Stop running the thread #
            elif self._is_idle():
                self._idle_callback()

            # Transition the thread from running to not running #
            elif self._is_paused():
                self._paused_callback()

            # Transition the thread from not running to running #
            elif self._is_resumed():
                self._resumed_callback()

            # Thread specific state must begin #
            else:
                self._alternative_callback()

        # Kill the thread #
        self._killed_callback()
        self._logger.info("Stopping thread: {0}...".format(self.name))

    def reset(self):
        """Updates the state of the thread to :py:attr:`ThreadState.STARTED`."""
        self._update_state(self._threadState.STARTED)

    def pause(self):
        """Updates the state of the thread to :py:attr:`ThreadState.PAUSED`."""
        self._update_state(self._threadState.PAUSED)

    def resume(self):
        """Updates the state of the thread to :py:attr:`ThreadState.RESUMED`."""
        self._update_state(self._threadState.RESUMED)

    def kill(self):
        """Updates the state of the thread to :py:attr:`ThreadState.KILLED`."""
        self._update_state(self._threadState.KILLED)