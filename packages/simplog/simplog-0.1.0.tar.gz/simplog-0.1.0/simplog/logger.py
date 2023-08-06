from functools import partial
from datetime import datetime
from typing import Callable, Any


def force_string(s: Any) -> str:
    """converts an Any value into a string by forcing string formatting"""
    return f'{s}'


def escape_value(s: Any, to_str_func: Callable[[Any], str]=force_string, force_quotes:bool=False) -> str: 
    """Performs successive steps to convert a regular string into one ready to be consumed by the logging function"""
    stringified = to_str_func(s)
    escape_funcs = [
        escape_backslash,
        escape_null,
        escape_newline,
        escape_tab,
        escape_quotes,
        lambda x: quote_string(x, force_quotes),  # Maybe this should be done via partial... maybe passed in to pre-compile it then?
    ]

    for step in escape_funcs:
        stringified = step(stringified)

    return stringified


def escape_backslash(s: str) -> str: 
    """Replaces any \\ character with \\\\"""
    return s.replace('\\', '\\\\')


def escape_newline(s: str) -> str:
    """Replaces each new line character (\\n) in the input with \\\\n""" 
    return s.replace('\n', '\\n')  # Todo: replace with re.sub and factor in \r

def escape_tab(s: str) -> str:
    """Replaces each tab character (\\t) in the input with \\\\t""" 
    return s.replace('\t', '\\t')

def escape_null(s: str) -> str:
    """Replaces each null character (\\0) in the input with \\\\0""" 
    return s.replace("\0", "\\0")


def escape_quotes(s: str) -> str:
    """Replaces double quotes in the input string with either ' or \\". 
        
    Description:
        Given a string, returns that string with double quotes escaped in one of two ways.
        If the string contains single quotes, then \\" will be used to escape the double quotes. 
        Otherwise, a single quote (') will be used instead.

    Examples:
        >>> escape_quotes('one "two" three')
        "one 'two' three"
        >>> escape_quotes('"He said he didn\\'t know."')
        '\\\\"He said he didn\\'t know.\\\\"'
    """
    if "'" in s:
        return s.replace('"', '\\"')
    return s.replace('"', "'")


def quote_string(s: str, force:bool=False) -> str:
    """Sometimes wraps strings in double quotes, depending on the content and force parameter.
    
    Description:
        This function provides conditional wrapping of strings inside double quotes. 
        If the input string contains a space, OR force is set to True, then the input string will 
        always be quoted.
        If the input string does not contain a space, AND force is set to False, then the input 
        string is returned unmodified.

    Args:
        s: The string that needs to be wrapped in quotes (maybe)
        force (optional): Whether to force quotes around the string even if not needed. Defaults to False.

    Examples:
        >>> quote_string("nevermore", False)
        'nevermore'
        >>> quote_string("nevermore")
        'nevermore'
        >>> quote_string("nevermore", True)
        '"nevermore"'
        >>> quote_string("never more", False)
        '"never more"'
    
    Returns:
        The string, maybe wrapped in double quotes
    """
    return f'"{s}"' if force or ' ' in s else s


def make_logger(write_func:Callable[[str], None]=print, *, message_label="msg", level_label="level", time_label=None, 
                to_string_func=force_string, force_quote=False):
    """Generates a logging function with some predefined functionality. 

    Description:
        A function to generate a semi-customizable logging function, specifically targeted for 
        microservices. The returned function contains basic logging info: Time of the event, 
        severity level, custom message, plus optional key/value pairs (provided as kwargs). The 
        general format is:
        ``<event><severity><provided key/value pairs><generic message>`` As a rough example:
        2019-05-13T12:01:27.424242 level=info key1=value1 key2="value 2" msg="Just a test"

    Args:
        write_func (optional): a function used to "record" the logged output. By default, this is print
        message_label (optional): What to call the value containing the generic log message. Defaults to 'msg'
        level_label (optional): What to call the severity level field. Defaults to 'level'
        time_label (optional): What to call the time/date field. Defaults to None, which means no label
        to_string_func (optional): During logging, the function used to convert an input value to a string. 
            Defaults to force_string
        force_quote (optional): If True, forces all values to be wrapped in double quotes. Defaults to False

    Returns:
        A callable function that takes a message, an optional severity level and any keyword args, 
        which can then be used to write out a log to the desired location
    """
    time_label = '' if time_label is None else f'{time_label}='
    esc = lambda m: escape_value(m, to_string_func, force_quote)

    def log(message, level='info', **kwargs) -> None:
        now = f'{time_label}{datetime.now().isoformat()}'
        msg = f'{message_label}={esc(message)}'
        lvl = f'{level_label}={esc(level)}'

        v_fields = [] if kwargs == {} else (f'{k}={esc(v)}' for k, v in kwargs.items())

        line = f'{now} {lvl} {" ".join(v_fields)}{" " if v_fields else ""}{msg}'
        write_func(line)

    return log


def refine_logger(logger, **kwargs):
    """Allows for the logging function to be amended with constant key/value pairs.
    
    Description:
        Returns back a function that will provide the logger function with pre-provided
        kwargs values. Useful in situations where you may log the same field multiple times, such
        as inside a particular function (e.g. inside=do_work) or when needing to identify a chain of
        events through multiple levels (e.g. message_context=abc123)
    
    Returns:
        A modified function with pre-provided kwargs. Note that these args can be overwritten later,
        but cannot be removed.
    """
    return partial(logger, **kwargs)
