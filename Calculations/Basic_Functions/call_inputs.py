import inspect
import Inputs.inputs as inputs

# every plain variable in inputs.py, as a dict
INPUTS = {k: v for k, v in vars(inputs).items() if not k.startswith("_")}

def call(fn, **extra):
    """Call fn, filling each argument from Inputs (or from `extra`)."""
    values  = {**INPUTS, **extra}
    params  = inspect.signature(fn).parameters
    missing = [p for p in params if p not in values]
    if missing:
        raise TypeError(f"{fn.__name__} needs {missing}, not found in Inputs")
    return fn(**{p: values[p] for p in params})