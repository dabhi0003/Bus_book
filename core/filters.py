# app_name/filters.py

def jinja2_range(start, stop=None, step=1):
    if stop is None:
        start, stop = 0, start
    return range(start, stop, step)
