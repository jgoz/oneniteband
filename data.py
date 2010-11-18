from sqlalchemy import create_engine, MetaData, Table

class Database(object):
    def __init__(self, dbstr):
        self.engine = create_engine(dbstr, convert_unicode=True)
        self.metadata = MetaData(bind=self.engine, reflect=True)

    def table(self, name):
        return Table(name, self.metadata, autoload=True)

    def conn(self):
        return engine.connect()

def get_page_content(db, page):
    content = db.table('content')
    return content.select(content.c.page == page).execute()
