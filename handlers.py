from data import AuthorizedEmail, Gig, TextContent
from datetime import datetime
from django.utils import simplejson
from tipfy import RequestHandler, Response, cached_property
from tipfy.ext.auth import AppEngineAuthMixin, login_required, user_required
from tipfy.ext.auth.google import GoogleMixin
from tipfy.ext.jinja2 import Jinja2Mixin, get_env
from tipfy.ext.session import AllSessionMixins, SessionMiddleware
from tipfy.ext.wtforms import Form, fields

def gigdate(dt):
    return dt.strftime('%b %d')

class RestfulRequestHandler(RequestHandler):
    def dispatch(self, method, **kwargs):
        if method.lower() == 'post' and self.request.form.has_key('method'):
            form_method = str(self.request.form['method']).lower()
            if form_method in self.app.allowed_methods:
                method = form_method
        return super(RestfulRequestHandler, self).dispatch(method, **kwargs)

class BaseHandler(RestfulRequestHandler, AppEngineAuthMixin, Jinja2Mixin, AllSessionMixins):
    middleware = [SessionMiddleware]

    def render_response(self, filename, **kwargs):
        self.request.context.update({
            'auth_session': self.auth_session,
            'current_user': self.auth_current_user,
            'login_url':    self.auth_login_url(),
            'logout_url':   self.auth_logout_url(),
            'current_url':  self.request.url,
            'now':          datetime.now(),
        })
        if self.messages:
            self.request.context['messages'] = simplejson.dumps(self.messages)

        jinja_env = get_env()
        jinja_env.filters['gigdate'] = gigdate

        static_path = self.get_config('oneniteband', 'static_path')
        jinja_env.globals['static_path'] = lambda filename: static_path + filename

        return super(BaseHandler, self).render_response(filename, **kwargs)

    def redirect_path(self, default='/'):
        url = self.request.args.get('continue', '/')

        if not url.startswith('/'):
            url = default

        return url

class IndexHandler(BaseHandler):
    def get(self, **kwargs):
        return self.render_response('index.html', gigs=Gig.get_upcoming())

class BioHandler(BaseHandler):
    def get(self, **kwargs):
        return self.render_response('bio.html', band_bio=TextContent.for_key('band_bio'))

class TextContentHandler(BaseHandler):
    def _content_response(self, content):
        if not content:
            return Response('', 'text/plain')
        return Response(content.text, 'text/plain')

    def get(self, id):
        return _content_response(TextContent.for_key(id))

    @user_required
    def post(self, id):
        return _content_response(TextContent.save(id, self.request.form.get('content')))

    @user_required
    def put(self, id):
        return _content_response(TextContent.save(id, self.request.form.get('content')))

class ImageContentHandler(BaseHandler):
    def _content_response(self, content):
        if not content:
            # TODO return empty image
            raise 'Image not found.'
        return Response(content.image, content.mimetype)

    def get(self, id):
        return _content_response(ImageContent.for_key(id))

class AdminHandler(BaseHandler):
    def get(self, **kwargs):
        return redirect(self.auth_login_url())

class SignupForm(Form):
    nickname = fields.TextField('Nickname')

class SignupHandler(BaseHandler):
    @login_required
    def get(self, **kwargs):
        redirect_url = self.redirect_path()

        if self.auth_current_user:
            # User is already registered, so don't display the signup form.
            return redirect(redirect_url)

        return self.render_response('signup.html', form=self.form)

    @login_required
    def post(self, **kwargs):
        redirect_url = self.redirect_path()

        if self.auth_current_user:
            # User is already registered, so don't process the signup form.
            return redirect(redirect_url)

        if self.form.validate():
            email = self.auth_session.email()
            if not AuthorizedEmail.check(email):
                self.set_message('error', '%s has not been preauthorized for administration.' % (email), life=None)
                return self.get(**kwargs)

            auth_id = 'gae|%s' % self.auth_session.user_id()
            user = self.auth_create_user(self.form.nickname.data, auth_id, email=email)
            if user:
                self.set_message('success', 'You are now registered. Welcome!', flash=True, life=5)
                return redirect(redirect_url)
            else:
                self.set_message('error', 'This nickname is already registered.', life=None)
                return self.get(**kwargs)

        self.set_message('error', 'A problem occurred. Please correct the errors listed in the form.', life=None)
        return self.get(**kwargs)

    @cached_property
    def form(self):
        return SignupForm(self.request)
