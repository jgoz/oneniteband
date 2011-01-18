config = {}

config['tipfy'] = {
    # Enable debugger. It will be loaded only in development.
    'middleware': [
        'tipfy.ext.debugger.DebuggerMiddleware',
    ],
}
config['tipfy.ext.session'] = {
    'secret_key': "don't worry, this isn't the real production key.",
}
config['oneniteband'] = {
    'static_path': '/static/',
}
