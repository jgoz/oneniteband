from cryptacular.bcrypt import BCRYPTPasswordManager
from datetime import datetime
from sqlalchemy import create_engine, MetaData, Table

class Database(object):
    def __init__(self, dbstr):
        self.engine = create_engine(dbstr, convert_unicode=True)
        self.metadata = MetaData(bind=self.engine, reflect=True)

    def table(self, name):
        return Table(name, self.metadata, autoload=True)

    def conn(self):
        return engine.connect()

def get_upcoming_gigs(db):
    gig = db.table('gig')
    return gig.select(gig.c.date > datetime.now).limit(5).order_by(gig.c.date).execute()

def get_band_bio(db):
    bio = db.table('bio')
    return bio.select(bio.c.slug == 'band').limit(1).execute().first()

def get_member_bios(db):
    bio = db.table('bio')
    return bio.select(bio.c.type == 'member').order_by(bio.c.name).execute().fetchall()

def get_admin(db, username):
    admin = db.table('admin')
    return admin.select(admin.c.username == username).execute().first()

def add_admin(db, username, password):
    bcrypt = BCRYPTPasswordManager()
    admin = db.table('admin')
    return admin.insert(values=dict(username=username, hash=bcrypt.encode(password))).execute()
