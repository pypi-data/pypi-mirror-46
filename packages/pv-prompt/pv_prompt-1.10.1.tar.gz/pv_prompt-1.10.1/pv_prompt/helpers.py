import asyncio
import logging
from functools import wraps

#from .print_output import print_dict, print_waiting_done
from pv_prompt.print_output import print_dict, print_waiting_done
from pv_prompt.settings import ATTR_VERBOSITY, GLOBALS

LOGGER = logging.getLogger(__name__)
_LOOP = None


def get_loop():
    """Return a default asyncio event loop."""
    global _LOOP

    if _LOOP is not None:
        return _LOOP

    _LOOP = asyncio.get_event_loop()
    return _LOOP


def verboser(func):
    """Print out response when verbosity is True."""

    @wraps(func)
    async def wrapper(*args, **kwargs):
        response = await func(*args, **kwargs)
        if GLOBALS[ATTR_VERBOSITY]:
            if isinstance(response, dict):
                print_dict(response)

    return wrapper


def spinner(message):
    """Wraps a Waiting.... done spinner around a method"""

    def _spinner(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            done = print_waiting_done(message)
            res = await func(*args, **kwargs)
            await done()
            return res

        return wrapper

    return _spinner
