# -*- coding: utf-8 -*-

def init():
    import sys
    import os
    import os.path
    if sys.version_info.major != 2:
        sys.exit('Python 2 is required to run this program')

    fdir = None
    if hasattr(sys, "frozen") and \
            sys.frozen in ("windows_exe", "console_exe"):
        fdir = os.path.dirname(os.path.abspath(sys.executable))
        sys.path.append(fdir)
        fdir = os.path.join(fdir, '..')
    else:
        fdir = os.path.dirname(__file__)

    with open(os.path.join(fdir, 'apikey.cfg')) as f:
        exec(f.read())

    srv = locals().get('SERVER')
    from facepp import API
    return API(API_KEY, API_SECRET, srv = srv)

api = init()

from facepp import API, File

del init

def _run():
    global _run
    _run = lambda: None

    msg = """
===================================================
Welcome to Face++ Interactive Shell!
Here, you can explore and play with Face++ APIs :)
---------------------------------------------------
Getting Started:
    0. Register a user and API key on https://cloud.megvii.com/
    1. Write your API key/secret in apikey.cfg
    2. Start this interactive shell and try various APIs
        For example, to find all faces in a local image file, just type:
            api.detect(image_file = File(r'<path to the image file>'))

Enjoy!
"""

    try:
        from IPython import embed
        embed(banner2 = msg)
    except ImportError:
        import code
        code.interact(msg, local = globals())


if __name__ == '__main__':
    _run()
