from tipfy import Rule, HandlerPrefix

rules = [
    HandlerPrefix('handlers.', [
        Rule('/', endpoint='index', handler='IndexHandler'),
        Rule('/bio', endpoint='bio', handler='BioHandler'),
        Rule('/content/text/<id>', endpoint='text-content', handler='TextContentHandler'),
        Rule('/content/image/<id>', endpoint='image-content', handler='ImageContentHandler'),
        Rule('/admin', endpoint='admin', handler='AdminHandler'),
        Rule('/auth/signup', endpoint='auth/signup', handler='SignupHandler')
    ]),
]
