from datetime import datetime
from google.appengine.ext import db
from markdown import markdown

class Gig(db.Model):
    date = db.DateProperty()
    title = db.StringProperty()
    place = db.StringProperty()

    @staticmethod
    def get_upcoming():
        return Gig.all().filter('date >', datetime.now()).order('-date').fetch(5)

class TextContent(db.Model):
    text = db.TextProperty()
    timestamp = db.DateTimeProperty()

    def to_html(self):
        return markdown(self.text)

    def to_dict(self):
        return {'raw': self.text, 'html': self.to_html()}

    @staticmethod
    def for_key(key):
        return TextContent.get_by_key_name(key)

    @staticmethod
    def save(key, text):
        content = TextContent(key_name=key, text=text)
        content.put()
        return content

class AuthorizedEmail(db.Model):
    email = db.EmailProperty()

    @staticmethod
    def check(email):
        return AuthorizedEmail.all().filter('email =', email).count() > 0

