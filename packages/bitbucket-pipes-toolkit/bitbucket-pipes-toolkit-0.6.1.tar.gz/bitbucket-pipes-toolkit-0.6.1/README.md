Pipetools
=========
This package contains various tools and helpers to make it more fun and easy for people to develope pipes.

Installation
============

`pip install bitbucket_pipes_toolkit`

Module pipetools.helpers
========================

Functions
---------

`configure_logger()`
:   Configure logger to produce colorized output.

`enable_debug()`
:   Enable the debug log level.

`fail(message='Fail!', do_exit=True)`
:   Prints the colorized failure message (in red)
    
    Args:
        message (str, optional): Output message
        do_exit (bool, optional): Call sys.exit if set to True

`get_variable(name, required=False, default=None)`
:   Fetch the value of a pipe variable.
    
    Args:
        name (str): Variable name.
        required (bool, optional): Throw an exception if the env var is unset.
        default (:obj:`str`, optional): Default value if the env var is unset.
    
    Returns:
        Value of the variable
    
    Raises
        Exception: If a required variable is missing.

`required(name)`
:   Get the value of a required pipe variable.
    
    This function is basically an alias to get_variable with the required 
        parameter set to True.
    
    Args:
        name (str): Variable name.
    
    Returns:
        Value of the variable
    
    Raises
        Exception: If a required variable is missing.

`success(message='Success', do_exit=True)`
:   Prints the colorized success message (in green)
    
    Args:
        message (str, optional): Output message
        do_exit (bool, optional): Call sys.exit if set to True
