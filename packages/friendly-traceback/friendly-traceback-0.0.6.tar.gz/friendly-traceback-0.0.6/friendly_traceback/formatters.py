"""formatters.py

"""

friendly_items = [
    ("header", "indent"),
    ("message", "double"),
    ("generic", "indent"),
    ("parsing error", "indent"),  # only for SyntaxError and subclasses
    ("parsing error source", "none"),  # only for SyntaxError and subclasses
    ("cause header", "indent"),
    ("cause", "double"),
    ("last_call header", "indent"),
    ("last_call source", "none"),
    ("last_call variables", "none"),
    ("exception_raised header", "indent"),
    ("exception_raised source", "none"),
    ("exception_raised variables", "none"),
]

explain_items = [
    ("header", "indent"),
    ("message", "double"),
    ("generic", "indent"),
    ("parsing error", "indent"),  # only for SyntaxError and subclasses
    ("parsing error source", "none"),  # only for SyntaxError and subclasses
    ("cause header", "indent"),
    ("cause", "double"),
]


def format_traceback(info, level=1):
    """ Simple text formatter for the traceback."""
    result = choose_formatter[level](info)
    return "\n".join(result)


def default(info, items=None):
    """Shows all the information processed by Friendly-traceback with
       formatting suitable for REPL.
    """
    if items is None:
        items = friendly_items
    spacing = {"indent": " " * 4, "double": " " * 8, "none": ""}
    result = [""]
    for item, formatting in items:
        if item in info:
            for line in info[item].split("\n"):
                result.append(spacing[formatting] + line)
    return result


def python_traceback_before(info):
    """Includes the normal Python traceback before all the information
       processed by Friendly-traceback.
    """
    result = [""]
    result.append(info["python_traceback"])
    result.extend(default(info))
    return result


def python_traceback_after(info):
    """Includes the normal Python traceback after all the information
       processed by Friendly-traceback.
    """
    result = default(info)
    result.append(info["python_traceback"])
    return result


def only_add_explain(info):
    """Includes the normal Python traceback before adding the generic
       information about a given exception and the likely cause.
    """
    result = [""]
    result.append(info["python_traceback"])
    if "generic" in info:
        result.append("    " + info["generic"])
    if "cause header" in info:
        result.append("    " + info["cause header"])
    if "cause" in info:
        result.append("        " + info["cause"])
    return result


def only_explain(info):
    result = default(info, items=explain_items)
    return result


choose_formatter = {
    1: default,
    2: python_traceback_before,
    3: only_add_explain,
    4: only_explain,
    9: python_traceback_after,
}
