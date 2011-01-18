import os
import sys

if 'lib' not in sys.path:
    # Add /lib as primary libraries directory, with fallback to /distlib
    # and optionally to distlib loaded using zipimport.
    sys.path[0:0] = ['lib', 'distlib', 'distlib.zip']

import config
import tipfy
import urls

def enable_appstats(app):
    """Enables appstats middleware."""
    if debug:
        return

    from google.appengine.ext.appstats.recording import appstats_wsgi_middleware
    app.wsgi_app = appstats_wsgi_middleware(app.wsgi_app)

def enable_jinja2_debugging():
    """Enables blacklisted modules that help Jinja2 debugging."""
    if not debug:
        return

    # This enables better debugging info for errors in Jinja2 templates.
    from google.appengine.tools.dev_appserver import HardenedModulesHook
    HardenedModulesHook._WHITE_LIST_C_MODULES += ['_ctypes', 'gestalt']

# Is this the development server?
debug = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')

# Instantiate the application.
app = tipfy.make_wsgi_app(rules=urls.rules, config=config.config, debug=debug)

def main():
    app.run()

if __name__ == '__main__':
    main()
