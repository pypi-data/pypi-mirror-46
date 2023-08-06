__author__ = "Pawel Kowalik"
__copyright__ = "Copyright 2018, 1&1 IONOS SE"
__credits__ = []
__license__ = "MIT"
__maintainer__ = "Pawel Kowalik"
__email__ = "pawel-kow@users.noreply.github.com"
__status__ = "Beta"

def stringify_keys(d):
    """Convert a dict's keys to strings if they are not."""
    if hasattr(d, 'keys'):
        to_iterate = list(d.keys())
        for key in to_iterate:

            # check inner dict
            if isinstance(d[key], dict):
                value = stringify_keys(d[key])
            else:
                value = d[key]

            # convert nonstring to string if needed
            if not isinstance(key, str):
                # noinspection PyBroadException
                try:
                    d[str(key)] = value
                except Exception:
                    try:
                        d[repr(key)] = value
                    except Exception:
                        raise

                # delete old k
                del d[key]

    if hasattr(d, '__dict__'):
        for k in d.__dict__:
            if isinstance(getattr(d, k), dict):
                setattr(d, k, stringify_keys(getattr(d, k)))

    return d
