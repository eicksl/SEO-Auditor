import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from constants import DB_URI
from models import Base, UniqueInboundOK


class SiteMapper():
    def __init__(self):
        engine = create_engine(DB_URI)
        Base.metadata.bind = engine
        self.db = sessionmaker(bind=engine)()
        self.write_sitemaps()


    def write_sitemaps(self):
        query = self.db.query(UniqueInboundOK).order_by(UniqueInboundOK.url)
        xml = open('reports/sitemap/sitemap.xml', 'w', encoding='utf-8')
        txt = open('reports/sitemap/sitemap.txt', 'w', encoding='utf-8')
        xml.write('''<?xml version="1.0" encoding="utf-8"?>\n''')
        xml.write('''<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">\n''')
        for entry in query:
            xml.write('  <url>\n    <loc>{}</loc>\n  </url>\n'.format(entry.url))
            txt.write(entry.url + '\n')
        xml.write('</urlset>')
        xml.close()
        txt.close()



SiteMapper()
